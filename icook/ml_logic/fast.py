from fastapi import FastAPI
from typing import Any, Dict
import pandas as pd
from icook.ml_logic.APIs import SpoonAPIcall
from icook.ml_logic.model_roboflow import Recognition

app = FastAPI()

@app.get('/')
def index():
    return {'Running': True}

@app.get('/recipe')
def index(data: Dict[str,Any]):
    result=SpoonAPIcall(Recognition(data['impage path']))
    return result
