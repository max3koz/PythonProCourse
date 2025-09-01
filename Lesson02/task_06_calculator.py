from typing import Callable


def create_calculator(operator: str) -> Callable[[float, float], float]:
	"""
	The function that create calculator based on the passed operator.
	Returns: Callable[[float, float], float]: A function that takes two numbers
	and performs the appropriate mathematical operation.
	Raises:	ValueError: If the operator is not supported or when dividing by zero.
	"""
	def calculate(a: float, b: float) -> float:
		"""
		The function to perform calculations.
		"""
		if operator == "+":
			return a + b
		elif operator == "-":
			return a - b
		elif operator == "*":
			return a * b
		elif operator == "/":
			if b == 0:
				raise ValueError("Division by zero is impossible!!!")
			return a / b
		else:
			raise ValueError(f"Unexpected operator: {operator}!!!")
	
	return calculate


add = create_calculator("+")
subtract = create_calculator("-")
multiply = create_calculator("*")
divide = create_calculator("/")
failed_operator = create_calculator("{")

print(add(10.0, 5.0))
print(subtract(10.5, 5.0))
print(multiply(10.5, 5.0))
print(divide(10.5, 5.0))
property(failed_operator(10.0, 5.6))
