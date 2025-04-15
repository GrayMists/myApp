import streamlit as st

st.set_page_config(
    page_title="Salae board",
    page_icon="⚡️",
    layout="wide"
)

import pandas as pd
from streamlit_option_menu import option_menu
import Data

from data_loader import load_data

# Створюємо вибір між сторінками


#with st.sidebar:
selected = option_menu(
    menu_title=None,
    options=["Завантаження", "Дані"],
    icons=["cloud-upload", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)
if selected == "Завантаження":
    # Поле для введення посилання
    sheet_url = st.text_input("Вставте посилання на Google Таблицю:")
    load_button = st.button("Завантажити")
    # Ініціалізуємо порожній DataFrame
    df = pd.DataFrame()

    if selected == "Завантаження":
        if sheet_url and load_button:
            df = load_data(sheet_url)
            if isinstance(df, str):
                st.error(df)
                df = pd.DataFrame()  # Скидаємо df у випадку помилки
            else:
                st.success("Дані успішно завантажені!")
                # Зберігаємо завантажені дані в session_state
                st.session_state.df = df
elif selected == "Дані":
    Data.show_data()
