import sqlite3
import os
import requests

recipe_database = 'recipe_sqlite.db'

def create_database():
    '''Create an SQLite database in the local directory
    with the two tables recipes and steps'''

    sqliteConnection = sqlite3.connect(recipe_database)
    cursor = sqliteConnection.cursor()

    table_recipes_query = '''
    CREATE TABLE IF NOT EXISTS recipes
    (
        [recipe_id] INTEGER PRIMARY KEY,
        [title] TEXT,
        [image] BLOB,
        [image_url] TEXT,
        [time_ready] INTEGER,
        [preparation_time] INTEGER,
        [cooking_time] INTEGER,
        [servings] INTEGER,
        [source_name] TEXT,
        [source_url] TEXT,
        [vegan] INTEGER,
        [vegetarian] INTEGER,
        [dairy_free] INTEGER,
        [gluten_free] INTEGER
    )
    '''

    table_steps_query = '''
    CREATE TABLE IF NOT EXISTS steps
    (
        [step_id] INTEGER PRIMARY KEY,
        [step_number] INTEGER,
        [step_description] TEXT,
        [recipe_id] INTEGER NOT NULL
    )
    '''

    table_ingredients_query = '''
    CREATE TABLE IF NOT EXISTS ingredients
    (
        [table_ingredients_id] INTEGER PRIMARY KEY,
        [recipe_id] INTEGER NOT NULL,
        [ingredient_name] TEXT NOT NULL,
        [ingredient_id] INTEGER NOT NULL,
        [amount] REAL,
        [unit] TEXT
    )
    '''

    cursor.execute(table_recipes_query)
    cursor.execute(table_steps_query)
    cursor.execute(table_ingredients_query)

    sqliteConnection.commit()
    sqliteConnection.close()


def call_spoon_API(id:int):
    '''Call spoon API to get information on a recipe ID'''

    params={
    'apiKey':os.environ.get("SPOON_API_KEY"),
    'id':id,
    'includeNutrition':False
    }
    url_steps = f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions"
    response_steps = requests.get(url_steps, params=params)
    json_steps = response_steps.json()

    params={
        'apiKey':os.environ.get("SPOON_API_KEY"),
        'id':id,
        'stepBreakdown':True
    }
    url_info = f"https://api.spoonacular.com/recipes/{id}/information"
    response_info = requests.get(url_info, params=params)
    json_info = response_info.json()

    return json_steps, json_info


def write_recipe_table(id:int, json_info:dict, cursor):
    '''Write a new row to the recipes table'''

    recipe_id = id
    title = json_info['title']
    image_url = json_info['image']
    time_ready = json_info['readyInMinutes']
    preparation_time = json_info['preparationMinutes']
    cooking_time = json_info['cookingMinutes']
    servings = json_info['servings']
    source_name = json_info['sourceName']
    source_url = json_info['sourceUrl']
    vegan = json_info['vegan']
    vegetarian = json_info['vegetarian']
    dairy_free = json_info['dairyFree']
    gluten_free = json_info['glutenFree']

    # retrieve image data from image url
    image_request = requests.get(json_info['image'])
    image = sqlite3.Binary(image_request.content)

    query = '''
    INSERT INTO recipes (recipe_id, title, image, image_url, time_ready,
    preparation_time, servings, cooking_time, source_name, source_url, vegan,
    vegetarian, dairy_free, gluten_free)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(query, (recipe_id, title, image, image_url, time_ready,
                           preparation_time, cooking_time, servings,
                           source_name, source_url, vegan, vegetarian,
                           dairy_free, gluten_free))


def write_ingredients_table(id, json_info, cursor):
    '''Write a new row to the ingredients table'''

    recipe_id = id

    # query current max ingredients_table_id in database
    table_ingredients_id_query = """
    SELECT MAX(table_ingredients_id)
    FROM ingredients
    """
    query_result = cursor.execute(table_ingredients_id_query)
    max_table_ingredients_id = query_result.fetchone()[0]

    # if no entry available in database return cannot be int -> asign int value
    if not isinstance(max_table_ingredients_id, int):
        table_ingredients_id = 0
    else:
        table_ingredients_id = max_table_ingredients_id

    # write ingredients for recipe to ingredients table
    for ingredient in json_info['extendedIngredients']:

        table_ingredients_id += 1
        ingredient_id = ingredient['id']
        ingredient_name = ingredient['name']
        amount = ingredient['amount']
        unit = ingredient['unit']

        query = '''
        INSERT INTO ingredients (table_ingredients_id, recipe_id, ingredient_id,
        ingredient_name, amount, unit)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (table_ingredients_id, recipe_id, ingredient_id,
                               ingredient_name, amount, unit))


