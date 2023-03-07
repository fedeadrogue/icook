import os
import sys
from roboflow import Roboflow
import streamlit as st
from PIL import Image
import requests
import io

sys.stdout = open(os.devnull, "w")

Spoon_API_KEY = '5cf4d9752bea4c38b962e643ca227e27'
Robo_API_KEY = 'qhSk7QdaM3p1YIzIdrPZ'

rf = Roboflow(api_key=Robo_API_KEY)
project = rf.workspace().project("icook")
model = project.version(3).model

sys.stdout = sys.__stdout__
url = "http://localhost:8501/"
session = requests.Session()
session.request('POST', url,timeout=60)

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


def SpoonAPIcall(ingredients:list,
            number:int=1,
            ):
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
            information=Get_recipies_information(response[i]['id'])
            result.append((response[i]['title'],information))

        return result
    else:
        print('0 recipies found')
