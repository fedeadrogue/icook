import streamlit as st
from icook.ml_logic.APIs import SpoonAPIcall
from icook.ml_logic.model_roboflow import Recognition
import numpy as np
import pandas as pd
import cv2
import requests

st.set_page_config(page_title="iCook", page_icon=":fork_and_knife:")

st.title("iCook")

upload_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if upload_image is not None:
    image = upload_image.read()
    nparr = np.fromstring(image, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2_img_resized = cv2.resize(cv2_img, (640,640))
    cv2.imwrite('test.jpg', cv2_img_resized)

    # df = pd.DataFrame({'path':['test.jpg']})
    # json_data = df.to_json()
    # result=requests.post(url="http://localhost:8000/recognition", data=json_data, headers={"Content-Type": "application/json"})

    result=Recognition('test.jpg')

    df = pd.DataFrame({'products':result})
    json_data = df.to_json()

    response = requests.post(url="http://localhost:8000/recipes", data=json_data, headers={"Content-Type": "application/json"})

    st.write("Predicted Ingredients:", response.json())

    # if results:
    #     st.write("Recommended Dish:", results[0][0])
    #     st.write("Dish Recipe:", results[0][1])
    # else:
    #     st.write("No recipes found for the given ingredients.")
