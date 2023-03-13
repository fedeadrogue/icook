import sqlite3

recipe_database = 'recipe_sqlite.db'

def query_by_id(id:int, recipe_database:str=recipe_database):
    '''Queries local SQLite recipe database by id'''

    sqliteConnection = sqlite3.connect(recipe_database)
    cursor = sqliteConnection.cursor()

    recipe = {}

    for table in ['recipes', 'ingredients', 'steps']:
        table_id_query = f'''
        SELECT *
        FROM {table}
        WHERE recipe_id = {id}
        '''

        query_result = cursor.execute(table_id_query)
        recipe[f'{table}'] = query_result.fetchall()

    sqliteConnection.commit()
    sqliteConnection.close()
    return recipe


def missing_unused_ingredients(recipe:dict, ingredients:str):
    '''Queries local database by ingredients taking the recipe dictionary and a
    string of ingredients separated by ,+. Returns two lists, one of missing
    ingredients and one of unused ingredients'''

    # make input string all lower case
    ingredients = ingredients.lower()

    # turn input string into list of ingredients
    ingredient_available = ingredients.split(',+')

    # add information on all missing ingredients (i.e. ingredients not available)
    missing_ingredients = []
    for ingredient in recipe['ingredients']:
        if ingredient[2] not in ingredient_available:
            keys_missing = ('table_ingredients_id', 'recipe_id', 'name', 'id', 'amount', 'unit')
            missing_info = dict((k, v) for k,v in zip(keys_missing, ingredient))
            missing_ingredients.append(missing_info)

    # add information on all unused ingredients (empty string for amound and unit)
    ingredient_names = [x[2] for x in recipe['ingredients']]
    unused_ingredients_names = [x for x in ingredient_available if x not in ingredient_names]
    unused_ingredients = [{'name':x, 'amount':'', 'unit':''} for x in unused_ingredients_names]

    return missing_ingredients, unused_ingredients


def db_id_query_to_spoon_format(query_by_id_return:dict, ingredients:str):
    '''Format local database return and a string of available ingredients separated by ,+
    to match the return format from spoon API'''

    # format return from recipes table
    keys_json_info = ('id', 'title', 'image_file', 'image', 'readyInMinutes',
    'preparationMinutes', 'cookingMinutes', 'servings', 'sourceName', 'sourceUrl',
    'vegan', 'vegetarian', 'dairyFree', 'glutenFree')
    json_info = dict((k, v) for k,v in zip(keys_json_info, query_by_id_return['recipes'][0]))

    # format return from ingredients table
    extendedIngredients = []
    keys_extendedIngredients = ('table_ingredients_id', 'recipe_id', 'name', 'id',
                                'amount', 'unit')
    for ingredient in query_by_id_return['ingredients']:
        extendedIngredients.append((dict((k, v) for k,v in zip(keys_extendedIngredients, ingredient))))
    json_info['extendedIngredients'] = extendedIngredients

    # format return from steps table
    steps = []
    keys_steps = ('step_id', 'number', 'step', 'recipe_id')
    for step in query_by_id_return['steps']:
        steps.append((dict((k, v) for k,v in zip(keys_steps, step))))
    json_steps = [{'name':'', 'steps':steps}]

    # add info on missing and unused ingredients
    missing_ingredients, unused_ingredients = missing_unused_ingredients(query_by_id_return, ingredients)
    json_info['missedIngredients'] = missing_ingredients
    json_info['unusedIngredients'] = unused_ingredients

    return json_steps, json_info


def ids_by_ingredients(ingredients:str, recipe_number:int):
    '''Queries local database by ingredients taking a string of ingredients
    separated by ,+ . Returns recipe_number recipe ids as a list'''

    # make input string all lower case
    ingredients = ingredients.lower()

    # turn input string into list of ingredients
    ingredient_list = ingredients.split(',+')

    # connect to local database
    sqliteConnection = sqlite3.connect(recipe_database)
    cursor = sqliteConnection.cursor()

    # create a list of recipe_id's that contain the input ingredients
    id_list = []
    for ingredient in ingredient_list:
        ingredients_query = f'''
        Select recipe_id
        FROM ingredients
        WHERE LOWER(ingredient_name) LIKE '%{ingredient}%'
        '''

        query_result = cursor.execute(ingredients_query)
        # transform the result to a list and drop duplicates within the same recipe
        unique_ids = list(set([x[0] for x in query_result.fetchall()]))
        id_list.append(unique_ids)

    # count recipes that contain ingredients
    count_dict = {}
    for recipe in id_list:
        for id in recipe:
            if id in count_dict.keys():
                count_dict[id] += 1
            else:
                count_dict[id] = 1

    # sort list by ingredient occurance
    ids_by_ingredient_occurance = sorted(count_dict, key=count_dict.get, reverse=True)

    # ensure to only return recipes that have steps associated with them
    steps_query = f'''
    SELECT DISTINCT recipe_id
    FROM steps
    '''
    query_result = cursor.execute(steps_query)
    recipes_with_steps = [x[0] for x in query_result.fetchall()]
    ids_by_ingredient_occurance = [x for x in ids_by_ingredient_occurance if x in recipes_with_steps]

    # sever connection to local database
    sqliteConnection.close()

    # return only as many recipes as specified
    ids_by_ingredient_occurance = ids_by_ingredient_occurance[:recipe_number]

    return ids_by_ingredient_occurance
