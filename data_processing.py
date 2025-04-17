import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt



from data_cleaner import (
    clean_quantity_column,
    clean_address_column,
    remove_unwanted,
    replacement_city,
    extract_city,
    remove_spaces,
    replacement_street,
    extract_street,
    mr_district,
    extract_num_house,
    update_territory_for_city_streets,
    assign_line_from_product_name
    
)
from dictionaries.dictionary_to_clear import (
    remove_values_from_ternopil,
    remove_values_from_frankivsk,
)
from dictionaries.replacement_city_dictionaries import replace_ternopil_city_dict
from dictionaries.replacement_street_dictionaries import replace_ternopil_street_dict
from dictionaries.mr import territory_mr, street_territory_2
from products import products_dict


# Перевірка, чи є дані в session_state
def get_session_dataframe():
    if 'df' in st.session_state:
        return st.session_state.df  # Отримуємо дані з session_state
    else:
        st.error("Дані не знайдено. Спочатку завантажте дані на першій сторінці.")
        return None

def process_filtered_df(df, region_name):
    # Логіка для того щоб датасет очищався з допомогою відповідних словників під регіон
    if region_name == "м.Тернопіль":
        region_values = remove_values_from_ternopil
        city_values = replace_ternopil_city_dict
        street_value = replace_ternopil_street_dict
        street_mr = street_territory_2
    elif region_name == "м.Івано-Франківськ":
        region_values = remove_values_from_frankivsk
        city_values = {}
        street_value = {}
        street_mr = {}

    # Проводимо очистку відфільтрованого датасету змінюючи назви міст та вулиць на коректні
    df["Факт.адресадоставки"] = df["Факт.адресадоставки"].apply(remove_unwanted, region_values=region_values)
    df["Факт.адресадоставки"] = df["Факт.адресадоставки"].apply(replacement_city, city_values=city_values).replace(",,", ",")
    df['Факт.адресадоставки'] = df['Факт.адресадоставки'].str.replace(" ", "")
    
    df['Факт.адресадоставки'] = df['Факт.адресадоставки'].apply(replacement_street, street_values=street_value).str.replace(',,', ',', regex=True)
    
    # Створюємо колонку з назвою міста, для подальшої можливості групування
    df["Факт.місто"] = df['Факт.адресадоставки'].apply(extract_city)
    df["Факт.місто"] = df["Факт.місто"].apply(remove_spaces)
    # Створюємо колонку з назвою вулиці, для подальшої можливості групування
    df["Вулиця"] = df['Факт.адресадоставки'].apply(extract_street)
    df["Вулиця"] = df["Вулиця"].str.strip()

    df["НомерБудинку"] = df['Факт.адресадоставки'].apply(extract_num_house)
    df["НомерБудинку"] = df["НомерБудинку"].str.strip()
    
    # Додаємо категоризацію по території, для подальшого зручнішого групування
    df["Територія"] = df["Факт.місто"].apply(lambda x: mr_district(x, territory_mr))
    df = update_territory_for_city_streets(df, region_name, street_mr)
    df = assign_line_from_product_name(df, products_dict)
    # Функція очищення колонки "Кількість"
    clean_quantity_column(df)
    # Функція очищення адреси доставки від пробілів
    clean_address_column(df)
    
    return df
#Обробка даних, та формування фінального dataFrame з яким буде проводитись візуалізація
def prepare_filtered_data(df, region_name):
    filtered_df = df[df["Регіон"] == region_name].reset_index(drop=True)
    filtered_df = process_filtered_df(filtered_df, region_name)
    
    return filtered_df


#         col1, col2 = st.columns([1, 4])

#         with col1:
#             st.write("ТОП-5 найбільших продаж області")
#             st.dataframe(filtered_df.groupby("Найменування")["Кількість"].sum().sort_values(ascending=False).head(5), width=500)
#             st.write("ТОП-5 найменших продаж області")
#             st.dataframe(filtered_df.groupby("Найменування")["Кількість"].sum().sort_values().head(5), width=500)

#         with col2:
#             # Створюємо список унікальних міст з колонки "Факт.місто"
#             cities = filtered_df["Факт.місто"].dropna().unique()

#             if cities.size == 0:
#                 st.warning("Немає міст для вибору.")
#             else:
#                 # Створення зведеної таблиці по місту та вулицях
#                 pivot_ternopil_street = pd.pivot_table(
#                     filtered_df,
#                     values="Кількість",
#                     index=["Факт.місто", "Вулиця"],
#                     columns="Найменування",
#                     aggfunc="sum"
#                 )

#                 if not isinstance(pivot_ternopil_street.index, pd.MultiIndex):
#                     st.error("Індекс `pivot_ternopil_street` не є MultiIndex. Перевірте створення зведеної таблиці.")
#                 else:
#                     # Мультивибір для міста
#                     selected_cities = st.multiselect("Оберіть міста: (фільтр стосується тільки 'Зведена таблиця по містах та вулицях')", cities)
#                     # Фільтруємо дані по вибраним містам
#                     if selected_cities:
#                         filtered_df_sku = filtered_df[filtered_df["Факт.місто"].isin(selected_cities)].groupby("Найменування")["Кількість"].sum().reset_index()
#                     else:
#                         filtered_df_sku = filtered_df.groupby("Найменування")["Кількість"].sum().reset_index()

#                     # Виводимо відфільтровані та згруповані дані
#                     st.write(filtered_df_sku.style
#                         .set_table_styles([
#                             {'selector': 'th.col0', 'props': [('width', '100px')]},  # задає ширину для колонки "Найменування"
#                         ])
#                         .hide(axis='index')
#                     )

#                     # Створення та виведення зведеної таблиці по місту та вулицях для вибраних міст
#                     if selected_cities:
#                         filtered_pivot_ternipil_street = pivot_ternopil_street.loc[
#                             pivot_ternopil_street.index.get_level_values("Факт.місто").isin(selected_cities)
#                         ]
#                     else:
#                         filtered_pivot_ternipil_street = pivot_ternopil_street

#                     st.write(filtered_pivot_ternipil_street.fillna(0))

#                     pivot = filtered_df.pivot_table(
#                         index="Найменування",
#                         columns="Територія",
#                         values="Кількість",
#                         aggfunc="sum",
#                         fill_value=0
#                     )
#                     st.write(pivot)

#                     # Перевертаємо, щоб товари були знизу вгору
#                     pivot = pivot[::-1]

#                     # Побудова графіка
#                     pivot.plot(kind="barh", stacked=False, figsize=(4, 10), width=0.8)
#                     fig = plt.gcf()
#                     ax = plt.gca()
#                     fig.patch.set_facecolor('#0b4b5c')  # фон всієї області
#                     ax.set_facecolor('#0b4b5c')         # фон поля побудови

#                     plt.title("Продажі товарів та територіях", color="#fff")
#                     plt.xlabel("Кількість", color="#fff")
#                     plt.ylabel("Товар", color="#fff")

#                     # Зменшення шрифту легенди
#                     plt.legend(fontsize=8)

#                     # Показуємо графік
#                     st.pyplot(plt.gcf())

#     st.write(filtered_df)
#     mask = filtered_df["Територія"].str.contains("Теронопіль.заг", case=False, na=False)
#     if mask.any():
#         st.write("В даній таблиці наведено інфомацію по рподажаї які не вдалось розподілити до певної території")
#         st.write(filtered_df[mask])