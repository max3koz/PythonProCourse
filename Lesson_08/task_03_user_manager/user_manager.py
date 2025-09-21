class UserManager:
	"""
	Class for managing users.
	"""
	
	def __init__(self):
		self._users = {}
	
	def add_user(self, name: str, age: int) -> None:
		"""Adds a user by name."""
		self._users[name] = age
	
	def remove_user(self, name: str) -> None:
		"""Deletes a user by name."""
		self._users.pop(name, None)
	
	def get_all_users(self) -> list:
		"""Returns a list of all users in the format (name, age)."""
		return [(name, age) for name, age in self._users.items()]
