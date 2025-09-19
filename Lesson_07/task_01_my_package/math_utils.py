def factorial(num: int) -> int:
	"""Calculates the factorial of a number 'num'."""
	if num < 0:
		raise ValueError(f"Factorial is defined only for non-negative numbers.")
	if num == 0 or num == 1:
		return 1
	return num * factorial(num - 1)


def gcd(num_1: int, num_2: int) -> int:
	"""
	Calculate the greatest common divisor (GCD) of two numbers on Euclid's
	algorithm based.
	"""
	if not isinstance(num_1, int) or not isinstance(num_2, int):
		raise TypeError("Arguments must be integers.")
	if num_1 < 0 or num_2 < 0:
		raise ValueError("The GCD is defined only for non-negative integers.")
	if num_2 == 0:
		return num_1
	return gcd(num_2, num_1 % num_2)
