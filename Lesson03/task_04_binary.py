import pytest
from assertpy import assert_that


class BinaryNumber:
	"""
	The class that represents a binary number and supports logical operations:
	AND (&), OR (|), XOR (^), NOT (~).
	"""
	
	def __init__(self, value: int) -> None:
		"""
		Initializes a BinaryNumber object.
		Args: value (int): The integer to be represented in binary form
		"""
		if value < 0:
			raise ValueError("BinaryNumber must be non-negative")
		self.value = value
	
	def __and__(self, other: 'BinaryNumber') -> 'BinaryNumber':
		"""
		Bitwise AND operation.
		Returns: Binary Number: Result of the operation self and other.
		"""
		return BinaryNumber(self.value & other.value)
	
	def __or__(self, other: 'BinaryNumber') -> 'BinaryNumber':
		"""
		BBitwise OR operation.
		Returns: BinaryNumber: Result of the operation self | other.
		"""
		return BinaryNumber(self.value | other.value)
	
	def __xor__(self, other: 'BinaryNumber') -> 'BinaryNumber':
		"""
		BBitwise XOR operation.
		Returns: BinaryNumber: Result of the operation self ^ other.
		"""
		return BinaryNumber(self.value ^ other.value)
	
	def __invert__(self) -> 'BinaryNumber':
		"""
		Bitwise NOT operation (inversion). Returns the inversion within the bit
		length of the number.
		Returns: BinaryNumber: The result of the ~self operation.
		"""
		bit_lenght = self.value.bit_length()
		mask = (1 << bit_lenght) - 1
		return BinaryNumber(~self.value & mask)
	
	def __repr__(self) -> str:
		"""
		Returns a string representation in binary format.
		Returns: str: For example, "BinaryNumber(0b1010)"
		"""
		return f"BinaryNumber({bin(self.value)})"


@pytest.mark.parametrize("binary_operation, expected_result", [
	pytest.param("and", 0b1000,
	             id="TC_04_01: Verify that Binary ADD operation run as expected"),
	pytest.param("or", 0b1110,
	             id="TC_04_02: Verify that Binary OR operation run as expected"),
	pytest.param("xor", 0b0110,
	             id="TC_04_03:Verify that Binary XOR operation run as expected"),
	pytest.param("inversion", 0b0101,
	             id="TC_04_04:Verify that Binary inversion operation run as expected"),
])
def test_binary_operation(binary_operation, expected_result) -> None:
	"""
	The test case checks logical operations on BinaryNumber objects.
	Parameters:
	binary_operation (str): The name of the operation to be performed;
	Possible values: "and", "or", "xor", "inversion";
	expected_result (int): The expected integer value after the operation.
	"""
	number_1 = BinaryNumber(0b1010)
	number_2 = BinaryNumber(0b1100)
	if binary_operation == "and":
		result = number_1 & number_2
	elif binary_operation == "or":
		result = number_1 | number_2
	elif binary_operation == "xor":
		result = number_1 ^ number_2
	elif binary_operation == "inversion":
		result = ~number_1
	else:
		raise ValueError(f"Unknown operation: {binary_operation}")
	
	assert_that(result.value == expected_result,
	            f"Error: {binary_operation.upper()} failed, the result is: "
	            f"{bin(result.value)}").is_true()
