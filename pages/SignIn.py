import streamlit as st
import toml
import SessionState
from passlib.hash import bcrypt
import time

def authenticate(username, password):
    # Read usernames and hashed passwords from ./.streamlit/secrets.toml
    secrets = toml.load("./.streamlit/secrets.toml")
    users = secrets.get("users", {})

    # Check if the username exists and the password is correct
    if username in users:
        hashed_password = users[username]
        if bcrypt.verify(password, hashed_password):
            return True
    return False

def register(username, password):
    # Read usernames and hashed passwords from ./.streamlit/secrets.toml
    secrets = toml.load("./.streamlit/secrets.toml")
    users = secrets.get("users", {})

    # Check if the username already exists
    if username in users:
        return False

    # Hash the password and save the new user
    hashed_password = bcrypt.hash(password)
    users[username] = hashed_password

    # Update ./.streamlit/secrets.toml with the new user
    secrets["users"] = users
    with open("./.streamlit/secrets.toml", "w") as f:
        toml.dump(secrets, f)

    return True

def show(session_state: SessionState):
    st.title("Sign In / Register")

   

    # Allow the user to choose between registering and logging in
    if not session_state.option:
        session_state.option = st.button("Sign In")
        session_state.register = st.button("Register")

    if session_state.register:
        st.subheader("Register")
        reg_username = st.text_input("New Username")
        reg_password = st.text_input("New Password", type="password")
        if st.button("Submit Registration"):
            if register(reg_username, reg_password):
                st.success("Registration successful!")
            else:
                st.error("Username already exists!")

    elif session_state.option and not session_state.is_authenticated:
        st.subheader("Log In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Submit Login"):
            if authenticate(username, password):
                session_state.is_authenticated = True
                session_state.username = username
                st.success("You have successfully logged in!")
                with st.spinner("Redirecting..."):
                    time.sleep(5)
                    st.switch_page("./Home.py")
            else:
                st.error("Invalid username or password")
                
     # If the user is already authenticated, show the logout button
    if session_state.is_authenticated:
        if st.button("Logout"):
            session_state.is_authenticated = False
            session_state.username = None
            session_state.option = None
            session_state.register = None
            st.success("You have been logged out!")

# Call the show() function to render the content
session_state = SessionState.get(is_authenticated=False, option=None, register=None,username=None,)
show(session_state)