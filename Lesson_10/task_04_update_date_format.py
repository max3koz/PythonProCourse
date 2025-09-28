from typing import Optional
import re
import pytest
from assertpy import assert_that


def convert_date_format(date_str: str) -> Optional[str]:
	"""
	The function converts a date from DD/MM/YYYY format to YYYY-MM-DD format.
	Parameters:
	- date_str (str): The input date string in DD/MM/YYYY format.
	Returns:
	- Optional[str]: The converted date string in YYYY-MM-DD format,
	  or None if the input format is invalid.
	"""
	pattern = r"^(\d{2})/(\d{2})/(\d{4})$"
	match = re.match(pattern, date_str)
	if match:
		day, month, year = match.groups()
		return f"{year}-{month}-{day}"
	return None


@pytest.mark.parametrize("input_date, expected_result", [
	pytest.param("01/01/2020", "2020-01-01",
	             id="TC_04_01: positive test 1"),
	pytest.param("31/12/1999", "1999-12-31",
	             id="TC_04_02: positive test 2"),
	pytest.param("5/9/2025", None,
	             id="TC_04_03: negative format - invalid format"),
	pytest.param("2025/09/28", None,
	             id="TC_04_04: negative format - incorrect order"),
	pytest.param("", None,
	             id="TC_04_05: negative format - empty string"),
])
def test_convert_date_format(input_date, expected_result):
	assert_that(convert_date_format(input_date),
	            f"Error: unexpected result "
	            f"{convert_date_format(input_date)}").is_equal_to(expected_result)
