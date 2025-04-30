import streamlit as st

# Ініціалізація df, якщо він ще не існує
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()  # або ваш DataFrame

# Тепер безпечно використовувати
df = st.session_state.df
def show_sidebar_data():
    with st.container(border=True):
        st.write("В подальшому тут будуть фільтри")