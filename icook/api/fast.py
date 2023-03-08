from fastapi import FastAPI
from typing import Any, Dict
import pandas as pd
from icook.ml_logic.APIs import SpoonAPIcall
from icook.ml_logic.model_roboflow import Recognition

app = FastAPI()

@app.get('/')
def index():
    return {'Running': True}

@app.post('/recipes')
def index(data: Dict[str,Any]):
    products = list(data['products'].values())
    recipies = SpoonAPIcall(products)
    return {'recipe':recipies}

@app.post('/recognition')
def prediction(data:Dict[str,Any]):
    image_path=data.path
    products=Recognition(image_path)
    return products
