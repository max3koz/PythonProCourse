from decimal import Decimal
from typing import Union


class UnknownOperationError(Exception):
	"""
	Exception for handling unsupported arithmetic operations.
	"""
	
	def __init__(self, operation: str) -> None:
		super().__init__(f"Unknown operation: '{operation}'. "
		                 f"Use exist operation: +, -, *, /.")


class SmartNumber:
	"""
	Wrapper class for Decimal that implements arithmetic operations.
	"""
	
	def __init__(self, value: Union[str, float, int, Decimal]) -> None:
		"""
		Initializes a SmartNumber object by converting the input value to Decimal.
		:param value: Numeric value (string, float, int or Decimal)
		:raises ValueError: If the value cannot be converted to Decimal
		"""
		try:
			self.value: Decimal = Decimal(str(value).replace(",", "."))
		except Exception:
			raise ValueError(f"Invalid value: {value}")
	
	"""Dunder methods for operationS"""
	
	def __add__(self, other: "SmartNumber") -> "SmartNumber":
		return SmartNumber(self.value + other.value)
	
	def __sub__(self, other: "SmartNumber") -> "SmartNumber":
		return SmartNumber(self.value - other.value)
	
	def __mul__(self, other: "SmartNumber") -> "SmartNumber":
		return SmartNumber(self.value * other.value)
	
	def __truediv__(self, other: "SmartNumber") -> "SmartNumber":
		if other.value == 0:
			raise ZeroDivisionError("Division by zero is not allowed.")
		return SmartNumber(self.value / other.value)
	
	def __str__(self) -> str:
		"""
		Returns a string representation of the number.
		:return: String with the result
		"""
		return str(self.value.normalize())


def calculate_expression(expr: str) -> SmartNumber:
	"""
	Processes an arithmetic expression in the format: <number> <operator> <number>.
	:param expr: Expression string (e.g., "3.5 + 2")
	:return: Result as SmartNumber
	:raises ValueError: If the expression format is invalid
	:raises UnknownOperationError: If the operation is not supported
	"""
	parts = expr.strip().split()
	if len(parts) != 3:
		raise ValueError("Format must be: <number> <operator> <number>")
	
	a, op, b = parts
	num1 = SmartNumber(a)
	num2 = SmartNumber(b)
	
	if op == '+':
		return num1 + num2
	elif op == '-':
		return num1 - num2
	elif op == '*':
		return num1 * num2
	elif op == '/':
		return num1 / num2
	else:
		raise UnknownOperationError(op)


def run_calculator() -> None:
	"""
	Launches the interactive console calculator.
	"""
	print("Calculator is running. Type number and operation "
	      "in the format: <number> <operator> <number>, or type 'exit' to quit.")
	while True:
		try:
			expr = input("> ")
			if expr.lower() == 'exit':
				break
			result = calculate_expression(expr)
			print(f"Result: {result}")
		except Exception as e:
			print(f"Error: {e}")


run_calculator()
