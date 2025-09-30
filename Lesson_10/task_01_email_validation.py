import re

import pytest
from assertpy import assert_that


def is_valid_email(email: str) -> bool:
	"""
	Validates whether the given email address matches the expected format.
	Format requirements:
	- Local part (before @): letters, digits, or dots (dot cannot be first or last).
	- Domain part (after @): letters or digits only.
	- TLD: 2 to 6 letters.
	Parameters:
	- email (str): The email address to validate.
	Returns:
	- bool: True if the email is valid, False otherwise.
	"""
	pattern = r"^(?!\.)([\w\.]+)(?<!\.)@([a-zA-Z0-9]+)\.([a-zA-Z]{2,6})$"
	return bool(re.fullmatch(pattern, email))


@pytest.mark.parametrize("email, expected_result", [
	pytest.param("user@example.com", True,
	             id="TC_01_01: positive test with 'user@example.com'"),
	pytest.param("john.doe@domain.net", True,
	             id="TC_01_02: positive test with dot in name"),
	pytest.param("a.b.c@abc.org", True,
	             id="TC_01_03: positive test with two dot in name"),
	pytest.param("user@domain.c", False,
	             id="TC_01_04: negative test - TLD too short"),
	pytest.param("user@domain.company", False,
	             id="TC_01_05: negative test - TLD too long"),
	pytest.param(".user@domain.com", False,
	             id="TC_01_06: negative test - dot at start"),
	pytest.param("user.@domain.com", False,
	             id="TC_01_07: negative test - dot at end"),
	pytest.param("user@do_main.com", False,
	             id="TC_01_08: negative test - underscore in domain"),
	pytest.param("user@domain", False,
	             id="TC_01_09: negative test - missing TLD"),
	pytest.param("user@domain.123", False,
	             id="TC_01_10: negative test - numeric TLD"),
	pytest.param("user@domain.c0m", False,
	             id="TC_01_11: negative test - mixed TLD"),
	pytest.param("user@domain..com", False,
	             id="TC_01_12: negative test - double dot in domain")
])
def test_is_valid_email(email, expected_result):
	assert_that(is_valid_email(email) == expected_result,
	            f"Error: unexpected result {expected_result}").is_true()
