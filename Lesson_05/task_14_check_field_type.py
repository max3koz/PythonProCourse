from typing import Any, Dict, Type


class TypeCheckedMeta(type):
	"""
	The metaclass that checks attribute types when they are set.
	If the value does not match the type annotation, a TypeError is raised.
	"""
	
	def __new__(mcs: Type[type], name: str, bases: tuple[type, ...],
	            namespace: Dict[str, Any]) -> type:
		cls = super().__new__(mcs, name, bases, namespace)
		annotations: Dict[str, type] = namespace.get('__annotations__', {})
		
		def checked_setattr(self: Any, attr: str, value: Any) -> None:
			expected_type = annotations.get(attr)
			if expected_type and not isinstance(value, expected_type):
				raise TypeError(f"The attribute ‘{attr}’ is expected to be "
				                f"of type ‘{expected_type.__name__}’, "
				                f"but ‘{type(value).__name__}’ was received.")
			object.__setattr__(self, attr, value)
		
		cls.__setattr__ = checked_setattr
		return cls


class Person(metaclass=TypeCheckedMeta):
	name: str = ""
	age: int = 0


p = Person()
p.name = "John"  # Все добре
p.age = 20  # Все добре
p.age = "30"  # Викличе помилку, очікується int
