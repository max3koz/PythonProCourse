from typing import Generic, TypeVar, List, Callable

from assertpy import assert_that

T = TypeVar("T")


class Processor(Generic[T]):
	"""
	The generic processor that applies a transformation function to each element in a list.
	Attributes:
	- data (List[T]): The list of elements to process.
	Methods:
	- apply(func: Callable[[T], T]) -> List[T]: Applies the given function
	to each element and returns the result.
	"""
	
	def __init__(self, data: List[T]) -> None:
		self.data = data
	
	def apply(self, func: Callable[[T], T]) -> List[T]:
		"""
		Applies a function to each element in the data list.
		Parameters:
		- func (Callable[[T], T]): A function that transforms an element of type T.
		Returns:
		- List[T]: A new list containing the transformed elements.
		"""
		return [func(item) for item in self.data]


def double(num: int) -> int:
	return num * 2


def to_upper(text: str) -> str:
	return text.upper()


p1 = Processor([1, 2, 3])
print(p1.apply(double))

p2 = Processor(["hello", "world"])
print(p2.apply(to_upper))


def test_processor_with_integers():
	test_processor = Processor([1, 2, 3])
	expected_result = test_processor.apply(double)
	assert_that(expected_result).is_equal_to([2, 4, 6])


def test_processor_with_strings():
	test_processor = Processor(["hello", "world"])
	expected_result = test_processor.apply(to_upper)
	assert_that(all(word.isupper() for word in expected_result)).is_true()
