import importlib
import inspect


def analyze_module(module_name: str) -> None:
	"""
	The function that takes the module name (string) as input and outputs
	a list of all classes, functions, and their signatures in the module
	using the inspect module.
	"""
	module = importlib.import_module(module_name)
	
	print(f"Functions of '{module.__name__}':")
	
	for name in dir(module):
		object = getattr(module, name)
		if inspect.isfunction(object) or inspect.isbuiltin(object):
			try:
				sig = inspect.signature(object)
				print(f"- {name} {sig}")
			except (ValueError, TypeError) as ex:
				print(f"- {name} - without signature")
	
	print(f"Classes of '{module.__name__}'")
	found_class = False
	for name in dir(module):
		object = getattr(module, name)
		if inspect.isclass(object):
			print(f"- {name}")
			found_class = True
	if not found_class:
		print("- no classes in module")


analyze_module("inspect")
analyze_module("math")
