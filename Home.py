import streamlit as st

def app():
    if "user" not in st.session_state:
        st.write("Please sign in")
    else:
        st.write(f"Welcome, {st.session_state.user}!")

app()