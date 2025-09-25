from typing import TypedDict, Optional, Protocol

from assertpy import assert_that


class User(TypedDict):
	"""
	Represents a user with basic attributes.
	Attributes:
	- id (int): Unique identifier of the user.
	- name (str): Name of the user.
	- is_admin (bool): Whether the user has administrative privileges.
	"""
	id: int
	name: str
	is_admin: bool


class UserDatabase(Protocol):
	"""
	Protocol defining the interface for a user database.
	"""
	
	def get_user(self, user_id: int) -> Optional[User]:
		"""
		Retrieves a user by ID.
		Parameters:
		- user_id (int): The ID of the user to retrieve.
		Returns:
		- Optional[User]: The user if found, otherwise None.
		"""
		pass
	
	def save_user(self, user: User) -> None:
		"""
		Saves a user to the database.
		Parameters:
		- user (User): The user to save.
		"""
		pass


class InMemoryUserDB:
	"""
	Implementation of the UserDatabase protocol.
	Stores users in a dictionary keyed by user ID.
	"""
	
	def __init__(self) -> None:
		self._users: dict[int, User] = {}
	
	def get_user(self, user_id: int) -> Optional[User]:
		return self._users.get(user_id)
	
	def save_user(self, user: User) -> None:
		self._users[user["id"]] = user


def test_save_and_get_user():
	db = InMemoryUserDB()
	user: User = {"id": 1, "name": "Alice", "is_admin": False}
	db.save_user(user)
	actual_result = db.get_user(1)
	assert_that(actual_result == user,
	            f"Error: wrong result {actual_result}").is_true()


def test_get_nonexistent_user():
	db = InMemoryUserDB()
	actual_result = db.get_user(999)
	assert_that(actual_result,
	            f"Error: wrong result {actual_result}").is_none()


def test_overwrite_user():
	db = InMemoryUserDB()
	user_1: User = {"id": 1, "name": "Alice", "is_admin": False}
	user_2: User = {"id": 1, "name": "Alice Updated", "is_admin": True}
	db.save_user(user_1)
	db.save_user(user_2)
	actual_result = db.get_user(1)
	assert_that(actual_result == user_2,
	            f"Error: wrong result {actual_result}").is_true()
