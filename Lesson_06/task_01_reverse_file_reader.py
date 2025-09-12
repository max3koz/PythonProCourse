from typing import Iterator, Optional


class ReverseFileReader:
	"""
	Iterator for reading a text file in reverse order — line by line from end
	to beginning.
	Parameters:
		filename (str): Path to the text file
		encoding (str): File encoding (default ‘utf-8’)
	"""
	
	def __init__(self, filename: str, encoding: str = "utf-8") -> None:
		self.filename: str = filename
		self.encoding: str = encoding
		self._lines: Optional[list[str]] = None
		self._index: int = -1
	
	def __iter__(self) -> Iterator[str]:
		try:
			with open(self.filename, "r", encoding=self.encoding) as file:
				self.lines = file.readlines()
			self.index = len(self.lines) - 1
		except FileNotFoundError:
			raise StopIteration(f"{self.filename}' file is not found.")
		return self
	
	def __next__(self) -> str:
		if self.lines is None or self.index < 0:
			raise StopIteration
		read_line = self.lines[self.index].rstrip("\n")
		self.index -= 1
		return read_line


test_file = "example.txt"
reader = ReverseFileReader(test_file)

for line in reader:
	print(f"{line}")
