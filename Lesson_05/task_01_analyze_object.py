from typing import Any


class MyClass:
	"""
	Investigated class
	"""
	def __init__(self, value):
		self.value = value

	def say_hello(self):
		return f"Hello, {self.value}"
	
def print_output(obj_list: list) -> None:
	"""
	The function pint output
	"""
	for obj_item in obj_list:
		print(obj_item)

def analyze_object(obj: Any) -> None:
	"""
	The function analyze object
	"""
	obj_method: list[str] = []
	obj_dunder_method: list[str] = []
	obj_attr: list[str] = []
	obj_dunder_attr: list[str] = []
	for attr_name in dir(obj):
		attr_value: Any = getattr(obj, attr_name)
		if attr_name.startswith("__") and attr_name.endswith("__"):
			if callable(attr_value):
				obj_dunder_method.append(f"- {attr_name}: {type(attr_value)}")
			elif not callable(attr_value):
				obj_dunder_attr.append(f"- {attr_name}: {type(attr_value)}")
		elif not attr_name.startswith("__") and not attr_name.endswith("__"):
			if callable(attr_value):
				obj_method.append(f"- {attr_name}: {type(attr_value)}")
			elif not callable(attr_value):
				obj_attr.append(f"- {attr_name}: {type(attr_value)}")
		else:
			continue
	print(f"Object type: {type(obj)}")
	print("Attributes:")
	print_output(obj_attr)
	print("Methods:")
	print_output(obj_method)
	print("Magic attributes:")
	print_output(obj_dunder_attr)
	print("Dunder methods:")
	print_output(obj_dunder_method)


obj = MyClass("World")
analyze_object(obj)


