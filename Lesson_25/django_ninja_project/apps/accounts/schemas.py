from ninja import Schema


class LoginIn(Schema):
	"""
	Input schema for user login.
	Attributes:
		username (str): The username of the user attempting to log in.
		password (str): The password corresponding to the given username.
	"""
	username: str
	password: str


class LoginOut(Schema):
	"""
	Output schema for user login response.
	Attributes:
		success (bool): Indicates whether authentication was successful.
		token (str | None): Authentication token or session identifier if login succeeded.
		message (str | None): Informational message about the login attempt.
	"""
	success: bool
	token: str | None = None
	message: str | None = None
