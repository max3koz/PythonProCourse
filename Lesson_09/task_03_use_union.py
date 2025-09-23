import pytest

from typing import Union, Optional, Any

from assertpy.assertpy import assert_that


def parse_input(value: Union[int, str]) -> Optional[int]:
    """
    Attempts to convert the input to an integer.
    Parameters:
    - value (Union[int, str]): The input value, either an integer or a string.
    Returns:
    - Optional[int]: The integer value if conversion is successful, otherwise None.
    """
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except ValueError:
        return None


@pytest.mark.parametrize("input_value, expected_result", [
    pytest.param(42, 42, id="TC03_01: integer input"),
    pytest.param("100", 100, id="TC03_02: numeric string"),
    pytest.param("hello", None, id="TC03_03: non-numeric string"),
    pytest.param("", None, id="TC03_04: empty string"),
    pytest.param("-25", -25, id="TC03_05: negative string"),
    pytest.param("3.14", None, id="TC03_06: float string"),
    pytest.param("0", 0, id="TC03_07: zero string"),
])
def test_parse_input(input_value: Any, expected_result: int | None):
    assert_that(parse_input(input_value) == expected_result).is_true()