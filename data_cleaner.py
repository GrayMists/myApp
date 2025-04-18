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
#Функція для заміни назв вулиць
def replacement_street(text, street_values):
    if isinstance(text, str):  # Переконуємось, що значення рядок
        for key, value in street_values.items():
            text = text.replace(key, value)  # Замінюємо ключ на значення
        return text.strip()  # Видаляємо зайві пробіли
    return text  # Якщо це не рядок, повертаємо його без змін
#Функція для отримання назв вулиць
def extract_street(address_street):
    parts = address_street.split(',')
    return parts[1].strip() if len(parts) > 1 else ""  # Перевіряємо, чи є хоча б 2 частини
#Функція для отримання номуру будинку
def extract_num_house(address_street):
    parts = address_street.split(',')
    return parts[2].strip() if len(parts) > 2 else ""  # Перевіряємо, чи є хоча б 3 частини
#Функція яка визначає приналежність до певної території відповідно до міста
def mr_district(text, dict):
    if isinstance(text, str):  # Перевіряємо, чи це рядок
        return dict.get(text, "").strip()
    return text
#Функція яка визначає приналежність до певної території відповідно до вулиці в місті
def update_territory_for_city_streets(df, city_name, street_dict):
    def update_row(row):
        if row["Факт.місто"] == city_name:
            for street_key, territory in street_dict.items():
                if pd.notna(row["Вулиця"]) and street_key in row["Вулиця"]:
                    return territory
        return row["Територія"]
    
    df["Територія"] = df.apply(update_row, axis=1)
    return df
#Функція яка визначає приналежність до певної лінії перпарату
def assign_line_from_product_name(df, product_dict):
    def find_line(name):
        for key in product_dict:
            if key in name:
                return product_dict[key]
        return None  # або "" якщо потрібно залишати порожнім
    if "Найменування" in df.columns:
        df["Лінія_авто"] = df["Найменування"].apply(find_line)
    return df

#Функція зміни наз регіонів
def change_district_name(region: str):
    region = str(region).strip()
    if region == "10. Івано-Франк":
        return "м.Івано-Франківськ"
    elif region == "24. Тернопіль":
        return "м.Тернопіль"
    return region

#Функцію очищення колонки адреси, та отримання нових колонок міста, вулиці та номеру бодинку
def clean_delivery_address(df, column, region_name, region_values, city_values, street_value, territory_mr, street_mr, products_dict):
    df[column] = (
        df[column]
        .apply(remove_unwanted, region_values=region_values)
        .apply(replacement_city, city_values=city_values)
        .str.replace(" ", "")
        .apply(replacement_street, street_values=street_value)
        .str.replace(",,", ",", regex=True)
    )
    
    df["Факт.місто"] = df[column].apply(extract_city).apply(remove_spaces)
    df["Вулиця"] = df[column].apply(extract_street).str.strip()
    df["НомерБудинку"] = df[column].apply(extract_num_house).str.strip()

    # Додаємо категоризацію по території, для подальшого зручнішого групування
    df["Територія"] = df["Факт.місто"].apply(lambda x: mr_district(x, territory_mr))
    df = update_territory_for_city_streets(df, region_name, street_mr)
    df = assign_line_from_product_name(df, products_dict)
    # Функція очищення колонки "Кількість"
    clean_quantity_column(df)
    # Функція очищення адреси доставки від пробілів
    clean_address_column(df)
    
    return df