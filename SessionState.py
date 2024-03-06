import streamlit as st

class _SessionState:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

def get(**kwargs):
    if not hasattr(st, '_session_state'):
        st._session_state = _SessionState(**kwargs)
    return st._session_state
