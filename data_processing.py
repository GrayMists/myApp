import streamlit as st

from data_cleaner import clean_delivery_address

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
    region_values = []  # або None, якщо remove_unwanted вміє це обробити
    city_values = {}
    street_value = {}
    street_mr = {}
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

    col = "Факт.адресадоставки"
    df = clean_delivery_address(df, col, region_values, city_values, street_value, territory_mr, street_mr, products_dict)
    
    return df
#Обробка даних, та формування фінального dataFrame з яким буде проводитись візуалізація
def prepare_filtered_data(df, region_name):
    filtered_df = df[df["Регіон"] == region_name].reset_index(drop=True)
    filtered_df = process_filtered_df(filtered_df, region_name)
    
    return filtered_df
