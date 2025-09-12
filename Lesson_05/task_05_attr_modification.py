from typing import Any


class MutableClass:
	"""
	The class that allows you to dynamically add and remove object attributes.
	"""
	
	def __init__(self):
		self.name = None
	
	def add_attribute(self, name: str, value: Any) -> None:
		"""
		Adds an attribute to an object.
		"""
		setattr(self, name, value)
	
	def remove_attribute(self, name: str) -> None:
		"""
		Remove an attribute from an object.
		"""
		if hasattr(self, name):
			delattr(self, name)
		else:
			raise AttributeError(f"Attribute {name} does not exist!!!")


object = MutableClass()

object.add_attribute("name", "Python")
print(object.name)
object.remove_attribute("name")
object.remove_attribute("name")
