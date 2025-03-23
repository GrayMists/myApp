import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Налаштування сторінки
st.set_page_config(layout="wide")

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
        return pd.read_csv(csv_url)
    except Exception as e:
        return f"Помилка при завантаженні: {e}"

st.title("Завантаження Google Таблиці без авторизації")

# Поле для введення посилання
sheet_url = st.text_input("Вставте посилання на Google Табліцю:")

# Ініціалізуємо порожній DataFrame
df = pd.DataFrame()

if sheet_url:
    df = load_data(sheet_url)
    if isinstance(df, str):
        st.error(df)
        df = pd.DataFrame()  # Скидаємо df у випадку помилки
    else:
        st.success("Дані успішно завантажені!")

if not df.empty and df.columns.any():
    # Видаляємо пробіли у назвах колонок
    df.columns = df.columns.str.replace(' ', '')
    #видалаємо непотрібні колонки
    df = df.drop(columns=["Adding", "ЄДРПОУ", "Юр.адресаклієнта"], errors="ignore")



    # Очищуємо та перетворюємо колонку "Кількість" (якщо вона є)
    if "Кількість" in df.columns:
        df["Кількість"] = df["Кількість"].astype(str).str.strip().str.replace(r"[^\d\-]", "", regex=True)
        df["Кількість"] = pd.to_numeric(df["Кількість"], errors="coerce").fillna(0).astype(int)

    # Видалення пробілів на початку та в кінці
    df["Факт.адресадоставки"] = df["Факт.адресадоставки"].apply(lambda x: x.replace('\n', '').replace('\t', '').strip())

    # Фільтр бази по місту Тернопіль
    ternopil = df[df["Регіон"] == "24. Тернопіль"].reset_index(drop=True)


    remove_values = [
        "ТЕРНОПІЛЬСЬКА ОБЛ., ", "Тернопільська обл., ", "48702, ", "46008, ", "48201, ", "48430 ",
        "47100, ", "47400, ", "48431, ", "48260, ", "ГУСЯТИНСЬКИЙ Р-Н., ", "46002, ", "48740, ",
        "Чортківський р-н., ", "48543, ", "Тернопільська обл.,", "Гусятинський район ,",
        "Чортківський район, ", "Україна, ", "46016, ", "Тернопільський р-н., ", "Чортківський р-н., ",
        "Бучацький р-н.,", "Бучацький р-н,", "47851, ", "Борщівський р-н, ", "Чортківський р-н,", "Гусятинський р-н,", "Тернопільська область, "
    ]

    # Функція для видалення значень
    def remove_unwanted(text):
        for val in remove_values:
            text = text.replace(val, "")  # Поетапна заміна
        return text.strip()  # Видалення зайвих пробілів

    # Застосовуємо функцію до кожного рядка
    ternopil["Факт.адресадоставки"] = ternopil["Факт.адресадоставки"].apply(remove_unwanted)

    # Словник для заміни значень 
    replace_dict = {
        "ТЕРНОПІЛЬ": "м.Тернопіль,",
        "КОЗОВА": "м.Козова,",
        "БОРЩІВ": "м.Борщів,",
        "БЕРЕЖАНИ": "м.Бережани,",
        "КРЕМЕНЕЦЬ": "м.Кременець,",
        "ТЕРЕБОВЛЯ": "м.Теребовля,",
        "ЗАЛІЩИКИ": "м.Заліщики,",
        "М. ШУМСЬК": "м.Шумськ,",
        "ШУМСЬК": "м.Шумськ,",
        "ЧОРТКІВ": "м.Чортків,",
        "ПОЧАЇВ": "м.Почаїв,",
        "МОНАСТИРИСЬКА": "м.Монастириська,",
        "БУЧАЧ": "м.Бучач,",
        "ГУСЯТИН": "смт.Гусятин,",
        "смт Гусятин": "смт.Гусятин,",
        "ВИСОКЕ": "с.Високе,",
        "ВЕЛИКІ ГАЇ": "с.Великі Гаї,",
        "ТОВСТЕ": "смт.Товсте",
        "М. ЛАНІВЦІ": "м.Ланівці", 
        "ЛАНІВЦІ": "м.Ланівці", 
        "м.Ланівці": "м.Ланівці,",
        "смт.Ланівці": "м.Ланівці",
        "ПІДВОЛОЧИСЬК": "м.Підволочиськ,",
        "ЗБАРАЖ": "м.Збараж,",
        "МИКУЛИНЦІ": "селище Микулинці,",
        "ХОРОСТКІВ": "м.Хоростків,",
        "ІВАНЕ-ПУСТЕ": "с.Іване-Пусте,",
        "ВЕЛИКА БЕРЕЗОВИЦЯ": "селище Велика Березовиця,",
        "ВИШНІВЕЦЬ": "селище Вишнівець,",
        "ГРИМАЙЛІВ": "смт.Гримайлів,",
        "М. КОПИЧИНЦІ": "м.Копичинці,",
        "ЗБОРІВ": "м.Зборів,",
        "КОПИЧИНЦІ": "м.Копичинці,",
        "МЕЛЬНИЦЯ-ПОДІЛЬСЬКА": "м.Мельниця-Подільська,",
        "НАГІРЯНКА": "село Нагірянка,",
        "ПІДГАЙЦІ": "м. Підгайці,",
        "СКАЛА-ПОДІЛЬСЬКА": "м.Скала-Подільська,",
        "СКАЛАТ": "м.Скалат,",
        "УВИСЛА": "с.Увисла,",
        "смт.Товсте ": "смт.Товсте,",
        "вул.Симоненка В.": "вул.Симоненка Василя",
        "БІЛОКРИНИЦЯ": "с.Білокриниця,",
        "ГОРОДНИЦЯ": "с.Городниця,",
        "ЗАЛІЗЦІ": "с.Залізці,",
        "ЗОЛОТИЙ ПОТІК": "с.ЗолотийПотік,",
        "ЗОЛОТНИКИ": "с.Золотники,",
        "КОЦЮБИНЦІ": "с.Коцюбинці,",
        "МИШКОВИЧІ": "с.Мишковичі,",
        "НОВОСІЛКА": "с.Новосілка,"

    }


    # Функція заміни, що використовує словник
    def replacement(text):
        if isinstance(text, str):  # Переконуємось, що значення рядок
            for key, value in replace_dict.items():
                text = text.replace(key, value)  # Замінюємо ключ на значення
            return text.strip()  # Видаляємо зайві пробіли
        return text  # Якщо це не рядок, повертаємо його без змін

    # Застосовуємо функцію до кожного рядка
    ternopil["Факт.адресадоставки"] = ternopil["Факт.адресадоставки"].apply(replacement).replace(",,",",")
    ternopil["Факт.адресадоставки"] = ternopil["Факт.адресадоставки"].apply(lambda x: x.replace(",,", ",") if isinstance(x, str) else x)
    def remove_spaces(text):
        if isinstance(text, str):  # Перевіряємо, чи це рядок
            return "".join(char for char in text if char != " ")
        return text  # Якщо це не рядок, повертаємо без змін

    # Оновлена функція, що виконує лише обробку тексту до коми
    def extract_part(address):
        # Витягуємо текст до першої коми
        part_before_comma = address.split(',')[0].strip()

        # Повертаємо текст до коми
        return part_before_comma


    # Застосовуємо функцію до колонки
    ternopil["Факт.місто"] = ternopil['Факт.адресадоставки'].apply(extract_part)
    ternopil["Факт.місто"] = ternopil["Факт.місто"].apply(remove_spaces)

    def extract_street(address_street):
        parts = address_street.split(',')
        return parts[1].strip() if len(parts) > 1 else ""  # Перевіряємо, чи є хоча б 2 частини

    ternopil["Вулиця"] = ternopil['Факт.адресадоставки'].apply(extract_street)
    ternopil["Вулиця"] = ternopil["Вулиця"].apply(remove_spaces)

    # Функція для побудови графіку продажів за регіонами
    def plot_sales_by_region(data):
    # Групуємо дані за "Найменування" та сумуємо "Кількість"
        aggregated_data = data.groupby("Найменування")["Кількість"].sum().reset_index().sort_values(by="Кількість", ascending=False)
                # Створюємо графік
        fig, ax = plt.subplots()
        ax.bar(aggregated_data["Найменування"], aggregated_data["Кількість"], color="skyblue")

        # Налаштовуємо підписи
        ax.set_title("Sales by Region")  # Title of the graph
        ax.set_xlabel("Найменування", fontsize=8)       # X-axis label
        ax.set_ylabel("Кількість", fontsize=8)        # Y-axis label
        ax.set_xticklabels(aggregated_data["Найменування"], rotation=90, fontsize=7)  # Повертаємо підписи для кращого вигляду

        # Виводимо графік
        st.pyplot(fig)


    col1, col2 = st.columns([1,4])

    with col1:
        st.write("Загальна продана кількість")
        st.write(ternopil.groupby("Найменування")["Кількість"].sum())
        
    with col2:
        st.write("Таблиця з даними")
        st.write(ternopil)
    
    st.write(plot_sales_by_region(ternopil))

    # Створюємо список унікальних міст з колонки "Факт.місто"
    cities = ternopil["Факт.місто"].unique()

    # Створення зведеної таблиці по місту та вулицях
    pivot_ternopil_street = pd.pivot_table(ternopil, values="Кількість", index=["Факт.місто", "Вулиця"], columns="Найменування", aggfunc="sum")

    # Мультивибір для міста
    selected_cities = st.multiselect("Оберіть міста: (фільтр стосується тільки 'Зведена таблиця по містах та вулицях')", cities)

    # Створення та виведення зведеної таблиці по місту та вулицях для вибраних міст
    if selected_cities:
        filtered_pivot_ternipil_street = pivot_ternopil_street.loc[pivot_ternopil_street.index.get_level_values("Факт.місто").isin(selected_cities)]
    else:
        filtered_pivot_ternipil_street = pivot_ternopil_street

    st.markdown("<h3 style='color: #00FFFF; font-weight: bold; text-align: center;'>Зведена таблиця по містах та вулицях</h3>", unsafe_allow_html=True)
    st.write(filtered_pivot_ternipil_street)
    pivot_ternopil = pd.pivot_table(ternopil, values="Кількість", index="Факт.місто", columns="Найменування", aggfunc="sum")
    st.markdown("<h3 style='color: #00FFFF; font-weight: bold; text-align: center;'>Зведена таблиця по містах</h3>", unsafe_allow_html=True)
    st.write(pivot_ternopil)

