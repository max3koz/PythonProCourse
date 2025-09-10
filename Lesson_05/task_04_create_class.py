from typing import Callable, Dict, Type


def say_hello(self) -> str:
	"""
	Say hello function.
	"""
	return "Hello!"


def say_goodbye(self) -> str:
	"""
	Say Goodbay function.
	"""
	return "Goodbye!"


def create_class(class_name: str, methods: Dict[str, Callable]) -> Type:
	"""
	The funtion creates a new class with a specified name and methods.
	"""
	return type(class_name, (object,), methods)


methods = {
	"say_hello": say_hello,
	"say_goodbye": say_goodbye
}

MyDynamicClass = create_class("MyDynamicClass", methods)

obj = MyDynamicClass()
print(obj.say_hello())  # Hello!
print(obj.say_goodbye())  # Goodbye!
