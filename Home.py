import streamlit as st
import SessionState
def app():
    session_state = SessionState.get(is_authenticated=False, option=None, register=None,username=None,)
    if session_state.username is None:
        st.write("Please sign in")
    else:
        st.write(f"Welcome, {session_state.username}!")

app()