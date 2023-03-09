from fastapi import FastAPI
from typing import Any, Dict
from icook.ml_logic.APIs import SpoonAPIcall
from icook.ml_logic.model_roboflow import Recognition
from icook.registry import load_model

app = FastAPI()
# model=load_model()

@app.get('/')
def index():
    return {'Running': True}

@app.post('/recipes')
def index(data: Dict[str,Any]):
    products = list(data['products'].values())
    recipies = SpoonAPIcall(products)
    return {'recipe':recipies}

# @app.post('/recognition')
# def prediction(data:Dict[str,Any]):
#     image_path=data.path
#     products=model.predict(image_path) # check if it is right
#     return products
