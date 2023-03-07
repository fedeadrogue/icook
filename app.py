import os
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from script import *

st.title("Ingredients for Recipes")

# Load image
file = st.file_uploader("Upload image at the ingredients", type=["jpg", "jpeg", "png"])

if file is not None:
    # Show imagen
    image = Image.open(BytesIO(file.read()))
    st.image(image, caption='Image at the ingredients', use_column_width=True)

    #Predict ingredients and get recipes
    preds_class = Recognition(image)
    result = SpoonAPIcall(preds_class, 1)

    #Show the recommended recipe
    st.subheader("Receta Recomendada:")
    st.write(result[0][0])
    st.write(result[0][1])
