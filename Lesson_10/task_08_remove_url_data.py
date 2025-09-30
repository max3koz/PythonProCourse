import re
from typing import List

import pytest
from assertpy import assert_that


def extract_urls(text: str) -> List[str]:
	"""
	The function extracts all URLs from the given text.
	Supports both http/https and www-style links. The function uses a regular expression
	to identify URLs that start with 'http', 'https', or 'www'.
	Args:
		text (str): Input string containing potential URLs.
	Returns:
		List[str]: A list of all matched URLs found in the text.
	"""
	url_pattern = re.compile(r'(https?://[^\s]+|www\.[^\s]+)', re.IGNORECASE)
	raw_urls = url_pattern.findall(text)
	return [url.rstrip('.,;:!?') for url in raw_urls]


@pytest.mark.parametrize("text,expected_result", [
	pytest.param("Check out https://example.com and http://test.org",
	             ["https://example.com", "http://test.org"],
	             id="TC_08_01: get 'http' and 'https' URL from the text."),
	pytest.param("Visit www.google.com or www.github.com for more info.",
	             ["www.google.com", "www.github.com"],
	             id="TC_08_02: get 'www' URL from the text"),
	pytest.param("No links here, just plain text.", [],
	             id="TC_08_03: text without URL"),
	pytest.param("Mixed content: https://site.com, www.site.org, and "
	             "ftp://ignored.com", ["https://site.com", "www.site.org"],
	             id="TC_08_04: text with valid and invalid links for removing"),
	pytest.param("URL with query params: "
	             "https://example.com/page?query=123&lang=en",
	             ["https://example.com/page?query=123&lang=en"],
	             id="TC_08_05: linls with query params"),
])
def test_extract_urls(text, expected_result):
	assert_that(extract_urls(text),
	            f"Error: unexpected result {extract_urls(text)}").is_equal_to(
		expected_result)
