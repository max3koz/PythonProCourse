import pytest


def calculate_discount(price: float, discount: float) -> float:
	"""
	Calculates the final price after applying a discount.
	Parameters:
	- price (float): The original price of the item.
	- discount (float): The discount percentage to apply.
	Returns:
	- float: The final price after discount. Returns 0.0 if discount exceeds 100%.
	"""
	if discount > 100:
		return 0.0
	return price * (1 - discount / 100)


@pytest.mark.parametrize("test_price, test_discount, expected_result", [
	pytest.param(100, 20, 80.00, id="TC01_01: discount less then 100%"),
	pytest.param(100, 99, 1.00, id="TC01_02: discount 99%"),
	pytest.param(100, 100, 0.00, id="TC01_03: discount 100%"),
	pytest.param(100, 101, 0.00, id="TC01_04: discount 101%")
])
def test_function_calculate_discount(test_price: float, test_discount: float,
                                     expected_result: float):
	actual_result = calculate_discount(test_price, test_discount)
	assert_that(actual_result).is_close_to(expected_result, tolerance=0.001)


from typing import List, Tuple


def filter_adults(people: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
	"""
	Filters out underage individuals from a list of people.
	Parameters:
	- people (List[Tuple[str, int]]): A list of tuples, each containing
	  a person's name and age.
	Returns:
	- List[Tuple[str, int]]: A list containing only those individuals who are
	  18 years old or older.
	"""
	return [person for person in people if person[1] >= 18]


def test_filter_adults_basic():
	test_people_data = [("Андрій", 25),
	                    ("Олег", 16),
	                    ("Марія", 19),
	                    ("Ірина", 15)]
	expected_result = [("Андрій", 25),
	                   ("Марія", 19)]
	actual_result = filter_adults(test_people_data)
	assert_that(actual_result == expected_result).is_true()


def test_filter_adults_empty_list():
	test_people_data = []
	expected_result = []
	actual_result = filter_adults(test_people_data)
	assert_that(actual_result == expected_result).is_true()


import pytest

from typing import Union, Optional, Any


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


from typing import List, TypeVar, Optional

import pytest

T = TypeVar("T")


def get_first(items: List[T]) -> Optional[T]:
	"""
	The function returns the first element of a list, or None if the list is empty.
	Parameters:
	- items (List[T]): A list of elements of any type.
	- returned_element: int - the number of element which need to return,
	Returns:
	- Optional[T]: The first element of the list, or None if the list is empty.
	"""
	first_element_index: int = 0
	return items[first_element_index] if items else None


@pytest.mark.parametrize("input_list, expected_result", [
	pytest.param([1, 2, 3], 1,
	             id="TC_04_01: the 1st element is integer"),
	pytest.param(["a", "b", "c"], "a",
	             id="TC_04_02: the 1st element is letter"),
	pytest.param([], None,
	             id="TC_04_03: verify the working with empty list"),
	pytest.param([True, False], True,
	             id="TC_04_04: the 1st element is bool"),
	pytest.param([{"name": "Maksym"}, {"name": "Oleh"}], {"name": "Maksym"},
	             id="TC_04_05: the 1st element is dictionary")
])
def test_get_first(input_list, expected_result):
	actual_result = get_first(input_list)


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
	
	assert_that(actual_result == expected_result,
	            f"Error: wrong value of 1st element {actual_result}").is_true()
