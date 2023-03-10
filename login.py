import streamlit as st
import app
from PIL import Image

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
st.write("Gone are the days of staring blankly at your fridge and wondering what you could possibly whip up for dinner.")
st.write("With iCook, all you need to do is snap a photo of the items you have on hand, and the app's advanced AI algorithms will do the rest, quickly identifying each item and giving you an instant list of recipe options to choose from.")
st.write(" ")

login_form = st.form("login_form")

# Get the list of users and passwords from secrets.toml
users = st.secrets["users"]

with login_form:
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    # Add a submit button to the form
    submit_button = st.form_submit_button(label="Login")

# Check if the submit button has been clicked and the credentials match
for u in users:
    if submit_button and user == u["username"] and pwd == u["password"]:
        # If the credentials match, set authenticated to True
        authenticated = True
        break
else:
    # If the credentials don't match, set authenticated to False
    authenticated = False

if authenticated:
    # Run your main application if the credentials match
    app.run()
else:
    if submit_button:
        st.error("Invalid username or password")
