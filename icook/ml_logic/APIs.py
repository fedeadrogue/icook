import os
import requests
from icook.recipe_database.database_search import ids_by_ingredients, db_id_query_to_spoon_format, query_by_id

def get_recipes_id(ingredients:str, #list of infgredients separate by coma in only one str not list.
                    number:int=2, # max number of recipes you want to return
                    ):
    '''Return a list of the .json files with the recipes'''

    url = "https://api.spoonacular.com/recipes/findByIngredients"

    SPOON_API_KEY=[
        'SPOON_API_KEY_R',
        'SPOON_API_KEY_F',
        'SPOON_API_KEY_A',
        'SPOON_API_KEY_L',
        'SPOON_API_KEY_F2'
    ]

    for key in SPOON_API_KEY:

        params={
            'apiKey':os.environ.get(key),
            'ingredients':ingredients,
            'number':number
        }

        response=requests.get(url, params=params).json()

        if type(response)!=list and 'status' in response.keys():
            pass
        else:
            return response

    # look in the local db
    print('Accessing the local database for ingredient information')
    id_list = ids_by_ingredients(ingredients, number)
    if id_list:
        return id_list
    else:
        return 'All keys over'


def get_recipe_information(id:int,
                            ingredients:str,
                            includeNutrition:bool=False):
    '''return the image, the preparation time and the url to the recipe'''

    # first query the local database
    recipe_info = query_by_id(id)
    if recipe_info['recipes']:
        print('Accessing the local database for recipe information')
        result = db_id_query_to_spoon_format(recipe_info, ingredients, info_only=True)
        return result

    # if id is not in local database, call spoon api
    print('Accessing the spoon database for recipe information')
    url = f"https://api.spoonacular.com/recipes/{id}/information"

    SPOON_API_KEY=[
        'SPOON_API_KEY_R',
        'SPOON_API_KEY_F',
        'SPOON_API_KEY_A',
        'SPOON_API_KEY_L',
        'SPOON_API_KEY_F2'
    ]

    for key in SPOON_API_KEY:

        params={
            'apiKey':os.environ.get(key),
            'id':id,
            'includeNutrition':False
        }

        response=requests.get(url, params=params).json()

        if type(response)!=list and 'status' in response.keys():
            pass
        else:
            result={
                'image':response['image'], # Picture of the recipe
                'readyInMinutes':response['readyInMinutes'], # preparation time
                'spoonacularSourceUrl':response['spoonacularSourceUrl'] # url link
            }

            return result

    result={
                'image':'All keys over', # Picture of the recipe
                'readyInMinutes':'All keys over', # preparation time
                'spoonacularSourceUrl':'All keys over' # url link
            }

    return result

def get_recipe_steps(id:int,
                     ingredients:str,
                     stepBreakdown: bool=True):
    '''Return a list of tuples (number of the step, description)'''

    # first query the local database
    recipe_info = query_by_id(id)
    if recipe_info['recipes']:
        print('Accessing the local database for instruction information')
        response = db_id_query_to_spoon_format(recipe_info, ingredients, steps_only=True)
        steps=[]
        for step in range(len(response[0]['steps'])):
            steps.append((response[0]['steps'][step]['number'],response[0]['steps'][step]['step']))
        return steps

    # if id is not in local database, call spoon api
    print('Accessing the spoon database for instruction information')
    url=f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions"

    SPOON_API_KEY=[
        'SPOON_API_KEY_R',
        'SPOON_API_KEY_F',
        'SPOON_API_KEY_A',
        'SPOON_API_KEY_L',
        'SPOON_API_KEY_F2'
    ]

    for key in SPOON_API_KEY:

        params={
            'apiKey':os.environ.get(key),
            'id':id,
            'stepBreakdown':stepBreakdown
        }

        response=requests.get(url, params=params).json()
        if response==[]:
            return [(0,'No steps needed')]

        if type(response)!=list and 'status' in response.keys():
            pass
        else:
            steps=[]
            for step in range(len(response[0]['steps'])):
                steps.append((response[0]['steps'][step]['number'],response[0]['steps'][step]['step']))

            return steps

    return [(0,'All keys over')]


def SpoonAPIcall(ingredients:list, # list of ingredients (can be repeating)
                 number:int=2 # max number of recipes you want to return (between 1 and 10)
                 ):
    '''return a list of dicts with the recipe information'''

    # make list unique (no repeated ingredients)
    ingredients_unique = list(set(ingredients))

    # make list into one string separated by ,+
    ingredients_str = ',+'.join(ingredients_unique)

    # call spoon API search by ingredients
    response = get_recipes_id(ingredients_str,number)
    if response == 'All keys over':
        return 'All keys over'
    elif response != None and response != 'All keys over':
        recipes=[]

        # if response is from spoon api
        if type(response[0]) is dict:
            for i in range(len(response)):

                # get a list of names of all missing and unused ingredients
                shopping_list = [(ingredient['name'],ingredient['amount'],ingredient['unit']) for ingredient in response[i]['missedIngredients']]
                unused_list = [(ingredient['name'],ingredient['amount'],ingredient['unit']) for ingredient in response[i]['unusedIngredients']]

                # get preparation time and link
                information=get_recipe_information(response[i]['id'], ingredients_str)
                steps=get_recipe_steps(response[i]['id'], ingredients_str)

                recipe={
                    'ID':response[i]['id'], # recipe id
                    'Title':response[i]['title'], # title of the recipe
                    'Image':information['image'], # image of the dish
                    'Picture ingredients':ingredients_unique, # list of ingredients find in the picture
                    'Shopping list':shopping_list, # list of tuples with the missing ingredients, quantities and units
                    'Unused ingredients':unused_list, # list of the unsued ingredients for this recipe
                    'Preparation time':information['readyInMinutes'], # preparation time
                    #'spoonacularSourceUrl':information['spoonacularSourceUrl'], # Link for all details
                    'steps':steps# List of tuples (step number, description)
                }
                recipes.append(recipe)

            return recipes

        # if response is from local query
        else:
            for i in range(len(response)):
                recipe_info = query_by_id(response[i])
                steps, information = db_id_query_to_spoon_format(recipe_info, ingredients_str)

                # get a list of names of all missing and unused ingredients
                shopping_list = [(ingredient['name'],ingredient['amount'],ingredient['unit']) for ingredient in information['missedIngredients']]
                unused_list = [(ingredient['name'],ingredient['amount'],ingredient['unit']) for ingredient in information['unusedIngredients']]


                recipe={
                    'ID':information['id'], # recipe id
                    'Title':information['title'], # title of the recipe
                    'Image':information['image'], # image of the dish
                    'Picture ingredients':ingredients_unique, # list of ingredients find in the picture
                    'Shopping list':shopping_list, # list of tuples with the missing ingredients, quantities and units
                    'Unused ingredients':unused_list, # list of the unsued ingredients for this recipe
                    'Preparation time':information['readyInMinutes'], # preparation time
                    #'spoonacularSourceUrl':information['spoonacularSourceUrl'], # Link for all details
                    'steps':steps# List of tuples (step number, description)
                }
                recipes.append(recipe)
            return recipes

    else:
        return '0 recipes found'
