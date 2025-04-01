import streamlit as st
import pandas as pd

# Функція для отримання CSV-посилання
def get_csv_url(sheet_url):
    try:
        if "/d/" not in sheet_url or "/edit" not in sheet_url:
            return None
        sheet_id = sheet_url.split("/d/")[1].split("/")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    except IndexError:
        return None

# Кешуємо завантаження даних до моменту зміни URL
#@st.cache_data(hash_funcs={str: hash})
def load_data(sheet_url):
    csv_url = get_csv_url(sheet_url)
    if not csv_url:
        return None
    try:
        df = pd.read_csv(csv_url)
        df.columns = df.columns.str.replace(" ","")  # Видаляємо пробіли з назв колонок
        excluded_columns = ["Adding", "ЄДРПОУ", "Юр.адресаклієнта"]
        df = df[df['Регіон'].isin(['24. Тернопіль'])]
        #, '10. Івано-Франк', '21. Ужгород' <-- до фільтру тернопіль щоб отримувати тільки ті дані що будуть в фільтрі
        df = df.drop(columns=[col for col in excluded_columns if col in df.columns], errors="ignore")
        return df
    except Exception as e:
        return f"Помилка при завантаженні: {e}"