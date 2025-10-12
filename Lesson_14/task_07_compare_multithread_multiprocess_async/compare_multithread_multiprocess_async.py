import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import aiohttp
import requests

URL = "https://yavuzceliker.github.io/sample-images/image-1021.jpg"
TOTAL_REQUESTS = 500


def sync_requests() -> None:
	"""
	The function executes TOTAL_REQUESTS HTTP requests to a URL synchronously.
	Each request is executed sequentially using the requests library.
	"""
	for item in range(TOTAL_REQUESTS):
		response = requests.get(URL)
		if response.status_code != 200:
			print(
				f"The request #{item} returned status: {response.status_code}")
		assert response.status_code == 200


def threaded_requests() -> None:
	"""
	The function executes TOTAL_REQUESTS HTTP requests to a URL
	in multithreaded mode.
	Each request is executed in a separate thread via a ThreadPoolExecutor.
	"""
	def fetch(_: int) -> None:
		"""
		The function executes a single HTTP request in a thread.
		"""
		response = requests.get(URL)
		assert response.status_code == 200
	
	with ThreadPoolExecutor() as executor:
		list(executor.map(fetch, range(TOTAL_REQUESTS)))


def fetch(i: int, url=URL) -> None:
	"""
	The function for multiprocessing: executes a single HTTP request.
	Args:
		i (int): Sequence number of the request (for logging).
		url (str): URL to download.
	"""
	response = requests.get(url, timeout=5)
	if response.status_code != 200:
		print(f"#{i}: статус {response.status_code}")


def process_requests() -> None:
	"""
	The function executes TOTAL_REQUESTS HTTP requests to a URL
	in multiprocessing mode.
	Each request is executed in a separate process via a ProcessPoolExecutor.
	"""
	with ProcessPoolExecutor() as executor:
		list(executor.map(fetch, range(TOTAL_REQUESTS)))


# Async mode
async def async_requests() -> None:
	"""
	Executes TOTAL_REQUESTS HTTP requests to a URL asynchronously.
	Uses aiohttp and asyncio.gather for parallel execution.
	"""
	async with aiohttp.ClientSession() as session:
		async def fetch(_: int) -> None:
			async with session.get(URL) as response:
				assert response.status == 200
		
		tasks = [fetch(i) for i in range(TOTAL_REQUESTS)]
		await asyncio.gather(*tasks)


def measure(label: str, func) -> None:
	"""
	The function measures the execution time of a synchronous function.
	Args:
		label (str): The name of the mode to output.
		func (Callable): A synchronous function with no arguments.
	"""
	print(f"\nStarting: {label}")
	start = time.perf_counter()
	func()
	elapsed = time.perf_counter() - start
	print(f"{label} completed in {elapsed:.2f} sec")


def measure_async(label: str, coro) -> None:
	"""
	The function measures the execution time of an asynchronous function.
	Args:
		label (str): The name of the mode to output.
		coro (Callable): An asynchronous function with no arguments.
	"""
	print(f"\n Starting: {label}")
	start = time.perf_counter()
	asyncio.run(coro())
	elapsed = time.perf_counter() - start
	print(f"{label} completed in {elapsed:.2f} sec")


measure("Sync mode - slow", sync_requests)
measure("Multithreading mode - fast", threaded_requests)
measure("Multiprocessing mode - slower for I/O operation", process_requests)
measure_async("Async режим - fastest", async_requests)
