import asyncio
import time
from typing import List

import aiohttp
import pytest
from assertpy import assert_that

image_sources: List[tuple[str, str]] = [
	("https://yavuzceliker.github.io/sample-images/image-1021.jpg",
	 "image1.jpg"),
	("https://yavuzceliker.github.io/sample-images/image-1055.jpg",
	 "image2.jpg"),
	("https://yavuzceliker.github.io/sample-images/image-1100.jpg",
	 "image3.jpg"),
	("https://yavuzceliker.github.io/sample-images/image-1121.jpg",
	 "image4.jpg"),
	("https://yavuzceliker.github.io/sample-images/image-1155.jpg",
	 "image5.jpg"),
	("https://yavuzceliker.github.io/sample-images/image-1200.jpg",
	 "image6.jpg"),
]


@pytest.mark.asyncio
async def test_real_image_download_parallel_start():
	"""Verify that all actual image downloads start at the same time."""
	start_times: dict[str, float] = {}
	
	async def download_image(url: str, filename: str) -> None:
		start_times[filename] = time.perf_counter()
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				response.raise_for_status()
				image_data = await response.read()
				with open(filename, 'wb') as file:
					file.write(image_data)
	
	tasks = [asyncio.create_task(download_image(url, filename))
	         for url, filename in image_sources]
	
	await asyncio.gather(*tasks)
	
	times = list(start_times.values())
	earliest = min(times)
	latest = max(times)
	delta = latest - earliest
	
	print(f" Different between startes: {delta:.6f} сек")
	
	assert_that(delta < 0.01,
	            f"The tasks did not start at the same time "
	            f"(difference {delta:.4f} sec)").is_true()
