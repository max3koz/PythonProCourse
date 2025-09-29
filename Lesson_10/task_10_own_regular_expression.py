import re
import pytest
from assertpy import assert_that

def is_valid_mac_address(mac: str) -> bool:
    """
    The function validates whether the given string is a valid MAC address.
    Supports both colon-separated (e.g. "00:1A:2B:3C:4D:5E") and dash-separated
    (e.g. "00-1A-2B-3C-4D-5E") formats. Each segment must be two hexadecimal digits.
    Args:
        mac (str): The MAC address string to validate.
    Returns:
        bool: True if the MAC address is valid, False otherwise.
    """
    mac = mac.strip()
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return bool(pattern.fullmatch(mac))




@pytest.mark.parametrize("mac,expected_result", [
    pytest.param("00:1A:2B:3C:4D:5E", True,
                 id="TC_10_01: valid MAC with colon and upper letters"),
    pytest.param("00-1A-2B-3C-4D-5E", True,
                 id="TC_10_02: valid MAC with dash and upper letters"),
    pytest.param("00:1a:2b:3c:4d:5e", True,
                 id="TC_10_03: valid MAC with colon and lower letters"),
    pytest.param("00:1A:2B:3C:4D", False,
                 id="TC_10_04: invalid MAC with less 1 group of number"),
    pytest.param("00:1A:2B:3C:4D:5E:6F", False,
                 id="TC_10_05: invalid MAC with more 1 group of number"),
    pytest.param("00:1A:2B:3C:4D:ZZ", False,
                 id="TC_10_06: invalid MAC without invalid symbols"),
    pytest.param("001A.2B3C.4D5E", False,
                 id="TC_10_07: invalid MAC with invalid format")
])
def test_is_valid_mac_address(mac, expected_result):
    assert_that(is_valid_mac_address(mac),
                f"Error: unexpected result "
                f"{is_valid_mac_address(mac)}").is_equal_to(expected_result)