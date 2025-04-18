import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_processing import (
    get_session_dataframe, 
    prepare_filtered_data)

from data_cleaner import change_district_name



def show_data():
    # Перевірка, чи є дані
    df = get_session_dataframe()
    if df is not None:
        #Переконуємось, що всі назви колонок є рядками, та очищаємо від пробілів на початку і вкінці
        df.columns = df.columns.astype(str).str.strip()
        
        # Вибір регіону
        if "Регіон" not in df.columns:
            st.error("Для отримання даних треба ввести правильне посилання")
            df["Регіон"] = df["Регіон"].apply(change_district_name)
            return
        else:
            col1, col2 = st.columns(2)

            with col1:
                first_selected_region = st.selectbox("Оберіть регіон:", df["Регіон"].unique(), key="first_region")
                first_filtered_df = prepare_filtered_data(df, first_selected_region)
                col3, col4 = st.columns(2)
                with col3:
                    st.write("ТОП-5 найбільших продаж області")
                    st.dataframe(first_filtered_df.groupby("Найменування")["Кількість"].sum().sort_values(ascending=False).head(5))
                with col4:
                    st.write("ТОП-5 найменших продаж області")
                    st.dataframe(first_filtered_df.groupby("Найменування")["Кількість"].sum().sort_values().head(5))

            with col2:
                second_selected_region = st.selectbox("Оберіть регіон:", df["Регіон"].unique(), key="second_region")
                second_filtered_df = prepare_filtered_data(df, second_selected_region)
                col5, col6 = st.columns(2)
                with col5:
                    st.write("ТОП-5 найбільших продаж області")
                    st.dataframe(second_filtered_df.groupby("Найменування")["Кількість"].sum().sort_values(ascending=False).head(5))
                with col6:
                    st.write("ТОП-5 найменших продаж області")
                    st.dataframe(second_filtered_df.groupby("Найменування")["Кількість"].sum().sort_values().head(5))