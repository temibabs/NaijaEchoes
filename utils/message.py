import streamlit as st


def reset_messages():
    st.session_state.pop("messages", [])
