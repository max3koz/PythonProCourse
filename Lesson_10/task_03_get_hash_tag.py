import re
from typing import List

import pytest
from assertpy import assert_that


def extract_hashtags(text: str) -> List[str]:
	"""
	The function extracts all valid hashtags from the given text.
	A valid hashtag:
	- Starts with '#'
	- Followed by one or more letters or digits (no symbols, no underscores)
	- Does not include punctuation or whitespace
	Parameters:
	- text (str): The input text to search for hashtags.
	Returns:
	- List[str]: A list of valid hashtags found in the text.
	"""
	pattern = r"(?<!\w)#([a-zA-Z0-9]+)(?![\w-])"
	return [f"#{match.group(1)}" for match in re.finditer(pattern, text)]


@pytest.mark.parametrize("text, expected_result", [
	pytest.param("Check out #Python3 and #2025!", ["#Python3", "#2025"],
	             id="TC_03_01: positive test 1"),
	pytest.param("#123 #abc123 #ABC", ["#123", "#abc123", "#ABC"],
	             id="TC_03_02: positive test 2"),
	pytest.param("We are launching a new initiative next week. Stay tuned!",
	             [], id="TC_03_03: not exist hash tag"),
	pytest.param("Mixed #valid1, #not-valid, and #alsoValid",
	             ["#valid1", "#alsoValid"],
	             id="TC_03_04: mix test with valid and invalid hash tag"),
])
def test_extract_hashtags(text, expected_result):
	(assert_that(extract_hashtags(text),
	             f"Error: unexpected result {extract_hashtags(text)}").
	 is_equal_to(expected_result))
