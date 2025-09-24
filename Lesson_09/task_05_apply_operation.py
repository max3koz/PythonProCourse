from typing import Callable

import pytest
from assertpy.assertpy import assert_that


def apply_operation(x: int, operation: Callable[[int], int]) -> int:
	"""
	Applies a given operation to an integer.
	Parameters:
	- x (int): The input number.
	- operation (Callable[[int], int]): A function that takes an integer and returns an integer.
	Returns:
	- int: The result of applying the operation to x.
	"""
	return operation(x)


def square(n: int) -> int:
	"""Returns the square of a number."""
	return n * n


def double(n: int) -> int:
	"""Returns double the value of a number."""
	return n * 2


@pytest.mark.parametrize("test_number, operation, expected_result", [
	pytest.param(5, square, 25,
	             id="TC_05_01: operation 'square' with positive number"),
	pytest.param(5, double, 10,
	             id="TC_05_02: operation 'double' with positive number"),
	pytest.param(0, square, 0, id="TC_05_03: operation 'square' with 0"),
	pytest.param(0, double, 0, id="TC_05_04 operation 'double' with 0"),
	pytest.param(-4, square, 16,
	             id="TC_05_05 operation 'square' with negative number"),
	pytest.param(-3, double, -6,
	             id="TC_05_06: operation 'double' with negative number")
])
def test_apply_operation(test_number, operation, expected_result):
	actual_result = apply_operation(test_number, operation)
	assert_that(actual_result == expected_result,
	            f"Error: unexpected result - {expected_result}").is_true()
