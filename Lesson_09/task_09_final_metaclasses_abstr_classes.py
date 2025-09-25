from abc import ABC, abstractmethod
from typing import Dict, Any, Final, List, final


@final
class Config:
	"""
	Final configuration class that cannot be subclassed.
	Used to store application-level constants or settings.
	"""
	STORE_NUMBER: Final[int] = 30


class BaseRepository(ABC):
	"""
	Abstract base class for data repositories.
	Defines the interface for saving data.
	"""
	
	@abstractmethod
	def save(self, data: Dict[str, Any]) -> None:
		"""
		Saves the provided data.
		Parameters:
		- data (Dict[str, Any]): The data to be saved.
		"""
		pass


class ProductRepository(BaseRepository):
	"""
    Concrete implementation of BaseRepository that stores products in memory.
    """
	
	def __init__(self) -> None:
		self._storage: List[Dict[str, Any]] = []
	
	def save(self, data: Dict[str, Any]) -> None:
		if "name" not in data or "price" not in data:
			raise ValueError("Product must have 'name' and 'price'")
		enriched_data = {
			**data,
			"store_number": Config.STORE_NUMBER
		}
		self._storage.append(enriched_data)
		print(f"Product saved: {data}")
	
	def get_all(self) -> List[Dict[str, Any]]:
		""""Returns all saved products."""
		return self._storage


repo = ProductRepository()
repo.save({"name": "Product1", "price": 10.5})
repo.save({"name": "Product2", "price": 20.0})

print(repo.get_all())
