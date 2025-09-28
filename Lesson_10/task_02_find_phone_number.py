import re
from typing import List

import pytest
from assertpy import assert_that


def find_phone_numbers(text: str) -> List[str]:
	"""
	The function Extracts all phone numbers from the given text.
	Supported formats: (123) 456-7890, 123-456-7890, 123.456.7890, 1234567890
	Parameters:
	- text (str): The input text to search for phone numbers.
	Returns:
	- List[str]: A list of matched phone numbers.
	"""
	pattern = r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
	return re.findall(pattern, text)


@pytest.mark.parametrize("text, expected_result", [
	pytest.param("Call (123) 456-7890", ["(123) 456-7890"],
	             id="TC_02_01: verify format '(***) ***-****'"),
	pytest.param("Numbers: 123-456-7890, 123.456.7890",
	             ["123-456-7890", "123.456.7890"],
	             id="TC_02_02: verify formats '***-***-****' and '***.***.****'"),
	pytest.param("Raw: 1234567890", ["1234567890"],
	             id="TC_02_03: verify format '**********'"),
	pytest.param("Mixed: (123)456-7890 and 123 456 7890",
	             ["(123)456-7890", "123 456 7890"],
	             id="TC_02_04: verify mix of formats"),
	pytest.param("Call to ant phone number.", [],
	             id="TC_02_05: verify that phone numbers are not exist in text"),
	pytest.param("", [], id="TC_02_06: verify empty text"),
])
def test_find_phone_numbers(text, expected_result):
	(assert_that(find_phone_numbers(text),
	             f"Error: unexpected result {expected_result}").
	 is_equal_to(expected_result))
