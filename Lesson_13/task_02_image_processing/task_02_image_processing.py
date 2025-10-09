import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
from typing import Optional

import requests
from PIL import Image, ImageFilter

OUTPUT_FOLDER: str = "processed"
TARGET_SIZE: Tuple[int, int] = (800, 600)


def download_image(url: str, save_dir: str = "images",
                   filename: Optional[str] = None) -> None:
	"""
	The function downloads an image from a URL and saves it to the specified directory.
	Args:
		- url (str): Link to the image.
		- save_dir (str): Name of the directory to save to (default "images").
		- filename (Optional[str]): Name of the file to save. If None, the name
		from the URL is used.
	"""
	try:
		response = requests.get(url)
		response.raise_for_status()
		
		if "image" not in response.headers.get("Content-Type", ""):
			print(f"It is not image: {url}")
			return None
		
		os.makedirs(save_dir, exist_ok=True)
		if filename is None:
			filename = os.path.basename(url.split("/")[0])
		
		path = os.path.join(save_dir, filename)
		
		with open(path, "wb") as file:
			for chunk in response.iter_content(chunk_size=8192):
				file.write(chunk)
		
		print(f"Downloaded: {path}")
		return path
	except requests.RequestException as e:
		print(f"Error: download error from {url}: {e}")
		return None


def process_image(image_path: str, output_dir: str,
                  size: Tuple[int, int]) -> None:
	"""
	The function processes a single image: resizes and applies a blur filter.
	Args:
		- image_path (str): Path to the input image.
		- output_dir (str): Directory to save the processed image.
		- size (Tuple[int, int]): New image size (width, height).
	"""
	try:
		with Image.open(image_path) as image:
			image_resized = image.resize(size)
			image_filtered = image_resized.filter(
				ImageFilter.GaussianBlur(radius=2))
			
			os.makedirs(output_dir, exist_ok=True)
			output_path = os.path.join(output_dir, os.path.basename(image_path))
			image_filtered.save(output_path)
			
			print(f"Processed: {output_path}")
	except Exception as e:
		print(f"Error: processing error {image_path}: {e}")


def process_images_concurrently(image_paths: List[str],
                                output_dir: str,
                                size: Tuple[int, int]) -> None:
	"""
	The function processes a list of images simultaneously using threads.
	Args:
		- image_paths (List[str]): List of image paths.
		- output_dir (str): Directory to store the results in.
		- size (Tuple[int, int]): New size for all images.
	"""
	with ThreadPoolExecutor() as executor:
		for path in image_paths:
			executor.submit(process_image, path, output_dir, size)


input_url_images: List[str] = [
	"https://yavuzceliker.github.io/sample-images/image-1021.jpg",
	"https://yavuzceliker.github.io/sample-images/image-1055.jpg",
	"https://yavuzceliker.github.io/sample-images/image-1100.jpg",
	"https://yavuzceliker.github.io/sample-images/image-1150.jpg",
	"https://yavuzceliker.github.io/sample-images/image-1200.jpg"
]

input_images = []
for item in input_url_images:
	input_images.append(download_image(url=item, save_dir="images",
	                                   filename=item.split("/")[-1])
	                    )

process_images_concurrently(input_images, OUTPUT_FOLDER, TARGET_SIZE)
