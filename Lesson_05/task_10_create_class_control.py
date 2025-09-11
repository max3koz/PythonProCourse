from typing import Any, Type


class SingletonMeta(type):
	"""
	The metaclass implements the Singleton pattern.
	It guarantees that a class using this metaclass will have only one instance.
	"""
	instances: dict[Type[Any], Any] = {}
	
	def __call__(cls: Type[Any], *args: Any, **kwargs: Any) -> Any:
		"""
		 Redefines the class call if the instance already exists — returns it,
		 otherwise creates a new one, saves it, and returns it.
        Arguments:
            cls (Type[Any]): The class being created.
            *args (Any): Positional constructor arguments.
            **kwargs (Any): Named constructor arguments.
        Returns:
            Any: A single instance of the class.
		"""
		if cls not in SingletonMeta.instances:
			SingletonMeta.instances[cls] = super().__call__(*args, **kwargs)
		return SingletonMeta.instances[cls]


class Singleton(metaclass=SingletonMeta):
	def __init__(self):
		print("Creating instance")


obj1 = Singleton()  # Creating instance
obj2 = Singleton()
print(obj1 is obj2)  # True
