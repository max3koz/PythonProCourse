from typing import Any


class MyClass:
	def greet(self, name: str) -> str:
		return f"Hello, {name}!"


class Proxy:
	"""
	The proxy class that logs method calls and forwards them to the original object.
	"""
	
	def __init__(self, target: Any) -> None:
		"""
		Initializes the proxy with the passed object.
		:param target: The object to which calls will be redirected.
		"""
		self.target = target
	
	def __getattr__(self, name: str) -> Any:
		"""
		Intercepts access to attributes by logging method calls.
		:param name: Name of the attribute or method.
		:return: Attribute or wrapped method.
		"""
		attr: Any = getattr(self.target, name)
		
		if callable(attr):
			def wrapper(*args: Any) -> Any:
				print(f"Method: {name}")
				print(f"Arguments: {args}.")
				return attr(*args)
			return wrapper
		return attr


obj = MyClass()
proxy = Proxy(obj)

print(proxy.greet("Alice"))