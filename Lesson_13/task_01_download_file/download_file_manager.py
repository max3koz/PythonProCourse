import os
import threading
from typing import List

import requests


def download_file(url: str, save_dir: str = "downloads") -> None:
	"""
	The function downloads a file from the specified URL and saves it
	to a local directory.
	Args:
		- url (str): Link to the file to download.
		- save_dir (str): Name of the directory to save the files.
	"""
	try:
		response = requests.get(url)
		response.raise_for_status()
		
		os.makedirs(save_dir, exist_ok=True)
		filename = os.path.join(save_dir, url.split("/")[-1])
		
		with open(filename, "wb") as file:
			for part in response.iter_content(chunk_size=8192):
				file.write(part) if part else None
		
		print(f"Downloaded: {filename}")
	except requests.RequestException as e:
		print(f"Error: download failed from {url}: {e}")


def download_files_concurrently(urls: List[str]) -> None:
	"""
	The function creates threads to download multiple files simultaneously.
	Args: urls (List[str]): List of URLs to download.
	"""
	threads: List[threading.Thread] = []
	
	for url in urls:
		thread = threading.Thread(target=download_file, args=(url,))
		threads.append(thread)
		thread.start()
	
	for thread in threads:
		thread.join()
	
	print("All downloads finished.")


file_urls = ["https://www.samplefiles.dev/files/documents/sample-pdf-file.pdf",
             "https://www.samplefiles.dev/files/images/sample-jpg-image.jpg",
             "https://www.samplefiles.dev/files/images/sample-png-image.png",
             "https://www.samplefiles.dev/files/audio/sample-mp3-file.mp3",
             "https://www.samplefiles.dev/files/documents/sample-csv-file.csv",
             "https://www.samplefiles.dev/files/archives/sample-zip-file.zip",
             "https://www.samplefiles.dev/files/documents/sample-docx-file.docx",
             "https://www.samplefiles.dev/files/documents/sample-xlsx-file.xlsx",
             "https://www.samplefiles.dev/files/documents/sample-txt-file.txt",
             "https://www.samplefiles.dev/files/videos/sample-mp4-video.mp4"
             ]

download_files_concurrently(file_urls)
