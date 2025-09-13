from pathlib import Path
from typing import Iterator, Tuple


class DirectoryFileIterator:
	"""
	The iterator that goes through all files in a given directory
	and returns their names and sizes in bytes.
	Parameter:
		folder: the path to folder
	"""
	
	def __init__(self, folder: str) -> None:
		self.folder = Path(folder)
		self.files = list(self.folder.iterdir())
		self.index = 0
	
	def __iter__(self) -> Iterator[Tuple[str, int]]:
		return self
	
	def __next__(self) -> Tuple[str, int]:
		while self.index < len(self.files):
			file_path = self.files[self.index]
			self.index += 1
			
			if file_path.is_file():
				return file_path.name, file_path.stat().st_size
		
		raise StopIteration


folder_path = "../Lesson_06"
iterator = DirectoryFileIterator(folder_path)

for name, size in iterator:
	print(f"{name} — {size} byte")
