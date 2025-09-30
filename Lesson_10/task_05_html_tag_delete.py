import re
from typing import Optional

import pytest
from assertpy import assert_that


def delete_html_tags(text: str) -> Optional[str]:
	"""
	The function delete all HTML tags from the given text.
	Parameters:
	- text (str): The input string containing HTML content.
	Returns:
	- Optional[str]: The cleaned text without any HTML tags.
	"""
	if not text:
		return None
	return re.sub(r"<[^>]+>", "", text)


@pytest.mark.parametrize("html, expected_result", [
	pytest.param("<p>Hello <strong>world</strong></p>", "Hello world",
	             id="TC_05_01: basic test with simple tags"),
	pytest.param("<div><a href='#'>Click here</a></div>", "Click here",
	             id="TC_05_02: nested tags with attributes"),
	pytest.param("<span>Text</span> with <br> line break",
	             "Text with  line break",
	             id="TC_05_03: self-closing tag <br> and text"),
	pytest.param("No tags here", "No tags here",
	             id="TC_05_04: text without HTML tags"),
	pytest.param("", None, id="TC_05_05: empty string"),
])
def test_remove_html_tags(html, expected_result):
	assert_that(delete_html_tags(html),
	            f"Error: unexpected result {delete_html_tags(html)}").is_equal_to(
		expected_result)
