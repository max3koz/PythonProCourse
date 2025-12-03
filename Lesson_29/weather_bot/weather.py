import logging
from datetime import datetime

import requests

from config import API_KEY

logging.basicConfig(filename="app.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def get_weather(city: str) -> str:
	"""Отримуємо погоду з OpenWeather API"""
	start_time = datetime.now()
	url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ua"
	response = requests.get(url).json()
	
	if response.get("cod") != 200:
		logging.error(
			f"Неуспішний запит для міста '{city}'. Код: {response.get('cod')}")
		return "Не вдалося знайти місто. Спробуйте ще раз."
	
	temp = response["main"]["temp"]
	description = response["weather"][0]["description"]
	duration = (datetime.now() - start_time).total_seconds()
	logging.info(
		f"Успішний запит для міста '{city}'. "
		f"Температура: {temp}°C, {description}. "
		f"Час виконання: {duration:.2f} сек.")
	return f"Погода в {city}: {temp}°C, {description}."


if __name__ == "__main__":
	city = input("Введіть місто: ")
	print(get_weather(city))
