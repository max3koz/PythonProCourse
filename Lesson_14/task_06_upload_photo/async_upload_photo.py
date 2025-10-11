import asyncio
from typing import List

import aiohttp


async def download_image(url: str, filename: str) -> None:
	"""
	The function downloads an image from the specified URL and saves it to a file.
	Args:
		url (str): The URL of the image to download.
		filename (str): The name of the file to which the image will be saved.
	"""
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			response.raise_for_status()  # Піднімає виняток, якщо статус не 200
			image_data: bytes = await response.read()
			with open(filename, 'wb') as file:
				file.write(image_data)
			print(f"✅ Downloaded: {filename}")


async def main() -> None:
	"""Creates a list of tasks to load images simultaneously."""
	image_sources: List[tuple[str, str]] = [
		("https://yavuzceliker.github.io/sample-images/image-1021.jpg",
		 "image1.jpg"),
		("https://yavuzceliker.github.io/sample-images/image-1055.jpg",
		 "image2.jpg"),
		("https://yavuzceliker.github.io/sample-images/image-1100.jpg",
		 "image3.jpg"),
	]
	
	tasks: List[asyncio.Task] = [
		asyncio.create_task(download_image(url, filename))
		for url, filename in image_sources
	]
	
	await asyncio.gather(*tasks)
	print("All images are uploaded!")


if __name__ == "__main__":
	asyncio.run(main())
