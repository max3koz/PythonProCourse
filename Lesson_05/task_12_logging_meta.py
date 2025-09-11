from typing import Any, Dict, Type, Tuple


class LoggingMeta(type):
	"""
	The metaclass that adds logging when accessing class instance attributes.
    Read (get) and write (set) operations are logged.
	"""
	def __new__(mcs: Type[type], name: str, bases: Tuple[type, ...],
	            namespace: Dict[str, Any]) -> type:
		"""
		Creates a new class and wraps its attribute access methods with logging.
        Arguments:
            mcs (Type[type]): Metaclass.
            name (str): Class name.
            bases (tuple[type, ...]): Base classes.
            namespace (dict[str, Any]): Class attributes.
        Returns: type: New class with logging of access to attributes.
		"""
		cls: type = super().__new__(mcs, name, bases, namespace)
		
		original_getattr = cls.__getattribute__
		original_setattr = cls.__setattr__
		
		def logged_getattr(self: Any, attr: str) -> Any:
			print(f"Logging: accessed '{attr}'.")
			return original_getattr(self, attr)
			
		def logged_setattr(self: Any, attr: str, value: Any) -> None:
			print(f"Logging: modified '{attr}'.")
			original_setattr(self, attr, value)
			
		cls.__getattribute__ = logged_getattr
		cls.__setattr__ = logged_setattr
		
		return cls


class MyClass(metaclass=LoggingMeta):
	def __init__(self, name):
		self.name = name


obj = MyClass("Python") # Logging: modified 'name': as result of the initialization of object creating
print(obj.name)  # Logging: accessed 'name'
obj.name = "New Python"  # Logging: modified 'name'
