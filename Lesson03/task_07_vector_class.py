import math

from assertpy import assert_that
from typing import List


class Vector:
	"""
	The class representing a vector in n-dimensional space.
	Supports addition, subtraction, dot product, and length comparison.
	"""
	
	def __init__(self, components: List[float]) -> None:
		"""Initializes a vector with the passed components."""
		self.components = components
	
	def __add__(self, other: 'Vector') -> 'Vector':
		"""
		Adds two vectors component by component.
		Returns: Vector: The new vector is the sum.
		"""
		self._validate_dimension(other)
		result = []
		for index in range(len(self.components)):
			result.append(self.components[index] + other.components[index])
		return Vector(result)
	
	def __sub__(self, other: 'Vector') -> 'Vector':
		"""
		Subtracts two vectors component by component.
		Returns: Vector: The new vector is the difference.
		"""
		self._validate_dimension(other)
		result = []
		for index in range(len(self.components)):
			result.append(self.components[index] - other.components[index])
		return Vector(result)
	
	def __mul__(self, other: 'Vector') -> float:
		"""
		Calculates the dot product of two vectors.
		Returns: float: The dot product.
		"""
		self._validate_dimension(other)
		total = 0.0
		for index in range(len(self.components)):
			total += self.components[index] * other.components[index]
		return total
	
	def magnitude(self) -> float:
		"""Calculates the length (modulus) of a vector."""
		return math.sqrt(sum(x ** 2 for x in self.components))
	
	"""
	Methods (__lt__, __le__, __eq__, __gt__, __ge__)
	for comparing vectors by length
	"""
	
	def __eq__(self, other: object) -> bool:
		if not isinstance(other, Vector):
			return NotImplemented
		return self.magnitude() == other.magnitude()
	
	def __lt__(self, other: 'Vector') -> bool:
		return self.magnitude() < other.magnitude()
	
	def __le__(self, other: 'Vector') -> bool:
		return self.magnitude() <= other.magnitude()
	
	def __gt__(self, other: 'Vector') -> bool:
		return self.magnitude() > other.magnitude()
	
	def __ge__(self, other: 'Vector') -> bool:
		return self.magnitude() >= other.magnitude()
	
	def _validate_dimension(self, other: 'Vector') -> None:
		"""
		Checks if vectors have the same number of dimensions.
		Raises: ValueError: If the dimensions do not match.
		"""
		if len(self.components) != len(other.components):
			raise ValueError("Vectors must have the same dimension")
		
		
def test_vector_addition() -> None:
	vector_1 = Vector([1, 2 ,3])
	vector_2 = Vector([3, 4, 5])
	result_vector = vector_1 + vector_2
	assert_that(result_vector.components == [4, 6, 8],
	            f"Error: unexpected result: "
	            f"{result_vector.components}").is_equal_to(True)


def test_vector_subtraction() -> None:
	vector_1 = Vector([5, 7, 9])
	vector_2 = Vector([1, 2, 3])
	result_vector = vector_1 - vector_2
	assert_that(result_vector.components == [4, 5, 6],
	            f"Error: unexpected result: "
	            f"{result_vector.components}").is_equal_to(True)

def test_vector_dot_product() -> None:
	vector_1 = Vector([1, 2, 3])
	vector_2 = Vector([4, 5, 6])
	result_vector = vector_1 * vector_2
	assert_that(result_vector == 32,
	            f"Error: unexpected result: {result_vector}").is_equal_to(True)


def test_vector_comparison() -> None:
	vector_1 = Vector([3, 4])  # length = 5
	vector_2 = Vector([6, 8])  # length = 10
	assert_that(vector_1 < vector_2, f"Error: unexpected result: "
	                                 f"{vector_1} < {vector_2}").is_equal_to(True)
	assert_that(vector_2 > vector_1, f"Error: unexpected result: "
	                                 f"{vector_2} > {vector_1}").is_equal_to(True)
	assert_that(vector_1 <= vector_2, f"Error: unexpected result: "
	                                  f"{vector_1} <= {vector_2}").is_equal_to(True)
	assert_that(vector_2 >= vector_1, f"Error: unexpected result: "
	                                  f"{vector_2} >= {vector_1}").is_equal_to(True)
	assert_that(vector_1 != vector_2, f"Error: unexpected result: "
	                                  f"{vector_1} != {vector_2}").is_equal_to(True)
