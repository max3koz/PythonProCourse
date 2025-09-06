from math import sqrt
from typing import Union

from assertpy import assert_that


class Vector:
	"""
	The class representing a mathematical vector in n-dimensional space.
	Supports basic operations: addition, subtraction, multiplication by a number,
	length comparison, and length calculation.
	"""
	
	def __init__(self, coordinates: list[float]) -> None:
		"""
		Initializes a vector with the passed coordinates.
		Args: coordinates (list[float]): List of vector coordinates.
		"""
		self.coordinates = coordinates
	
	def __add__(self, other: 'Vector') -> 'Vector':
		"""
		Adds two vectors coordinate-wise.
		Args: other (Vector): Another vector.
		Returns: Vector: The result of the addition.
		"""
		result = []
		for coordinate_index in range(len(self.coordinates)):
			result.append(self.coordinates[coordinate_index] +
			              other.coordinates[coordinate_index])
		return Vector(result)
	
	def __sub__(self, other: 'Vector') -> 'Vector':
		"""
		Subtracts one vector from another coordinate-wise.
		Args: other (Vector): Another vector.
		Returns: Vector: The result of the subtraction.
		"""
		result = []
		for coordinate_index in range(len(self.coordinates)):
			result.append(self.coordinates[coordinate_index] -
			              other.coordinates[coordinate_index])
		return Vector(result)
	
	def __mul__(self, scalar: Union[int, float]) -> 'Vector':
		"""
		Multiplies a vector by a scalar.
		Args: scalar (int | float): The number to multiply the vector by.
		Returns: Vector: The result of the multiplication.
		"""
		result = [number * scalar for number in self.coordinates]
		return Vector(result)
	
	def lenght(self) -> float:
		"""
		Calculates the length (modulus) of a vector.
		Returns: float: The length of the vector.
		"""
		return sqrt(sum(coordinate ** 2 for coordinate in self.coordinates))
	
	def __lt__(self, other: 'Vector') -> bool:
		"""
		Compares vectors by length.
		Args: other (Vector): Another vector.
		Returns: bool: True if the current vector is shorter.
		"""
		return self.lenght() < other.lenght()
	
	def __repr__(self) -> str:
		"""
		Returns a string representation of a vector.
		Returns: str: Format "Vector([x1, x2, ...])"
		"""
		return f"Vector({self.coordinates})"


vector_1 = Vector([3, 4])
vector_2 = Vector([1, 2])

print(f"Vector 1: {vector_1}")
print(f"Vector 1: {vector_2}")

add_vector = vector_1 + vector_2
assert_that(str(add_vector),
            f"Error: unexpected result: "
            f"{add_vector}").is_equal_to("Vector([4, 6])")
sub_vector = vector_1 - vector_2
assert_that(str(sub_vector),
            f"Error: unexpected result: "
            f"{sub_vector}").is_equal_to("Vector([2, 2])")
sub_vector = vector_1 * 2
assert_that(str(sub_vector),
            f"Error: unexpected result: "
            f"{sub_vector}").is_equal_to("Vector([6, 8])")
assert_that(vector_1 == vector_2,
            f"Error: unexpected result: {sub_vector}").is_equal_to(False)
assert_that(vector_1 < vector_2,
            f"Error: unexpected result: {sub_vector}").is_equal_to(False)
assert_that(vector_1.lenght(),
            f"Error: unexpected result: {sub_vector}").is_equal_to(5.0)
