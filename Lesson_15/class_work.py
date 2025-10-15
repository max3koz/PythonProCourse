import requests
from bs4 import BeautifulSoup

url = "https://google.com"

response = requests.get(url)

if response.status_code == 200:
	# 1
	soup = BeautifulSoup(response.text, 'html.parser')
	title_tag = soup.find('title')
	print("Заголовок сайту:", title_tag.text)
	
	# 2
	divs = soup.find_all('div')
	print(f"Знайдено {len(divs)} тегів <div>. Перші 10:")
	for i, div in enumerate(divs[:10], 1):
		print(f"\n--- <div> #{i} ---")
		print(div.prettify())

