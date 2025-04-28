import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt


def show_data():
    # Створення даних продажів
    data_input = st.text_input("Введіть дані продаж через кому. Наприклад:172,205,176")

    if data_input:
        data_list = [int(x) for x in data_input.split(",") if x.strip()]
        data = {"sale_amount": data_list}
        sales_data = pd.DataFrame(data)
    else:
        st.error("Будь ласка, введіть дані продажів.")

    button = st.button("Запустити розрахунки")

    if button:

        # Bootstrap function: generating new samples with replacement
        def bootstrap(data, n_iterations):
            sample_means = []
            for i in range(n_iterations):
                sample = data.sample(frac=1, replace=True)  # resampling with replacement
                sample_means.append(sample["sale_amount"].mean())
            return sample_means




        # Виконання бутстрепу
        bootstrap_means = bootstrap(sales_data, 1000)

        # Обчислення середнього, стандартного відхилення та довірчого інтервалу
        mean_purchase = np.mean(sales_data["sale_amount"])
        std_dev = np.std(sales_data["sale_amount"], ddof=1)
        n = len(sales_data)
        confidence = 0.95
        confidence_interval = stats.t.interval(
            confidence, df=n - 1, loc=mean_purchase, scale=std_dev / np.sqrt(n)
        )


        # Функція для відображення результатів
        st.write(f"Середнє очікуване: {mean_purchase}")
        st.write(f"Мінімально можливо: {confidence_interval[0]:.2f}")
        st.write(f"Максимально можливо: {confidence_interval[1]:.2f}")
       

        # Візуалізація розподілу середніх бутстрепів
        fig, ax = plt.subplots()
        ax.hist(bootstrap_means, bins=30, edgecolor="black")
        ax.set_title("Bootstrap Distribution of Sample Means")
        ax.set_xlabel("Mean Sale Amount")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)