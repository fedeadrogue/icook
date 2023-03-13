import streamlit as st
from icook.ml_logic.model_roboflow import Recognition
import numpy as np
import pandas as pd
import cv2
import requests
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from streamlit.components.v1 import html
import io
import json

st.set_page_config(page_title="iCook", page_icon=":fork_and_knife:")

def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

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

st.write(" ")

if st.button("I have a user"):
    nav_page("app")

with open('config.yaml') as file:
    config = stauth.yaml.load(file, Loader=stauth.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

try:
    if authenticator.register_user("Don't have a user? Create one!", preauthorization=False):
        st.success('User registered successfully')
        nav_page("app")
except Exception as e:
    st.error(e)

with open('config.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)
