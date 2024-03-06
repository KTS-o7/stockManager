import streamlit as st

def app():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if username == st.secrets["users"]["username"] and password == st.secrets["users"]["password"]:
            st.session_state.user = username
            st.success("Signed in successfully")
        else:
            st.error("Incorrect username or password")
app()