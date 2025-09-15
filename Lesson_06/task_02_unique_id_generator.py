import uuid
from typing import Iterator


class UniqueIDGenerator:
	"""
	An iterator that generates unique identifiers based on UUIDv4.
	Each iteration returns a new unique string, for example:
	‘a3f1c2e4-8b9d-4f1a-9c2e-7d3b1e2f4a5c’.
	"""
	
	def __iter__(self) -> Iterator[str]:
		return self
	
	def __next__(self) -> str:
		return str(uuid.uuid4())


unique_generator = UniqueIDGenerator()
for _ in range(5):
	print(next(unique_generator))
