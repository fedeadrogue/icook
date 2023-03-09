import streamlit as st
from icook.ml_logic.APIs import SpoonAPIcall
from icook.ml_logic.model_roboflow import Recognition
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import requests
import av
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


response = '''
{
    "recipe": [
        {
            "Title": "Torta (Filipino Omelet)",
            "Image": "https://spoonacular.com/recipeImages/663680-556x370.jpg",
            "Shooping list": [
                "garlic cloves",
                "onion",
                "scallions",
                "cilantro",
                "soy sauce"
            ],
            "Unused ingredients": [],
            "Preparation time": 45,
            "steps": [
                [
                    1,
                    "In a medium-heated large skillet, add a little oil and thoroughly cook the meat and potatoes along with soy sauce, garlic and onions. Set aside to cool."
                ],
                [
                    2,
                    "Meanwhile, in a mixing bowl, combine cooled meat mixture with the eggs, tomatoes, cilantro and scallions. Season with salt & pepper and whisk until evenly incorporated."
                ],
                [
                    3,
                    "In the same skillet in medium heat, ladle just enough to form a thin pancake-size patty, one batch at a time. Cook both sides, flipping over after 2-3 minutes. Be careful not to over brown the eggs."
                ],
                [
                    4,
                    "Transfer to a plate, cut in wedges (for bite-size servings) and garnish with cilantro leaves, if you want."
                ]
            ]
        }
    ]
}
'''
response = json.loads(response)

#if upload_image is not None:
#    image = upload_image.read()
#    nparr = np.fromstring(image, np.uint8)
#    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#    cv2_img_resized = cv2.resize(cv2_img, (640,640))
#    cv2.imwrite('icook/img/food_picture.jpg', cv2_img_resized)

#    result=Recognition('icook/img/food_picture.jpg')

    #df = pd.DataFrame({'products':result})
    #json_data = df.to_json()

    #response = requests.post(url="http://localhost:8000/recipes",
    #                         data=json_data,
    #                         headers={"Content-Type": "application/json"})

    #response = response.json()

st.write("Recommended dish according to your ingredients:", response)

title = response['recipe'][0]['Title']
dish_image = response['recipe'][0]['Image']
#ingredients = response['recipe'][0]['']
left_ingredients = response['recipe'][0]['Shooping list']
#instructions =

st.title(f'{title}')
st.write(' ')
st.write('Take a look of your future dish. Looks good!')
st.image(dish_image, width=200, use_column_width=True)
st.write(' ')
st.write('List of ingredients you have:')
#for item in ingredients:
#    st.write(f'• {item}')
st.write(' ')
st.write('List of ingredients you need to buy:')
for item in left_ingredients:
    st.write(f'• {item}')
st.write(' ')
st.write('List of ingredients you need to buy:')
for item in left_ingredients:
    st.write(f'• {item}')
