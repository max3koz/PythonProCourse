import random


def memoize(func):
	cache = {}
	
	def wrapper(*args):
		if args in cache:
			return cache[args]
		result = func(*args)
		cache[args] = result
		return result
	
	return wrapper


@memoize
def factorial(number: int) -> int:
	result = 1
	for next_number in range(2, number + 1):
		result *= next_number
	return result


for i in range(0, 10):
	number_in_order = random.randint(0, 100)
	print(f"The factorial of the number {number_in_order} is "
	      f"'{factorial(number_in_order)}'")
