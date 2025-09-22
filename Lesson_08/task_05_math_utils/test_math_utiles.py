import pytest
from assertpy import assert_that

from .math_utils import divide


def test_divide_normal():
	"""Positive test case"""
	expected_result = 5.0
	actual_result = divide(10, 2)
	assert_that(expected_result == actual_result,
	            "Something wrong!").is_true()


def test_divide_zero_division():
	"""Negative test case."""
	num_1 = 5.0
	num_zero = 0
	assert_that(lambda: divide(num_1, num_zero)).raises(ZeroDivisionError)


@pytest.mark.parametrize("num_1, num_2, expected_result", [
	pytest.param(10, 2, 5.0, id="TC_01_01"),
	pytest.param(9, 3, 3.0, id="TC_01_02"),
	pytest.param(-8, 2, -4.0, id="TC_01_03"),
	pytest.param(7, -1, -7.0, id="TC_01_04"),
	pytest.param(0, 1, 0.0, id="TC_01_05"),
])
def test_divide_parametrized(num_1, num_2, expected_result):
	"""Parametrized test case"""
	assert_that(divide(num_1, num_2) == expected_result,
	            "Something wrong!").is_true()
