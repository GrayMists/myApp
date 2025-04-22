import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data_processing import (
    get_session_dataframe, 
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
    
    with st.expander("Натисни щоб побачить відфільтровану таблицію продаж", icon="⬇️"):
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

        if cities.size == 0:
            st.warning("Немає міст для вибору.")
        else:
            # Створення зведеної таблиці по місту та вулицях
            pivot_ternopil_street = pd.pivot_table(
                filtered_df,
                values="Кількість",
                index=["Місто", "Вулиця"],
                columns="Найменування",
                aggfunc="sum"
            )

            if not isinstance(pivot_ternopil_street.index, pd.MultiIndex):
                st.error("Індекс `pivot_ternopil_street` не є MultiIndex. Перевірте створення зведеної таблиці.")
            else:
                # Мультивибір для міста
                selected_cities = st.multiselect("Оберіть міста:", cities)
                # Фільтруємо дані по вибраним містам
                if selected_cities:
                    filtered_df_sku = filtered_df[filtered_df["Місто"].isin(selected_cities)].groupby("Найменування")["Кількість"].sum().reset_index()
                else:
                    filtered_df_sku = filtered_df.groupby("Найменування")["Кількість"].sum().reset_index()

                # Виводимо відфільтровані та згруповані дані
                st.write(filtered_df_sku.style
                    .set_table_styles([
                        {'selector': 'th.col0', 'props': [('width', '100px')]},  # задає ширину для колонки "Найменування"
                    ])
                    .hide(axis='index')
                )

                # Створення та виведення зведеної таблиці по місту та вулицях для вибраних міст
                if selected_cities:
                    filtered_pivot_ternipil_street = pivot_ternopil_street.loc[
                        pivot_ternopil_street.index.get_level_values("Місто").isin(selected_cities)
                    ]
                else:
                    filtered_pivot_ternipil_street = pivot_ternopil_street

                st.write(filtered_pivot_ternipil_street.droplevel("Місто").fillna(0))
                styled_df = (
                filtered_pivot_ternipil_street
                .droplevel("Місто")
                .fillna(0)
                .reset_index()
                .style
                .set_properties(subset=["Вулиця"], props=[("width", "150px")])
                )

                st.write(styled_df)
                
                

                

                # Перевертаємо, щоб товари були знизу вгору
                pivot = pivot[::-1]

                # Побудова графіка
                pivot.plot(kind="barh", stacked=False, figsize=(4, 10), width=0.8)
                fig = plt.gcf()
                ax = plt.gca()
                fig.patch.set_facecolor('#0b4b5c')  # фон всієї області
                ax.set_facecolor('#0b4b5c')         # фон поля побудови

                plt.title("Продажі товарів та територіях", color="#fff")
                plt.xlabel("Кількість", color="#fff")
                plt.ylabel("Товар", color="#fff")

                # Зменшення шрифту легенди
                plt.legend(fontsize=8)

                # Показуємо графік
                st.pyplot(plt.gcf())

    
