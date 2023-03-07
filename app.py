import streamlit as st
from PIL import Image
import tempfile
from API_Roboflow_Spoonacular import SpoonAPIcall, Recognition
import numpy as np
import cv2
st.set_page_config(page_title="iCook", page_icon=":fork_and_knife:")

st.title("iCook")

upload_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if upload_image is not None:
    image = upload_image.read()
    nparr = np.fromstring(image, np.uint8)
    cv2_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2_img_resized = cv2.resize(cv2_img, (640,640))
    cv2.imwrite('test.jpg', cv2_img_resized)

    preds_class = Recognition('test.jpg')

    st.write("Predicted Ingredients:", preds_class)

    results = SpoonAPIcall(preds_class)

    if results:
        st.write("Recommended Dish:", results[0][0])
        st.write("Dish Recipe:", results[0][1])
    else:
        st.write("No recipes found for the given ingredients.")
