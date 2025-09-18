import requests


def download_page(url: str, filename: str) -> None:
	"""
	Downloads an HTML page from the specified URL and saves it to a text file
	in UTF-8 format.
    Parameters:
    - url (str): The address of the page to download.
    - filename (str): The name of the file in which the page content will be saved.
	"""
	try:
		response = requests.get(url, timeout=10)
		response.raise_for_status()  # Raise exception for status codes 4xx/5xx
		
		with open(filename, 'w', encoding='utf-8') as file:
			file.write(response.text)
		print(f"The page was saved to the '{filename}' file successfully.")
	
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error: {http_err}")
	except requests.exceptions.ConnectionError:
		print("Connect error. Check the internet connection or URL.")
	except requests.exceptions.Timeout:
		print("The waiting time has expired.")
	except requests.exceptions.RequestException as err:
		print(f"Another error: {err}")


download_page("https://www.google.com/", "google_page.txt")
