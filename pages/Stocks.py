import streamlit as st 
import SessionState

def show(session_state: SessionState):
    if not session_state.is_authenticated:
        st.error("You must be logged in to access this page.")
        return

    st.title("Portfolio Management")
    st.title("Stocks")
    st.write("Welcome to the Stocks page")
    st.write("This is a secure page")
    st.write("You can only access this page if you are signed in")
    st.write("You can sign in by going to the Sign In page")
    st.write("You can sign out by going to the Sign Out page")
    
session_state = SessionState.get()
show(session_state)