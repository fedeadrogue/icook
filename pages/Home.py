import streamlit as st
from icook.ml_logic.model_roboflow import Recognition
import numpy as np
import pandas as pd
import cv2
import requests
from PIL import Image
import streamlit_authenticator as stauth
import yaml
import io
import json
from icook.recipe_database.database_streamlit import add_recipe, get_recipes

st.set_page_config(page_title="iCook", page_icon=":fork_and_knife:")

logo = Image.open('icook/img/logo.png')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')
with col2:
    st.image(logo, use_column_width=True)
with col3:
    st.write(' ')

st.title("Feeling hungry?")
st.write(' ')
st.write("Gone are the days of staring blankly at your fridge and wondering what you could possibly whip up for dinner.")
st.write("With iCook, all you need to do is snap a photo of the items you have on hand, and the app's advanced AI algorithms will do the rest, quickly identifying each item and giving you an instant list of recipe options to choose from.")

with open('config.yaml') as file:
    config = stauth.yaml.load(file, Loader=stauth.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Let's cook 👨‍🍳", "main")

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')

    st.write(" ")
    st.title("Welcome again Chef, let's cook something...")

    # Initialize session state to store saved recipes
    if "saved_recipes" not in st.session_state:
        st.session_state.saved_recipes = []

    upload_image = st.camera_input("Take a picture of your food! 📷")

    if upload_image is not None:
        image = upload_image.read()
        nparr = np.fromstring(image, np.uint8)
        cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2_img_resized = cv2.resize(cv2_img, (640,640))

        cv2.imwrite('icook/img/food_picture.jpg', cv2_img_resized)

        result=Recognition('icook/img/food_picture.jpg')
        if result==[]:
            st.write('No recognized ingredients')
        else:
            df = pd.DataFrame({'products':result})
            json_data = df.to_json()

            # # API call to the docker in the cloud
            # response = requests.post(url="https://icook-6hyjqqtjpq-ew.a.run.app/recipes",
            #                          data=json_data,
            #                          headers={"Content-Type": "application/json"})

            # api call in local

            response = requests.post(url="http://localhost:8000/recipes",
                                    data=json_data,
                                    headers={"Content-Type": "application/json"})
            response = response.json()
            if response==0:
                st.write('API key error: probably you spend all the free calls on spoon')
            else:
                st.write(' ')
                st.write("<h1 style='font-size: 24px; font-weight: bold;'>We have two recommendations according to your ingredients...</h1>", unsafe_allow_html=True)

                dishes = ["Choose a Dish 🍳", response['recipe'][0]['Title'], response['recipe'][1]['Title']]
                select_dish = st.selectbox("Now it's your turn!", dishes, index=0)

                #First Recipe
                if select_dish == response['recipe'][0]['Title']:

                    title = response['recipe'][0]['Title']
                    recipe_id = response['recipe'][0]['ID']
                    dish_image = response['recipe'][0]['Image']
                    ingredients = response['recipe'][0]['Picture ingredients']
                    left_ingredients = [x[0] for x in response['recipe'][0]['Shopping list']]
                    num_left_ingredients = [x[1] for x in response['recipe'][0]['Shopping list']]
                    amount_left_ingredients = [x[2] for x in response['recipe'][0]['Shopping list']]
                    instructions = response['recipe'][0]['steps']

                    st.write(' ')
                    st.title(f'{title}')
                    st.write(' ')

                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>Take a look of your future dish. Looks good! 🤤</h1>", unsafe_allow_html=True)
                    st.image(dish_image, width=200, use_column_width=True)
                    st.write(' ')

                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>✅ List of ingredients you have:</h1>", unsafe_allow_html=True)
                    for item in ingredients:
                        st.write(f'• {item}')
                    st.write(' ')

                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>🛒 List of ingredients you need to buy:</h1>", unsafe_allow_html=True)
                    for item, num, amount in zip(left_ingredients, num_left_ingredients, amount_left_ingredients):
                        st.write(f'• {item}: {num} {amount}')
                    st.write(' ')

                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>🔪 How to prepare your dish:</h1>", unsafe_allow_html=True)
                    for number, instr in instructions:
                        st.write(f'{number}) {instr}')

                    # Display button to save recipe
                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>⭐ Did you like the recipe? Save it for later!</h1>", unsafe_allow_html=True)
                    if st.button("Save Recipe"):
                        add_recipe(st.session_state['name'] , recipe_id)
                        if title not in st.session_state["saved_recipes"]:
                            st.session_state["saved_recipes"].append(title)
                            st.success(f"{title} added to saved recipes!")
                        else:
                            st.warning(f"{title} already exists in saved recipes!")

                #Second Recipe
                elif select_dish == response['recipe'][1]['Title']:

                    title = response['recipe'][1]['Title']
                    recipe_id = response['recipe'][0]['ID']
                    dish_image = response['recipe'][1]['Image']
                    ingredients = response['recipe'][1]['Picture ingredients']
                    left_ingredients = [x[0] for x in response['recipe'][1]['Shopping list']]
                    num_left_ingredients = [x[1] for x in response['recipe'][1]['Shopping list']]
                    amount_left_ingredients = [x[2] for x in response['recipe'][1]['Shopping list']]
                    instructions = response['recipe'][1]['steps']

                    st.write(' ')
                    st.write(' ')
                    st.title(f'{title}')
                    st.write(' ')

                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>Take a look of your future dish. Looks good! 🤤</h1>", unsafe_allow_html=True)
                    st.image(dish_image, width=200, use_column_width=True)
                    st.write(' ')

                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>✅ List of ingredients you have:</h1>", unsafe_allow_html=True)
                    for item in ingredients:
                        st.write(f'• {item}')
                    st.write(' ')

                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>🛒 List of ingredients you need to buy:</h1>", unsafe_allow_html=True)
                    for item, num, amount in zip(left_ingredients, num_left_ingredients, amount_left_ingredients):
                        st.write(f'• {item}: {num} {amount}')
                    st.write(' ')

                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>🔪 How to prepare your dish:</h1>", unsafe_allow_html=True)
                    for number, instr in instructions:
                        st.write(f'{number}) {instr}')

                    # Display button to save recipe
                    st.write("<h1 style='font-size: 20px; font-weight: bold;'>⭐ Did you like the recipe? Save it for later!</h1>", unsafe_allow_html=True)
                    if st.button("Save Recipe"):
                        add_recipe(st.session_state['name'] , recipe_id)
                        if title not in st.session_state["saved_recipes"]:
                            st.session_state["saved_recipes"].append(title)
                            st.success(f"{title} added to saved recipes!")
                        else:
                            st.warning(f"{title} already exists in saved recipes!")

    # Display list of saved recipes
    st.write(' ')
    st.write("<h1 style='font-size: 20px; font-weight: bold;'>🍽️ Your Saved Recipes:</h1>", unsafe_allow_html=True)
    if st.button("View Saved Recipes"):
        recipies = get_recipes(st.session_state['name'])
        recipies = list(set(recipies))
        st.write(recipies)

        #if len(st.session_state["saved_recipes"]) == 0:
        #    st.write("<h1 style='font-size: 20px; font-weight: bold;'>No recipes saved ☹️ </h1>", unsafe_allow_html=True)
        #else:
        #    st.write("<h1 style='font-size: 20px; font-weight: bold;'>⭐ Your Recipes:</h1>", unsafe_allow_html=True)
           # for i, recipe in enumerate(st.session_state["saved_recipes"]):
               # st.write(f"{i+1}. {recipe}")

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
