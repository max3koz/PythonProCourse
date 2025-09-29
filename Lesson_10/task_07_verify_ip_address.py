import re
from typing import List

import pytest
from assertpy import assert_that


def extract_ipv4_addresses(text: str) -> List[str]:
	"""
	The function extracts all valid IPv4 addresses from the given text.
	Parameters:
	- text (str): The input text to search for IPv4 addresses.
	Returns:
	- List[str]: A list of valid IPv4 addresses found in the text.
	"""
	candidate_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
	candidates = re.findall(candidate_pattern, text)
	
	valid_ips = []
	for ip in candidates:
		parts = ip.split(".")
		if all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
			valid_ips.append(ip)
	
	return valid_ips


@pytest.mark.parametrize("text, expected", [
	pytest.param("Ping 192.168.1.1 and 10.0.0.254",
	             ["192.168.1.1", "10.0.0.254"],
	             id="TC_07_01: valid IP addresses"),
	pytest.param("Invalid: 300.1.1.1, 192.168.1.256", [],
	             id="TC_07_02: IP addresses with number more 255"),
	pytest.param("Valid: 8.8.8.8, Invalid: 999.999.999.999", ["8.8.8.8"],
	             id="TC_07_03: valid and invalid IP addresses in text"),
	pytest.param("No IPs here", [],
	             id="TC_07_04: the text without IP addresses"),
	pytest.param("Check 001.002.003.004", ["001.002.003.004"],
	             id="TC_07_05: ip addresses with leading zeros"),
])
def test_extract_ipv4_addresses(text, expected):
	assert_that(extract_ipv4_addresses(text) == expected, "").is_true()
