import streamlit as st
import SessionState
def app():
    st.set_page_config(layout="wide")
    session_state = SessionState.get(is_authenticated=False, option=None, register=None,username=None,clientName=None)
    if session_state.username is None:
        st.write("Please sign in")
        col1, col2, col3 = st.columns(3)
        col1.metric("Stock Value", "70 $", "1.2%")
        col2.metric("IndexName", "22000", "+8%")
        col3.metric("IndexName2", "56000", "-4%")
    else:
        st.write(f"Welcome, {session_state.clientName}!")

app()