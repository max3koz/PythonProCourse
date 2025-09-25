from typing import List, TypeVar, Optional

import pytest
from assertpy.assertpy import assert_that

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
	assert_that(actual_result == expected_result,
	            f"Error: wrong value of 1st element {actual_result}").is_true()
