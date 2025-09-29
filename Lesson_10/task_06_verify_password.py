import re

import pytest
from assertpy import assert_that


def is_strong_password(password: str) -> bool:
	"""
	The function checks whether the given password is strong.
	A strong password must:
	- Be at least 8 characters long
	- Contain at least one digit
	- Contain at least one uppercase letter
	- Contain at least one lowercase letter
	- Contain at least one special character (@, #, $, %, &, etc.)
	Parameters:
	- password (str): The password string to validate.
	Returns:
	- bool: True if the password is strong, False otherwise.
	"""
	if len(password) < 8:
		return False
	if not re.search(r"\d", password):
		return False
	if not re.search(r"[A-Z]", password):
		return False
	if not re.search(r"[a-z]", password):
		return False
	if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
		return False
	return True


@pytest.mark.parametrize("password, expected_result", [
	pytest.param("Abc123$%", True, id="TC_05_01: valid password"),
	pytest.param("A1b$", False, id="TC_05_02: less 8 simbols"),
	pytest.param("Abcdef$%", False, id="TC_05_03: password without numbers"),
	pytest.param("abc123$%", False,
	             id="TC_05_04: password without upper letter"),
	pytest.param("ABC123$%", False,
	             id="TC_05_05: password without little letter"),
	pytest.param("Abc12345", False,
	             id="TC_05_06: password without special characters"),
	pytest.param("12345678", False, id="TC_05_07: password with number only"),
	pytest.param("", False, id="TC_05_08: empty string"),
])
def test_is_strong_password(password, expected_result):
	assert_that(is_strong_password(password) == expected_result,
	            f"Error: unexpected result "
	            f"{is_strong_password(password)}").is_true()