def write_steps_table(id, json_steps, cursor):
    '''Write a new row to the steps table'''

    recipe_id = id

    # query current max step_id in database
    max_step_id_query = """
    SELECT MAX(step_id)
    FROM steps
    """
    query_result = cursor.execute(max_step_id_query)
    max_step_id = query_result.fetchone()[0]

    # if no entry available in database return cannot be int -> asign int value
    if not isinstance(max_step_id, int):
        step_id = 0
    else:
        step_id = max_step_id

    # write steps for recipe to step table
    for step in json_steps[0]['steps']:

        step_id += 1
        step_number = step['number']
        step_description = step['step']

        query = '''
        INSERT INTO steps (step_id, step_number, step_description, recipe_id)
        VALUES (?, ?, ?, ?)
        '''
        cursor.execute(query, (step_id, step_number, step_description, recipe_id))


def write_empty_recipe_row(id, json_info, cursor):
    '''Write an empty row to the recipes table where id doesn't exist for spoon API'''

    recipe_id = id
    title = json_info['message']

    query = '''
    INSERT INTO recipes (recipe_id, title)
    VALUES (?, ?)
    '''
    cursor.execute(query, (recipe_id, title))


def new_db_entry_from_spoon_id(
    id:int,
    recipe_database:str=recipe_database
    ):
    '''Create a new database entry in the local sqlite database using spoon API
    given the spoon API id'''

    # connect to local database
    sqliteConnection = sqlite3.connect(recipe_database, isolation_level=None)
    cursor = sqliteConnection.cursor()

    # gather data from spoon API or abort if

    json_steps, json_info = call_spoon_API(id)

    # try to write to local database or abort
    try:
        write_recipe_table(id, json_info, cursor)
        write_ingredients_table(id, json_info, cursor)
        if json_steps: # only write steps if there is any information from spoon API
            write_steps_table(id, json_steps, cursor)

        print(f'Added recipe {json_info["title"]} ✅')

    except Exception as e1:
        try:
            # if error due to invalid id, write empty row
            if json_info['message'] == f'A recipe with the id {id} does not exist.':
                write_empty_recipe_row(id, json_info, cursor)
                print(f'{json_info["message"]}')
                print(f'Added empty row ❌')
            else:
                print(f'Error; json_info={json_info}, json_steps={json_steps} ❌')
        except Exception as e2:
            #print(f'Error; json_info={json_info}, json_steps={json_steps} ❌')
            print(e1)
            print(e2)

    sqliteConnection.close()


def lowest_non_existant_id(
    recipe_database:str=recipe_database
    ):
    '''Retrieve lowest non-existant recipe id from local recipe database'''

    sqliteConnection = sqlite3.connect(recipe_database, isolation_level=None)
    cursor = sqliteConnection.cursor()

    # create a list of touples containing all recipe_id's currently in the database
    recipe_ids_query = """
    SELECT recipe_id
    FROM recipes
    """
    query_result = cursor.execute(recipe_ids_query)
    recipe_ids = query_result.fetchall()

    sqliteConnection.close()

    # change the touple list in a simple list of recipe ids as numbers
    recipe_ids = [x[0] for x in recipe_ids]

    # look for the lowest non-existant id in the recipe_ids list
    lowest_ne_id = next(i for i, e in enumerate(recipe_ids + [ None ], 1) if i != e)

    return lowest_ne_id


def delete_row(id, recipe_database=recipe_database):
    '''Delete row with id number from all tables'''

    sqliteConnection = sqlite3.connect(recipe_database, isolation_level=None)
    cursor = sqliteConnection.cursor()

    for table in ['recipes', 'ingredients', 'steps']:

        deletion_query = f"""
        DELETE FROM {table}
        WHERE recipe_id = {id}
        """
        cursor.execute(deletion_query)

    sqliteConnection.close()


if __name__ == '__main__':
    if not os.path.isfile(recipe_database):
        create_database()
        print('Database created ✅')
    else:
        print('Database exists ✅')
