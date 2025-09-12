import csv
import os
from typing import Iterator

from PIL import Image


class ImageMetadataIterator:
	"""
	An iterator that goes through all images in the directory,
	opens them using PIL, and extracts basic metadata.
	Parameters:
        folder (str): Path to the image directory
        extensions (tuple[str]): Supported extensions (default: .jpg, .png, .jpeg)
	"""
	
	def __init__(self, folder: str,
	             extensions: tuple[str, ...] = (".jpg", ".jpeg",
	                                            ".png")) -> None:
		self.folder = folder
		self.extensions = extensions
		self.files = [file for file in os.listdir(folder) if
		              file.lower().endswith(extensions)]
		self.index = 0
	
	def __iter__(self) -> Iterator[dict]:
		return self
	
	def __next__(self) -> dict:
		if self.index >= len(self.files):
			raise StopIteration
		
		filename = self.files[self.index]
		path = os.path.join(self.folder, filename)
		
		try:
			with Image.open(path) as img:
				metadata = {"filename": filename, "format": img.format,
				            "size": f"{img.width}x{img.height}",
				            "mode": img.mode}
		except Exception as e:
			metadata = {"filename": filename, "error": str(e)}
		
		self.index += 1
		return metadata


def save_metadata_to_csv(folder: str, output_csv: str) -> None:
	"""
	Save image metadata to CSV file
	"""
	iterator = ImageMetadataIterator(folder)
	with open(output_csv, "w", newline="", encoding="utf-8") as f:
		writer = csv.DictWriter(f, fieldnames=["filename", "format", "size",
		                                       "mode", "error"])
		writer.writeheader()
		for data in iterator:
			writer.writerow(data)
	print(f"Data was saved to file {output_csv}")


save_metadata_to_csv("task_03_images", "task_03_metadata.csv")
