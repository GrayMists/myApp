import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from data_processing import (
    prepare_filtered_data)

from data_cleaner import change_district_name


def show_data():
    # Перевірка, чи є дані
    if "df" not in st.session_state:
        st.warning("Спочатку завантажте файл на сторінці 'Завантаження'")
        return
    df = st.session_state.df
    if df is not None:
        #Переконуємось, що всі назви колонок є рядками, та очищаємо від пробілів на початку і вкінці
        df.columns = df.columns.astype(str).str.strip()
        df["Регіон"] = df["Регіон"].apply(change_district_name)
        # Вибір регіону
        if "Регіон" not in df.columns:
            st.error("Для отримання даних треба ввести правильне посилання")
            return
        else:
            selected_region = st.selectbox("Оберіть регіон:", df["Регіон"].unique())

        # Замініть існуючий фільтр
        filtered_df = prepare_filtered_data(df, selected_region)
    
    with st.expander("Натисни щоб побачіть відфільтровану таблицю продаж", icon="⬇️"):
        st.write(filtered_df)
    
    mask = filtered_df["Територія"].str.contains("Теронопіль.заг", case=False, na=False) | (filtered_df["Територія"] == "")
    if mask.any():
        st.write("В даній таблиці наведено інфомацію по рподажаї які не вдалось розподілити до певної території")
        st.write(filtered_df[mask])

    col1, col2 = st.columns([3,4])

    with col1:
        col3, col4 = st.columns(2)

        with col3:
            st.write("ТОП-5 найбільших продаж області")
            st.dataframe(filtered_df.groupby("Найменування")["Кількість"].sum().sort_values(ascending=False).head(5), width=500)
        with col4:
            st.write("ТОП-5 найменших продаж області")
            st.dataframe(filtered_df.groupby("Найменування")["Кількість"].sum().sort_values().head(5), width=500)

        st.write("Продажі по територіях")
        pivot = filtered_df.pivot_table(
            index="Найменування",
            columns="Територія",
            values="Кількість",
            aggfunc="sum",
            fill_value=0
        )
        st.write(pivot)
    with col2:
        # Створюємо список унікальних міст з колонки "Факт.місто"
        cities = filtered_df["Місто"].dropna().unique()
        mr = filtered_df["Територія"].dropna().unique()

        if cities.size == 0:
            st.warning("Немає міст для вибору.")
        else:
            # Створення зведеної таблиці по місту та вулицях
            pivot_ternopil_street = pd.pivot_table(
                filtered_df,
                values="Кількість",
                index=["Територія","Місто", "Вулиця"],
                columns="Найменування",
                aggfunc="sum"
            )

            if not isinstance(pivot_ternopil_street.index, pd.MultiIndex):
                st.error("Індекс `pivot_ternopil_street` не є MultiIndex. Перевірте створення зведеної таблиці.")
            else:
                # Мультивибір для міста
                selected_cities = st.multiselect("Оберіть міста:", cities)
                selected_mr = st.multiselect("Оберіть територію(якщо вибрано місто Теронпіль):", mr)
                # Фільтруємо дані по вибраним містам
                if selected_cities:
                    filtered_df_sku = filtered_df[filtered_df["Місто"].isin(selected_cities)]
                else:
                    filtered_df_sku = filtered_df

                if selected_mr:
                    filtered_df_sku = filtered_df_sku[filtered_df_sku["Територія"].isin(selected_mr)]

                filtered_df_sku = filtered_df_sku.groupby("Найменування")["Кількість"].sum().reset_index()

                # Виводимо відфільтровані та згруповані дані
                st.write(filtered_df_sku.style
                    .set_table_styles([
                        {'selector': 'th.col0', 'props': [('width', '100px')]},  # задає ширину для колонки "Найменування"
                    ])
                    .hide(axis='index')
                )


                # Створення та виведення зведеної таблиці по місту та вулицях для вибраних міст і територій
                if selected_cities or selected_mr:
                    filtered_pivot_ternopil_street = pivot_ternopil_street.loc[
                        pivot_ternopil_street.index.get_level_values("Місто").isin(selected_cities if selected_cities else cities) &
                        pivot_ternopil_street.index.get_level_values("Територія").isin(selected_mr if selected_mr else mr)
                    ]
                else:
                    filtered_pivot_ternopil_street = pivot_ternopil_street

                st.write(filtered_pivot_ternopil_street.droplevel("Місто").droplevel("Територія").fillna(0))


    group_teemap_df = filtered_df.groupby(["Територія","Найменування"])["Кількість"].sum().reset_index()
    fig = px.treemap(
    group_teemap_df,
    path=["Територія",'Найменування'],
    values='Кількість',
    color='Кількість',
    color_continuous_scale='RdBu'
    )
    fig.update_traces(hovertemplate='<b>%{label}</b><br>Кількість: %{value}')
 
    fig.update_layout(
        margin=dict(t=30, l=5, r=5, b=5),
        title='Розмір та колір відповідає кількості проданих упаковок',
        #paper_bgcolor='#fff',
    )


    st.plotly_chart(fig, use_container_width=True)
