from typing import Type


class Parent:
	def parent_method(self):
		pass


class Child(Parent):
	def child_method(self):
		pass


def analyze_inheritance(cls: Type) -> None:
	"""
	Analyzes the inheritance of a given class and outputs all methods that
	it inherits from base classes.
	Arguments: cls (Type): The class to be analyzed.
	Output:
    Outputs a list of methods that the class inherits from its immediate
    base classes, excluding special methods (those beginning with ‘__’)
    and the class's own methods.
	"""
	inherited_methods: dict[str, str] = {}
	own_methods: set[str] = set(cls.__dict__.keys())
	
	for base in cls.__bases__:
		base_methods = set(dir(base))
		for method in base_methods:
			if method not in own_methods and not method.startswith("__"):
				inherited_methods[method] = base.__name__
		
		if inherited_methods:
			print(f"Class {cls.__name__} inherited:")
			for method, base_name in inherited_methods.items():
				print(f"- {method} from {base_name}")
			print()
		else:
			print(f"Class {cls.__name__} is not inherited any methods.\n")


analyze_inheritance(Parent)
analyze_inheritance(Child)
