import os
import requests

def get_recipes_id(ingredients:str, #list of infgredients separate by coma in only one str not list.
                    number:int=1, # max number of recipes you want to return
                    ):
    '''Return a list ode the .json files with the recipes'''

    url = "https://api.spoonacular.com/recipes/findByIngredients"

    params={
        'apiKey':os.environ.get('SPOON_API_KEY'),
        'ingredients':ingredients,
        'number':number
    }

    return requests.get(url, params=params).json()


def get_recipes_information(id:list,
                             includeNutrition:bool=False):
    '''return the imag, the preparation time and the url to the recipe'''

    url = f"https://api.spoonacular.com/recipes/{id}/information"

    params={
        'apiKey':os.environ.get("SPOON_API_KEY"),
        'id':id,
        'includeNutrition':False
    }

    response=requests.get(url, params=params).json()

    result={
        'image':response['image'], # Picture of the recipe
        'readyInMinutes':response['readyInMinutes'], # preparation time
        'spoonacularSourceUrl':response['spoonacularSourceUrl'] # url link
    }

    return result

def get_recipe_steps(id:list,
                     stepBreakdown: bool=True):
    '''Return a list of tuples (number of the step, description)'''

    params={
        'apiKey':os.environ.get("SPOON_API_KEY"),
        'id':id,
        'stepBreakdown':stepBreakdown
    }
    url=f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions"

    response=requests.get(url, params=params).json()

    steps=[]
    for step in range(len(response[0]['steps'])):
        steps.append((response[0]['steps'][step]['number'],response[0]['steps'][step]['step']))

    return steps


def SpoonAPIcall(ingredients:list, # list of ingredients (can be repeating)
                 number:int=1 # max number of recipes you want to return (between 1 and 10)
                 ):
    '''return a list of dicts with the recipe information'''

    # make list unique (no repeated ingredients)
    ingredients_unique=list(set(ingredients))

    # make list into one string separated by ,+
    ingredients_str = ',+'.join(ingredients_unique)

    # call spoon API search by ingredients
    response=get_recipes_id(ingredients_str,number)

    if response!=None:

        recipes=[]

        for i in range(number):
            # get a list of names of all missing and unused ingredients
            shopping_list = [ingredient['name'] for ingredient in response[i]['missedIngredients']]
            unused_list = [ingredient['name'] for ingredient in response[i]['unusedIngredients']]

            # get preparation time and link
            information=get_recipes_information(response[i]['id'])
            steps=get_recipe_steps(response[i]['id'])

            recipe={
                'Title':response[i]['title'], # title of the recipe
                'Image':information['image'], # image of the dish
                'Shooping list':shopping_list, # list of the missing ingredients
                'Unused ingredients':unused_list, # list of the unsued ingredients for this recipe
                'Preparation time':information['readyInMinutes'], # preparation time
                #'spoonacularSourceUrl':information['spoonacularSourceUrl'], # Link for all details
                'steps':steps
            }
            recipes.append(recipe)

        #result={'recipes':recipes}


        return recipes
    else:
        return '0 recipes found'
