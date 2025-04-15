import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from data_loader import load_data




# Створюємо вибір між сторінками
st.set_page_config(
    page_title="Salae board",
    page_icon="⚡️",
    layout="wide"
)

st.title("Завантаження Google Таблиці ")
st.sidebar.success("Pages")
# Поле для введення посилання
sheet_url = st.text_input("Вставте посилання на Google Табліцю:")
load_button = st.button("Завантажити")
# Ініціалізуємо порожній DataFrame
df = pd.DataFrame()

if sheet_url and load_button:
    df = load_data(sheet_url)
    if isinstance(df, str):
        st.error(df)
        df = pd.DataFrame()  # Скидаємо df у випадку помилки
    else:
        st.success("Дані успішно завантажені!")
        # Зберігаємо завантажені дані в session_state
        st.session_state.df = df
