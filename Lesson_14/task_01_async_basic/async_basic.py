import asyncio
import random
from typing import List


async def download_page(url: str) -> None:
	"""
	The asynchronous function simulates loading a web page with a random delay.
	Args: url (str): The URL of the page to load.
	"""
	delay: int = random.randint(1, 5)
	await asyncio.sleep(delay)
	print(f"Downloaded: {url} in {delay} sec")


async def main(urls: List[str]) -> None:
	"""
	The asynchronous function loads a list of web pages at once.
	Args: urls (List[str]): List of URLs to load.
	"""
	tasks: List[asyncio.Task] = [asyncio.create_task(download_page(url)) for url
	                             in urls]
	await asyncio.gather(*tasks)
	# for task_item in asyncio.as_completed(tasks):
	# 	await task_item


test_urls = [
	"https://example1.com",
	"https://example2.com",
	"https://example3.com",
	"https://example4.com",
	"https://example5.com",
	"https://example6.com",
	"https://example7.com",
	"https://example8.com",
	"https://example9.com",
]

asyncio.run(main(test_urls))
