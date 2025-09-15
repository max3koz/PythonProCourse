import os
import random


class BinaryBlockReader:
	"""
	Context manager for reading a binary file in blocks.
	Parameters:
		filepath: Path to the binary file
		block_size: Block size in bytes (default is 1024)
	"""
	
	def __init__(self, filepath: str, block_size: int = 1024) -> None:
		self.filepath = filepath
		self.block_size = block_size
		self.file = None
	
	def __enter__(self):
		self.file = open(self.filepath, "rb")
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		if self.file:
			self.file.close()
	
	def read_blocks(self):
		"""
		Generates data blocks from a file.
		"""
		while True:
			chunk = self.file.read(self.block_size)
			if not chunk:
				break
			yield chunk


def generate_binary_file(filename: str, size_in_kb: int) -> None:
	"""
	Creates a binary file of a specified size with random bytes.
	It needs for testing.
	Parameters:
		filename: File name
		size_in_kb: Size in kilobytes
	"""
	total_bytes_in_file = random.randint(123, size_in_kb)
	with open(filename, "wb") as f:
		f.write(os.urandom(total_bytes_in_file))
	print(
		f"Created the '{filename}' file with a size of {total_bytes_in_file} bytes")


test_file = "task_12_data.bin"
generate_binary_file(test_file, size_in_kb=10000)

total_bytes = 0
count = 0
try:
	with BinaryBlockReader(test_file, block_size=1024) as reader:
		for block in reader.read_blocks():
			total_bytes += len(block)
			count += 1
			print(f"Read block {count}: {len(block)} bytes")
	
	print(f"Total read: {total_bytes} bytes.")

except FileNotFoundError:
	print(f"The {test_file} is not found.")
except Exception as e:
	print(f"Error: {e}")
