import pytest

from assertpy import assert_that


class User:
	"""
	Initializes a User object.
	Args: first_name (str): User's first name; last_name (str): User's last name;
	email (str): User's email address.
	"""
	
	def __init__(self, first_name: str, last_name: str, email: str) -> None:
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
	
	@property
	def first_name(self) -> str:
		"""Returns the users name"""
		return self._first_name
	
	@first_name.setter
	def first_name(self, value: str) -> None:
		"""Sets the users name."""
		self._first_name = value
	
	@property
	def last_name(self) -> str:
		"""Returns the users last name"""
		return self._last_name
	
	@last_name.setter
	def last_name(self, value: str) -> None:
		"""Sets the users last name."""
		self._last_name = value
	
	@property
	def email(self) -> str:
		"""Returns the users email"""
		return self._email
	
	@email.setter
	def email(self, value: str) -> None:
		"""
		Sets the users email.
		Raises: ValueError: if incorrect email format.
		"""
		if not self.is_valid_email(value):
			raise ValueError(f"Unexpected email format: {value} ")
		self._email = value
	
	def is_valid_email(self, email: str) -> bool:
		"""
		Checks the format of an email address.
		"""
		return "@" in email and "." in email.split("@")[-1]
	
	def __repr__(self) -> str:
		"""Returns a string representation of the user."""
		return f"User({self.first_name}, {self.last_name}, {self.email})"


def test_user_properties() -> None:
	user = User("Maksym", "Trykoz", "example@max.koz")
	assert_that(user.first_name == "Maksym",
	            f"Error: unexpected first name: {user.first_name}").is_true()


def test_user_properties_change() -> None:
	user = User("Maksym", "Trykoz", "example@max.koz")
	
	user.first_name = "Mark"
	user.last_name = "Ivanenko"
	user.email = "mark@ivan.enko"
	
	assert_that(user.first_name == "Mark",
	            f"Error: unexpected first name: {user.first_name}").is_true()
	assert_that(user.last_name == "Ivanenko",
	            f"Error: unexpected last name: {user.last_name}").is_true()
	assert_that(user.email == "mark@ivan.enko",
	            f"Error: unexpected email: {user.email}").is_true()


@pytest.mark.parametrize("invalid_email", [
	pytest.param("example@maxkoz",
	             id="TC_06_01: Verify the validation on  '.'"),
	pytest.param("examplemax.koz",
	             id="TC_06_02: Verify the validation on  '@'")
])
def test_negative_user_email(invalid_email) -> None:
	try:
		User("Maksym", "Trykoz", invalid_email)
		assert False, f"Unexpected expected behavior of function!!!"
	except ValueError as e:
		assert_that(str(e)).contains("Unexpected email format")
