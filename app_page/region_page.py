import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from data_processing import (
    get_session_dataframe, 
    prepare_filtered_data)

from data_cleaner import change_district_name

#Функція для отримання згрупованих препаратів 1 лінії
def line_one_df (df):
    line_one = df[df["Лінія"] == "Лінія 1"].groupby("Найменування")["Кількість"].sum().sort_values(ascending=False)

    return line_one
#Функція для отримання згрупованих препаратів 2 лінії
def line_two_df (df):
    line_two = df[df["Лінія"] == "Лінія 2"].groupby("Найменування")["Кількість"].sum().sort_values(ascending=False)

    return line_two

def show_data():
    # Перевірка, чи є дані
    df = get_session_dataframe()
    if df is not None:
        #Переконуємось, що всі назви колонок є рядками, та очищаємо від пробілів на початку і вкінці
        df.columns = df.columns.astype(str).str.strip()
        
        # Вибір регіону
        if "Регіон" not in df.columns:
            st.error("Для отримання даних треба ввести правильне посилання")
            return
        else:
            df["Регіон"] = df["Регіон"].apply(change_district_name)
            col1, col2 = st.columns(2)

            with col1:
                first_selected_region = st.selectbox("Оберіть регіон:", df["Регіон"].unique(), key="first_region")
                first_filtered_df = prepare_filtered_data(df, first_selected_region)
                col3, col4 = st.columns(2)
                with col3:
                    st.write("ТОП-5 найбільших продаж області")
                    st.dataframe(first_filtered_df.groupby("Найменування")["Кількість"].sum().sort_values(ascending=False).head(5))
                    st.write("Препарати першої ліній")
                    st.dataframe(line_one_df(first_filtered_df), height=1122)
                with col4:
                    st.write("ТОП-5 найменших продаж області")
                    st.dataframe(first_filtered_df.groupby("Найменування")["Кількість"].sum().sort_values().head(5))
                    st.write("Препарати другої ліній")
                    st.dataframe(line_two_df(first_filtered_df), height=737)
                

            with col2:
                second_selected_region = st.selectbox("Оберіть регіон:", df["Регіон"].unique(), key="second_region")
                second_filtered_df = prepare_filtered_data(df, second_selected_region)
                col5, col6 = st.columns(2)
                with col5:
                    st.write("ТОП-5 найбільших продаж області")
                    st.dataframe(second_filtered_df.groupby("Найменування")["Кількість"].sum().sort_values(ascending=False).head(5))
                    st.write("Препарати першої ліній")
                    st.dataframe(line_one_df(second_filtered_df), height=1122)
                with col6:
                    st.write("ТОП-5 найменших продаж області")
                    st.dataframe(second_filtered_df.groupby("Найменування")["Кількість"].sum().sort_values().head(5))
                    st.write("Препарати другої ліній")
                    st.dataframe(line_two_df(second_filtered_df), height=737)
        
            treemap_selected_region = st.selectbox("Оберіть регіон:", df["Регіон"].unique(), key="treemap")
            treemap_filtered_df = prepare_filtered_data(df, treemap_selected_region)
            df_grouped = treemap_filtered_df.groupby('Найменування', as_index=False)['Кількість'].sum()

            fig = px.treemap(
            df_grouped,
            path=['Найменування'],
            values='Кількість',
            color='Кількість',
            color_continuous_scale='speed'
            )
            fig.update_traces(hovertemplate='<b>%{label}</b><br>Кількість: %{value}')
        
            fig.update_layout(
                margin=dict(t=20, l=20, r=20, b=20),
                title='Продажі продуктів (розмір = обсяг)'
                #hovertemplate='<b>%{label}</b><br>Сума рахунку: %{value}'
            )

            st.subheader("Treemap продажів")
            st.plotly_chart(fig, use_container_width=True)               


                
                
    
