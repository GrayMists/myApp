import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from st import df

from data_cleaner import clean_quantity_column, clean_address_column,remove_unwanted, replacement_city,extract_city,remove_spaces,replacement_street, extract_street
from dictionary_to_clear import remove_values_from_ternopil, remove_values_from_frankivsk
from replacement_city_dictionaries import replace_ternopil_city_dict
from replacement_street_dictionaries import replace_ternopil_street_dict

# Перевірка, чи є дані в session_state
if 'df' in st.session_state:
    df = st.session_state.df  # Отримуємо дані з session_state
else:
    st.error("Дані не знайдено. Спочатку завантажте дані на першій сторінці.")

# Функція очищення колонки "Кількість"
clean_quantity_column(df)
# Функція очищення адреси доставки від пробілів
clean_address_column(df)

df.columns = df.columns.astype(str).str.strip()
# Вибір регіону
if "Регіон" not in df.columns:
    st.error("Для отримання даних треба ввести правильне посилання")
else:
    selected_region = st.selectbox("Оберіть регіон:", df["Регіон"].unique())

# Замініть існуючий фільтр
filtered_df = df[df["Регіон"] == selected_region].reset_index(drop=True)

if filtered_df.empty:
    st.warning("Немає даних для вибраного регіону!")
else:
    #Логіка для того щоб датасет очищався з допомогою відповідних словників під регіон
    if selected_region == "24. Тернопіль":
        region_values = remove_values_from_ternopil
        city_values = replace_ternopil_city_dict
        street_value = replace_ternopil_street_dict
    elif selected_region == "10. Івано-Франк":
        region_values = remove_values_from_frankivsk
        city_values = {}
        street_value = {}

    #Проводимо очистку відфільтрованого датасету змінююси назви міст та вулиць на коректні
    filtered_df["Факт.адресадоставки"] = filtered_df["Факт.адресадоставки"].apply(remove_unwanted, region_values=region_values)
    filtered_df["Факт.адресадоставки"] = filtered_df["Факт.адресадоставки"].apply(replacement_city, city_values=city_values).replace(",,", ",")
    filtered_df['Факт.адресадоставки'] = filtered_df['Факт.адресадоставки'].str.replace(" ","")
    filtered_df['Факт.адресадоставки'] = filtered_df['Факт.адресадоставки'].apply(replacement_street, street_values=street_value).replace(",,",",")
    #Створюємо колонку з назвою міста, для подальшої можливості групування
    filtered_df["Факт.місто"] = filtered_df['Факт.адресадоставки'].apply(extract_city)
    filtered_df["Факт.місто"] = filtered_df["Факт.місто"].apply(remove_spaces)

    filtered_df["Вулиця"] = filtered_df['Факт.адресадоставки'].apply(extract_street)
    #filtered_df["Вулиця"] = filtered_df["Вулиця"].apply(remove_spaces)
    filtered_df["Найменування"] = filtered_df["Найменування"].str.strip()
    st.write(filtered_df)
    

    
    col1, col2 = st.columns([1,4])

    with col1:
         st.write("ТОП-5 найбільших продаж області")
         st.dataframe(filtered_df.groupby("Найменування")["Кількість"].sum().sort_values(ascending=False).head(5), width=500)
         st.write("ТОП-5 найменших продаж області")
         st.dataframe(filtered_df.groupby("Найменування")["Кількість"].sum().sort_values().head(5), width=500)
            
    with col2:
        # Створюємо список унікальних міст з колонки "Факт.місто"
        cities = filtered_df["Факт.місто"].dropna().unique()

        if cities.size == 0:
            st.warning("Немає міст для вибору.")
        else:
            # Створення зведеної таблиці по місту та вулицях
            pivot_ternopil_street = pd.pivot_table(filtered_df, values="Кількість", index=["Факт.місто", "Вулиця"], columns="Найменування", aggfunc="sum")
            
            if not isinstance(pivot_ternopil_street.index, pd.MultiIndex):
                st.error("Індекс `pivot_ternopil_street` не є MultiIndex. Перевірте створення зведеної таблиці.")
            else:
                # Мультивибір для міста
                selected_cities = st.multiselect("Оберіть міста: (фільтр стосується тільки 'Зведена таблиця по містах та вулицях')", cities)
                # Фільтруємо дані по вибраним містам
                if selected_cities:
                    filtered_df_sku = filtered_df[filtered_df["Факт.місто"].isin(selected_cities)].groupby("Найменування")["Кількість"].sum().reset_index()
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
                    filtered_pivot_ternipil_street = pivot_ternopil_street.loc[pivot_ternopil_street.index.get_level_values("Факт.місто").isin(selected_cities)]
                    
                else:
                    filtered_pivot_ternipil_street = pivot_ternopil_street

                
                st.write(filtered_pivot_ternipil_street.fillna(0))
                
st.write(filtered_df.style \
        .format(precision=3, thousands=".", decimal=",") \
        .format_index(str.upper, axis=1)
         )          
