from typing import Iterator


class LimitedWriter:
	"""
	A context manager that writes a limited number of values to a file.
	Parameters:
		filename: the path to file
		limit: Number of values for recording
	"""
	
	def __init__(self, filename: str, limit: int = 100) -> None:
		self.filename = filename
		self.limit = limit
		self.file = None
	
	def __enter__(self):
		self.file = open(self.filename, "w", encoding="utf-8")
		return self.file
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.file:
			self.file.close()


def even_numbers() -> Iterator[int]:
	"""Generates an infinite sequence of even numbers."""
	n = 0
	while True:
		yield n
		n += 2


gen = even_numbers()

test_file = "example.txt"

with LimitedWriter(test_file, limit=100) as f:
	for _ in range(100):
		f.write(str(next(gen)) + "\n")

print(f"100 even numbers are recorded in the {test_file} file.")
