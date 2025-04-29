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
import app_page.sales as sales
import app_page.sidebar_region as sidebar_region
import app_page.sidebar_city as sidebar_city

from data_loader import load_data, process_uploaded_excel



with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Завантаження", "Регіони", "Місто", "Прогноз"],
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
                    df = process_uploaded_excel(uploaded_file)
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
    elif selected == "Регіони":
        sidebar_region.show_data()
    elif selected == "Місто":
        sidebar_city.show_sidebar_data()

if selected == "Завантаження":
    show_welcome = True

    if "df" in st.session_state and not st.session_state.df.empty:
        if show_welcome:
            st.markdown("""
            ### 👋 Вітаю в моєму застосунку!

            Якщо ти працюєш в моїй команді компанії **Нутрімед**, 
            завантаж, будь ласка, файли у боковій панелі для подальшої роботи з ними.
            """)
        st.markdown("#### Перейдіть до наступних розділів:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Перейти до Регіони"):
                selected = "Регіони"
                show_welcome = False
        with col2:
            if st.button("Перейти до Місто"):
                selected = "Місто"
                show_welcome = False

if selected == "Регіони":
    rerion_page.show_data()
elif selected == "Місто":
    city_page.show_data()
elif selected == "Прогноз":
    sales.show_data()
