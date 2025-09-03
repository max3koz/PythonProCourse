from typing import Iterator

import pytest
from assertpy import assert_that


class CustomList:
	"""
	A class that mimics the behavior of a list and implements its own versions
	of the functions:
	custom_len(), custom_sum(), custom_min().
	Supports iteration, indexing, and length calculations.
	"""
	
	def __init__(self, items: list[int]) -> None:
		"""
		Initializes a CustomList object.
		Args: items (list[int]): A list of integers.
		"""
		self.items = items
	
	def __len__(self) -> int:
		"""
		Returns the number of elements in a list.
		Returns: int: The length of the list.
		"""
		return len(self.items)
	
	def __getitem__(self, index: int) -> int:
		"""
		Allows access to elements by index.
		Args: index (int): The index of the element.
		Returns: int: The value of the element.
		"""
		return self.items[index]
	
	def __iter__(self) -> Iterator[int]:
		"""
		Allows iterating over elements.
		Returns: Iterator[int]: Iterator over the list.
		"""
		return iter(self.items)
	
	def custom_len(self) -> int:
		"""
		Custom implementation of the len() function without using __len__
		via generator.
		Returns: int: Number of elements in the list.
		"""
		return sum(1 for _ in self)
	
	def custom_sum(self) -> int:
		"""
		Custom implementation of the sum() function.
		Returns: int: The sum of all elements.
		"""
		total = 0
		for item in self:
			total += item
		return total
	
	def custom_min(self) -> int | ValueError:
		"""
		Custom implementation of the min() function.
		Returns: int: The minimum value among the elements.
		Raises: ValueError: If the list is empty.
		"""
		if self.custom_len() == 0:
			return ValueError("Not possible to find min in the empty list.")
		min_num = self[0]
		for item in self:
			if item < min_num:
				min_num = item
		return min_num


@pytest.mark.parametrize("custom_function, test_list", [
	pytest.param("len_custom_func", [3, 6, 4, 1, 10],
	             id="TC_05_01: Verify that custom 'len' function run as expected"),
	pytest.param("sum_custom_func", [3, 8, 4, 1],
	             id="TC_05_02: Verify that custom 'sum' function run as expected"),
	pytest.param("min_custom_func", [5, 6, 4, 1, 10],
	             id="TC_05_03: Verify that custom 'min' function run as expected")
])
def test_custom_function_len(custom_function, test_list):
	data = CustomList(test_list)
	if custom_function == "len_custom_func":
		expected_result = len(data)
		actual_result = data.custom_len()
	elif custom_function == "sum_custom_func":
		expected_result = sum(data)
		actual_result = data.custom_sum()
	elif custom_function == "min_custom_func":
		expected_result = min(data)
		actual_result = data.custom_min()
	else:
		raise ValueError(f"Unknown custom function: {custom_function}")
	assert_that(expected_result == actual_result,
	            f"Error: expected result: {expected_result}, "
	            f"actual result: {actual_result}").is_true()
