import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_processing import (
    get_session_dataframe, 
    prepare_filtered_data)

from data_cleaner import change_district_name



def show_data():
    st.write("Hello")