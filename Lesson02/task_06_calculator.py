from typing import Callable


def create_calculator(operator: str) -> Callable[[float, float], float]:
	def calculate(a: float, b: float) -> float:
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
