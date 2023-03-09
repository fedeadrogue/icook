import streamlit as st
from icook.ml_logic.APIs import SpoonAPIcall
from icook.ml_logic.model_roboflow import Recognition
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import requests
import io
import json

st.set_page_config(page_title="iCook", page_icon=":fork_and_knife:")

logo = Image.open('icook/img/logo.png')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image(logo, width=200, use_column_width=True)
with col3:
    st.write(' ')

st.write("Gone are the days of staring blankly at your ingredients and wondering what you could possibly whip up for dinner.")
st.write("With iCook, all you need to do is snap a photo of the items you have on hand, and the app's advanced AI algorithms will do the rest, quickly identifying each item and giving you an instant list of recipe options to choose from.")

upload_image = st.camera_input("Take a picture of your food!")

if upload_image is not None:
    image = upload_image.read()
    nparr = np.fromstring(image, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2_img_resized = cv2.resize(cv2_img, (640,640))
    cv2.imwrite('icook/img/food_picture.jpg', cv2_img_resized)

    result=Recognition('icook/img/food_picture.jpg')

    df = pd.DataFrame({'products':result})
    json_data = df.to_json()

    response = requests.post(url="http://localhost:8000/recipes",
                             data=json_data,
                             headers={"Content-Type": "application/json"})

    response = response.json()

    st.write(' ')
    st.write("<h1 style='font-size: 24px; font-weight: bold;'>We have two recommendations according to your ingredients...</h1>", unsafe_allow_html=True)

    dishes = ["Choose a Dish", response['recipe'][0]['Title'], response['recipe'][1]['Title']]
    select_dish = st.selectbox("Now it's your turn!", dishes, index=0)

    #First Recipe
    if select_dish == response['recipe'][0]['Title']:

        title = response['recipe'][0]['Title']
        dish_image = response['recipe'][0]['Image']
        ingredients = response['recipe'][0]['Picture ingredients']
        left_ingredients = response['recipe'][0]['Shooping list']
        instructions = response['recipe'][0]['steps']

        st.write(' ')
        st.title(f'{title}')
        st.write(' ')

        st.write("<h1 style='font-size: 20px; font-weight: bold;'>Take a look of your future dish. Looks good!</h1>", unsafe_allow_html=True)
        st.image(dish_image, width=200, use_column_width=True)
        st.write(' ')

        st.write("<h1 style='font-size: 20px; font-weight: bold;'>List of ingredients you have:</h1>", unsafe_allow_html=True)
        for item in ingredients:
            st.write(f'• {item}')
        st.write(' ')

        st.write("<h1 style='font-size: 20px; font-weight: bold;'>List of ingredients you need to buy:</h1>", unsafe_allow_html=True)
        for item in left_ingredients:
            st.write(f'• {item}')
        st.write(' ')

        st.write("<h1 style='font-size: 20px; font-weight: bold;'>How to prepare your dish:</h1>", unsafe_allow_html=True)
        for number, instr in instructions:
            st.write(f'{number}) {instr}')

    #Second Recipe
    elif select_dish == response['recipe'][1]['Title']:

        title = response['recipe'][1]['Title']
        dish_image = response['recipe'][1]['Image']
        ingredients = response['recipe'][1]['Picture ingredients']
        left_ingredients = response['recipe'][1]['Shooping list']
        instructions = response['recipe'][1]['steps']

        st.write(' ')
        st.write(' ')
        st.title(f'{title}')
        st.write(' ')

        st.write("<h1 style='font-size: 20px; font-weight: bold;'>Take a look of your future dish. Looks good!</h1>", unsafe_allow_html=True)
        st.image(dish_image, width=200, use_column_width=True)
        st.write(' ')

        st.write("<h1 style='font-size: 20px; font-weight: bold;'>List of ingredients you have:</h1>", unsafe_allow_html=True)
        for item in ingredients:
            st.write(f'• {item}')
        st.write(' ')

        st.write("<h1 style='font-size: 20px; font-weight: bold;'>List of ingredients you need to buy:</h1>", unsafe_allow_html=True)
        for item in left_ingredients:
            st.write(f'• {item}')
        st.write(' ')

        st.write("<h1 style='font-size: 20px; font-weight: bold;'>How to prepare your dish:</h1>", unsafe_allow_html=True)
        for number, instr in instructions:
            st.write(f'{number}) {instr}')
