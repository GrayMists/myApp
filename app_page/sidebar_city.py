import streamlit as st

df = st.session_state.df
def show_sidebar_data():
    with st.container(border=True):
        st.write("В подальшому тут будуть фільтри")