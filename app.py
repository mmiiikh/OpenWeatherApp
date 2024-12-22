import streamlit as st
import pandas as pd
import pickle
import requests
from datetime import datetime
import matplotlib.pyplot as plt


with open('stats.pkl', 'rb') as f:
    stats = pickle.load(f)

month_to_season = {12: "winter", 1: "winter", 2: "winter",
                   3: "spring", 4: "spring", 5: "spring",
                   6: "summer", 7: "summer", 8: "summer",
                   9: "autumn", 10: "autumn", 11: "autumn"}

st.title("Анализ погодных данных c OpenWeatherAPI")
st.header("Шаг 1: Загрузка данных")
uploaded_file = st.file_uploader("Выберите CSV-файл", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Превью данных:")
    st.dataframe(data)
else:
    st.write("Пожалуйста, загрузите CSV-файл.")

if uploaded_file is not None:
    st.header("Шаг 2: Выбор города")
    city = st.selectbox('Выберите город:', data.city.unique())
    st.header("Шаг 3: API ключ")
    apikey = st.text_input('Впишите ключ:')
    urlg = 'http://api.openweathermap.org/geo/1.0/direct'
    paramsg = {'q': city, 'appid': apikey}
    response_geo = requests.get(urlg, paramsg)
    err = {"cod":401, "message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."}
    if apikey is not "":
        if response_geo.status_code == 401:
            st.json(err)
        else:
            st.write("Ключ верный")
        st.header("Анализ погоды")
        lat = response_geo.json()[0]['lat']
        lon = response_geo.json()[0]['lon']
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'lat': lat, 'lon': lon, 'units': 'metric', 'appid': apikey}
        response = requests.get(url, params)
        st.write(f"Текущая температура в {city} составляет {response.json()['main']['temp']}.")
        resp_season = month_to_season[datetime.fromtimestamp(response.json()['dt']).month]
        needed_stat = stats[city]['stats'][stats[city]['stats'].index == resp_season]
        if response.json()['main']['temp'] < needed_stat['mean'][resp_season] + 2 * needed_stat['std'][resp_season] and response.json()['main']['temp'] > needed_stat['mean'][resp_season] - 2 * needed_stat['std'][resp_season]:
            st.write(f'Температура в {city} в пределах нормы')
        else:
            st.write('Температура аномальная')
        st.subheader("Историческая статистика")
        data_city = data[data['city'] == city].copy()
        st.write('Описательные статистики данных')
        st.write(data_city.describe(include = 'all'))
        measure = st.selectbox('Выберите показатель', stats[city].keys())
        st.write(stats[city][measure])
        if st.checkbox("Показать графики по историческим данным", key = 0):
            st.subheader('График изменения температуры')
            fig, ax = plt.subplots(figsize = (20,15))
            ax.plot(data_city.index, data_city['temperature'])
            if st.checkbox("Показать аномалии", key = 1):
                ax.scatter(stats[city]['anomalies'].index,stats[city]['anomalies']['temperature'], c = 'red')
            st.pyplot(fig)
