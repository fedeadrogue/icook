import requests
import os

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

    return response['spoonacularSourceUrl']


def SpoonAPIcall(ingredients:list, #list of infgredients
            number:int=1, # max number of recipies you want to return
            ):
    '''Return a list of tuples (title of the recipie, url)'''
    ingredients_unique=list(set(ingredients))

    ingredients_str=''
    for ingredient in ingredients_unique:
        if ingredients_str=='':
            ingredients_str= ingredient
        else:
            ingredients_str=ingredients_str + ', ' + ingredient

    ingredients_str

    response=Get_recipies_id(ingredients_str,number)
    if response!=None:
        result=[]
        for i in range(number):
            information=Get_recipies_information(response[i]['id'])
            result.append((response[i]['title'],information))

        return result
    else:
        print('0 recipies found')
