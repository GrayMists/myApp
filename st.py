import streamlit as st

st.set_page_config(
    page_title="Salae board",
    page_icon="⚡️",
    layout="wide"
)

import pandas as pd
from streamlit_option_menu import option_menu
import app_page.region_page as rerion_page
import app_page.city_page as city_page

from data_loader import load_data

with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Завантаження", "Регіони", "Місто"],
        icons=["cloud-upload","back" ,"bar-chart"],
        menu_icon="cast",
        default_index=0,
        #orientation="horizontal",
        key="main_menu" 
    )

    if selected == "Завантаження":
        sheet_url = st.text_input("Вставте посилання на Google Таблицю:")
        uploaded_file = st.file_uploader("Оберіть файл")
        load_button = st.button("Завантажити")

        df = pd.DataFrame()

        if uploaded_file is not None:
            if uploaded_file.name.endswith((".xlsx", ".xls")):
                try:
                    df = pd.read_excel(uploaded_file)
                    st.success("Файл успішно завантажено!")
                    df.columns = df.columns.str.replace(" ", "")  # Видалення пробілів
                    excluded_columns = ["Adding", "ЄДРПОУ", "Юр.адресаклієнта"]
                    df = df[df['Регіон'].isin(['24. Тернопіль', '10. Івано-Франк'])]
                    st.session_state.df = df
                except Exception as e:
                    st.error(f"Помилка при зчитуванні файлу: {e}")
            else:
                st.error("Будь ласка, завантажте Excel-файл (.xlsx або .xls)")
        elif sheet_url and load_button:
            df = load_data(sheet_url)
            if isinstance(df, str):
                st.error(df)
                df = pd.DataFrame()
            else:
                st.success("Дані успішно завантажені з посилання!")
                st.session_state.df = df

        if not df.empty:
            st.write("Колонки таблиці:", list(df.columns))

if selected == "Регіони":
    rerion_page.show_data()
elif selected == "Місто":
    city_page.show_data()
