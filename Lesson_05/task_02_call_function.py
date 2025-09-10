from typing import Any


class Calculator:
	def add(self, a, b):
		return a + b
	
	def subtract(self, a, b):
		return a - b

def call_function(obj: Any, method_name: str, *args: Any) -> Any:
	method = getattr(obj, method_name)
	if callable(method):
		return method(*args)
	else:
		return AttributeError(f"'{type(obj).__name__}' object has no callable "
		                      f"method '{method_name}'")

calc = Calculator()
print(call_function(calc, "add", 10, 5))  # 15
print(call_function(calc, "subtract", 10, 5))  # 5
print(call_function(calc, "div", 10, 5))  # AttributeError: 'Calculator' object has no attribute 'div'

