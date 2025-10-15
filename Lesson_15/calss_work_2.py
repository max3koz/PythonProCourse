"""
Скрипт повинен почати з першої сторінки (http://books.toscrape.com/).
Скрипт повинен обійти всі сторінки каталогу (до 50 сторінок). 🚀
Для кожної книги на кожній сторінці необхідно зібрати такі дані:
Назва книги (Title).
Ціна (Price, у фунтах стерлінгів).
Рейтинг (Rating, у вигляді слів, наприклад, "Three", "Five").
Наявність на складі (Availability – просто перевірка, чи присутній текст "In stock").
Зберігання Результатів:
Зібрані дані мають бути збережені у форматі CSV (Comma Separated Values) або Excel.
Кожен рядок у файлі повинен відповідати одній книзі.
Файл повинен мати чіткі заголовки стовпців: Назва, Ціна, Рейтинг, Наявність.
Вимоги до Реалізації та Кроки
HTTP-Запит (requests):
Створіть функцію, яка приймає URL і повертає об'єкт HTML-відповіді.
Обробіть можливі помилки запиту (наприклад, коди 404, 500) за допомогою конструкції try...except.
Парсинг HTML (BeautifulSoup):
Створіть функцію, яка приймає HTML-контент і парсить його, знаходячи всі елементи книг.
Для кожного елемента книги використовуйте методи find() або select_one() для вилучення необхідних даних:
Назва: зазвичай знаходиться в тегу <h3> або посиланням <a> всередині.
Ціна: використовуйте відповідний CSS-клас, наприклад, .price_color.
Рейтинг: шукайте клас, що починається з star-rating, наприклад, class="star-rating Three".
Навігація:
Реалізуйте логіку для переходу до наступної сторінки, шукаючи посилання з текстом "next" або відповідним CSS-класом у нижній частині поточної сторінки.
Очищення Даних (Data Cleaning):
Ціна: Приберіть символ валюти (наприклад, £) та перетворіть значення на числове (float).
Наявність: Перетворіть текстове значення на булеве (True/False або Так/Ні).
Рейтинг: Виділіть саме слово-рейтинг (наприклад, Three).
Очікуваний Результат
Файл, наприклад, books_data.csv, що містить сотні рядків (по одній книзі) з чітко структурованими даними.
НазваﾠЦінаﾠРейтингﾠНаявність
A Light in the Atticﾠ51.77ﾠThreeﾠTrue
Tipping the Velvetﾠ53.74ﾠOneﾠTrue
...ﾠ...ﾠ...ﾠ...
The Secret Gardenﾠ15.00ﾠTwoﾠTrue
"""


import csv
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"
START_URL = CATALOGUE_URL + "page-1.html"
MAX_PAGES = 10
HEADERS = ["Назва", "Ціна", "Рейтинг", "Наявність"]


def get_html(url):
	try:
		response = requests.get(url, timeout=10)
		response.encoding = 'utf-8'
		response.raise_for_status()
		return response.text
	except requests.RequestException as e:
		print(f"Помилка запиту до {url}: {e}")
		return None


def parse_books(html):
	soup = BeautifulSoup(html, "html.parser")
	books = soup.select("article.product_pod")
	results = []
	
	for book in books:
		title = book.h3.a["title"]
		
		price_text = book.select_one(".price_color").text.strip()
		price = float(price_text.replace("£", ""))
		
		rating_tag = book.select_one(".star-rating")
		rating = next(
			(cls for cls in rating_tag["class"] if cls != "star-rating"),
			"Unknown")
		
		availability_text = book.select_one(".availability").text.strip()
		availability = "In stock" in availability_text
		
		results.append([title, price, rating, availability])
	
	return results


def parse_all_books():
	all_books = []
	current_url = START_URL
	page_count = 0
	
	while current_url and page_count < MAX_PAGES:
		print(f"Парсимо: {current_url}")
		html = get_html(current_url)
		if not html:
			break
		
		soup = BeautifulSoup(html, "html.parser")
		books = parse_books(html)
		all_books.extend(books)
		
		current_url = get_next_page(soup)
		page_count += 1
		time.sleep(1)
	
	return all_books


def get_next_page(soup):
	next_link = soup.select_one("li.next a")
	if next_link:
		return CATALOGUE_URL + next_link["href"]
	return None


def save_to_csv(data, filename="books.csv"):
	with open(filename, "w", newline="", encoding="utf-8") as file:
		writer = csv.writer(file)
		writer.writerow(HEADERS)
		writer.writerows(data)
	print(f"Збережено {len(data)} книг у файл {filename}")


books = parse_all_books()
save_to_csv(books)
