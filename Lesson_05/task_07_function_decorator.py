from typing import Callable, Type


def log_method(cls: Type) -> Type:
	"""
	The class decorator that logs calls to all of its methods.
	:param cls: The class to which the decorator is applied.
	:return: The class with wrapped methods.
	"""
	for attr_name, attr_value in cls.__dict__.items():
		if callable(attr_value):
			def make_wrapper(func: Callable) -> Callable:
				def wrapper(self, *args, **kwargs):
					print(f"Logging: {func.__name__} called with {args}")
					return func(self, *args, **kwargs)
				
				return wrapper
			
			setattr(cls, attr_name, make_wrapper(attr_value))
	return cls


@log_method
class MyClass:
	def add(self, a, b):
		return a + b
	
	def subtract(self, a, b):
		return a - b


obj = MyClass()
obj.add(5, 3)  # Logging: add called with (5, 3)
obj.subtract(5, 3)  # Logging: subtract called with (5, 3)
