import os
import sys

from roboflow import Roboflow
import requests

sys.stdout = open(os.devnull, "w")

Spoon_API_KEY = '5cf4d9752bea4c38b962e643ca227e27'
Robo_API_KEY = 'qhSk7QdaM3p1YIzIdrPZ'

rf = Roboflow(api_key=Robo_API_KEY)
project = rf.workspace().project("icook")
model = project.version(1).model

sys.stdout = sys.__stdout__

image = "input_image.jpg"

def Recognition(image):
    '''Object Recognition Model predicts input image, saves output image and returns the list of ingredients'''
    prediction = model.predict(image)

    preds_class = []
    for result in prediction.json()['predictions']:
        preds_class.append(result['class'])

    prediction.save(output_path="output_image.jpg")

    return preds_class


def Get_recipies_id(ingredients:str, #list of infgredients separate by coma in only one str not list.
                    number:int=1, # max number of recipies you want to return
                    ):
    '''Return a list ode the .json files with the recipies'''

    url = "https://api.spoonacular.com/recipes/findByIngredients"

    params={
        'apiKey':Spoon_API_KEY,
        'ingredients':ingredients,
        'number':number
    }

    return requests.get(url, params=params).json()


def Get_recipies_information(id:list,
                             includeNutrition:bool=False):
    '''return the url of a recipie'''

    url = f"https://api.spoonacular.com/recipes/{id}/information"

    params={
        'apiKey':Spoon_API_KEY,
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

    result=[]
    for i in range(number):
        information=Get_recipies_information(response[i]['id'])
        result.append((response[i]['title'],information))

    return result

result = SpoonAPIcall(Recognition(image))

print("Recomended Dish:", result[0][0])
print("Dish Recipe:", result[0][1])
