import os
import requests

def Get_recipies_id(ingredients:str, #list of infgredients separate by coma in only one str not list.
                    number:int=1, # max number of recipies you want to return
                    ):
    '''Return a list ode the .json files with the recipies'''

    url = "https://api.spoonacular.com/recipes/findByIngredients"

    params={
        'apiKey':os.environ.get('SPOON_API_KEY'),
        'ingredients':ingredients,
        'number':number
    }

    return requests.get(url, params=params).json()


def Get_recipies_information(id:list,
                             includeNutrition:bool=False):
    '''return the url of a recipie'''

    url = f"https://api.spoonacular.com/recipes/{id}/information"

    params={
        'apiKey':os.environ.get("SPOON_API_KEY"),
        'id':id,
        'includeNutrition':False
    }
    response=requests.get(url, params=params).json()

    result={
        'image':response['image'], # Picture of the recipie
        'readyInMinutes':response['readyInMinutes'], # preparation time
        'spoonacularSourceUrl':response['spoonacularSourceUrl'] # url link
    }

    return result


def SpoonAPIcall(ingredients:list,
            number:int=1,
            ):
    '''return a list of dicts with the recipie information'''
    ingredients_unique=list(set(ingredients))

    ingredients_str=''
    for ingredient in ingredients_unique:
        if ingredients_str=='':
            ingredients_str= ingredient
        else:
            ingredients_str=ingredients_str + ', ' + ingredient

    response=Get_recipies_id(ingredients_str,number)

    if response!=None:

        result=[]

        for i in range(number):
            shooping_list=[]
            for ingredient in range(response[i]['missedIngredientCount']):
                shooping_list.append(response[i]['missedIngredients'][ingredient]['name'])

            unused_ingredients=[]
            for ingredient in range(len(response[i]['unusedIngredients'])):
                unused_ingredients.append(response[i]['unusedIngredients'][ingredient]['name'])

            information=Get_recipies_information(response[i]['id'])

            recipie={
                'Title':information[i]['title'], # Title of the recipie
                'image':information[i]['image'], # Image of the dish
                'Missed ingredients':len(shooping_list), # Quantity of missing ingredients
                'Shooping llist':shooping_list, # list of the missing ingredients
                'Unused ingredients':unused_ingredients, # list of the unsued ingredients for this recipie
                'Preparation time':information[i]['readyInMinutes'], # time of preparation
                'spoonacularSourceUrl':information[i]['spoonacularSourceUrl'] # Link for all details
            }
            result.append(recipie)

        return result
    else:
        return '0 recipies found'
