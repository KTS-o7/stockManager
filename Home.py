import streamlit as st

def app():
    st.title('Home')
    st.write('Welcome to the home page of this multi-page app. This app is meant to demonstrate how to create multi-page apps in Streamlit.')
    st.write('In this app, we will be creating a simple app with three pages: Home, Data, and About.')

def main():
    app()
main()