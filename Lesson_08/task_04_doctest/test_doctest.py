def is_even(n: int) -> bool:
	"""
	Checks whether a number is even.
	>>> is_even(2)
	True
	>>> is_even(3)
	False
	>>> is_even(0)
	True
	>>> is_even(-4)
	True
	>>> is_even(-5)
	False
	"""
	return n % 2 == 0


def factorial(number: int) -> int:
	"""
	Calculates the factorial of a number n.
	>>> factorial(0)
	1
	>>> factorial(1)
	1
	>>> factorial(5)
	120
	>>> factorial(3)
	6
	>>> factorial(10)
	3628800
	"""
	if number < 0:
		raise ValueError("Factorial is defined only for non-negative integers.")
	result = 1
	for i in range(2, number + 1):
		result *= i
	return result
