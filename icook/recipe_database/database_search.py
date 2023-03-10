import sqlite3

recipe_database = 'recipe_sqlite.db'

def query_by_id(id, recipe_database:str=recipe_database):
    '''Queries local SQLite recipe database by id'''

    sqliteConnection = sqlite3.connect(recipe_database)
    cursor = sqliteConnection.cursor()

    table_return = {}

    for table in ['recipes', 'ingredients', 'steps']:
        table_id_query = f'''
        SELECT *
        FROM {table}
        WHERE recipe_id = {id}
        '''

        query_result = cursor.execute(table_id_query)
        table_return[f'{table}'] = query_result.fetchall()

    sqliteConnection.commit()
    sqliteConnection.close()
    return table_return

def db_id_query_to_spoon_format(id_query_return):
    '''Format local database return format to match the return format from
    spoon API'''

    # format return from recipes table
    keys_json_info = ('id', 'title', 'image_file', 'image', 'readyInMinutes',
    'preparationMinutes', 'cookingMinutes', 'servings', 'sourceName', 'sourceUrl',
    'vegan', 'vegetarian', 'dairyFree', 'glutenFree')
    json_info = dict((k, v) for k,v in zip(keys_json_info, id_query_return['recipes'][0]))

    # format return from ingredients table
    extendedIngredients = []
    keys_extendedIngredients = ('table_ingredients_id', 'recipe_id', 'name', 'id',
                                'amount', 'unit')
    for ingredient in id_query_return['ingredients']:
        extendedIngredients.append((dict((k, v) for k,v in zip(keys_extendedIngredients, ingredient))))
    json_info['extendedIngredients'] = extendedIngredients

    # format return from steps table
    steps = []
    keys_steps = ('step_id', 'number', 'step', 'recipe_id')
    for step in id_query_return['steps']:
        steps.append((dict((k, v) for k,v in zip(keys_steps, step))))
    json_steps = [{'name':'', 'steps':steps}]

    return json_steps, json_info
