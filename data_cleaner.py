import pandas as pd


# Функція очищення колонки "Кількість"
def clean_quantity_column(df):
    if "Кількість" in df.columns:
        df["Кількість"] = df["Кількість"].astype(str).str.strip().str.replace(r"[^\d\-]", "", regex=True)
        df["Кількість"] = pd.to_numeric(df["Кількість"], errors="coerce").fillna(0).astype(int)
    return df

# Функція очищення адреси доставки
def clean_address_column(df):
    if "Факт.адресадоставки" in df.columns:
        df["Факт.адресадоставки"] = df["Факт.адресадоставки"].apply(lambda x: x.replace('\n', '').replace('\t', '').strip())
    return df

# Функція для видалення значень
def remove_unwanted(text, region_values):
    if isinstance(text, str):  # Перевіряємо, чи це рядок
        for val in region_values:
            text = text.replace(val, "")  # Поетапна заміна
    return text.strip()  # Видалення зайвих пробілів
#Функція для зміни назви вулиць, для приведення до єдиного спільного
def replacement_city(text, city_values):
    if isinstance(text, str):  # Переконуємось, що значення - це рядок
        for key, value in city_values.items():  # Використовуємо city_values, якщо це словник
            text = text.replace(key, value)  # Поетапна заміна
    return text.strip()  # Видаляємо зайві пробіли

#Витягуємо назву міста
def extract_city(address):
        # Витягуємо текст до першої коми
        part_before_comma = address.split(',')[0].strip()

        # Повертаємо текст до коми
        return part_before_comma
#Видаляємо пробіли
def remove_spaces(text):
    if isinstance(text, str):  # Перевіряємо, чи це рядок
        return "".join(char for char in text if char != " ")
    return text  # Якщо це не рядок, повертаємо без змін

def replacement_street(text, street_values):
    if isinstance(text, str):  # Переконуємось, що значення рядок
        for key, value in street_values.items():
            text = text.replace(key, value)  # Замінюємо ключ на значення
        return text.strip()  # Видаляємо зайві пробіли
    return text  # Якщо це не рядок, повертаємо його без змін
def extract_street(address_street):
    parts = address_street.split(',')
    return parts[1].strip() if len(parts) > 1 else ""  # Перевіряємо, чи є хоча б 2 частини

def mr_district(text, dict):
    if isinstance(text, str):  # Перевіряємо, чи це рядок
        return dict.get(text, "").strip()
    return text
