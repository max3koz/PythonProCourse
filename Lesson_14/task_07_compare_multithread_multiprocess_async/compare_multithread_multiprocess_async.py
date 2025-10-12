import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import aiohttp
import requests

URL = "https://yavuzceliker.github.io/sample-images/image-1021.jpg"
TOTAL_REQUESTS = 500


# Sync mod
def sync_requests() -> None:
	for item in range(TOTAL_REQUESTS):
		response = requests.get(URL)
		if response.status_code != 200:
			print(
				f"The request #{item} returned status: {response.status_code}")
		assert response.status_code == 200


# Multithreading mode
def threaded_requests() -> None:
	def fetch(_: int) -> None:
		response = requests.get(URL)
		assert response.status_code == 200
	
	with ThreadPoolExecutor() as executor:
		list(executor.map(fetch, range(TOTAL_REQUESTS)))


# Multiprocessing mode
def fetch(i: int, url=URL) -> None:
	response = requests.get(url, timeout=5)
	if response.status_code != 200:
		print(f"#{i}: статус {response.status_code}")


def process_requests() -> None:
	with ProcessPoolExecutor() as executor:
		list(executor.map(fetch, range(TOTAL_REQUESTS)))


# Async mode
async def async_requests() -> None:
	async with aiohttp.ClientSession() as session:
		async def fetch(_: int) -> None:
			async with session.get(URL) as response:
				assert response.status == 200
		
		tasks = [fetch(i) for i in range(TOTAL_REQUESTS)]
		await asyncio.gather(*tasks)


# Time measuring
def measure(label: str, func) -> None:
	print(f"\n🔍 Starting: {label}")
	start = time.perf_counter()
	func()
	elapsed = time.perf_counter() - start
	print(f"{label} completed in {elapsed:.2f} sec")


def measure_async(label: str, coro) -> None:
	print(f"\n🔍 Starting: {label}")
	start = time.perf_counter()
	asyncio.run(coro())
	elapsed = time.perf_counter() - start
	print(f"✅ {label} completed in {elapsed:.2f} sec")


measure("Sync mode - slow", sync_requests)
measure("Multithreading mode - fast", threaded_requests)
measure("Multiprocessing mode - slower for I/O operation", process_requests)
measure_async("Async режим - fastest", async_requests)
