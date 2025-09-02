import random
from typing import Callable


def memoize(func: Callable) -> Callable:
	"""
	The function takes a function and returns a new function that stores
	the results of the calls
	"""
	cache = {}
	
	def wrapper(*args):
		"""
		Wrapper function that caches results of the original function.
		Args: *args (Any): Arguments passed to the original function.
        Returns: Any: Result from cache or computed by the original function.
		"""
		if args in cache:
			return cache[args]
		result = func(*args)
		cache[args] = result
		return result
	
	return wrapper


@memoize
def factorial(number: int) -> int:
	"""
	The function calculates the factorial of the non-negative integer.
	"""
	result = 1
	for next_number in range(2, number + 1):
		result *= next_number
	return result


for i in range(0, 10):
	number_in_order = random.randint(0, 100)
	print(f"The factorial of the number {number_in_order} is "
	      f"'{factorial(number_in_order)}'")
