from typing import Any, Dict, Type


class AutoMethodMeta(type):
	"""
	A metaclass that automatically generates getters and setters for each class
	attribute.
	"""
	
	def __new__(mcs: Type[type], name: str, bases: tuple[type, ...],
	            namespace: Dict[str, Any]) -> type:
		cls = super().__new__(mcs, name, bases, namespace)
		
		for attr_name, attr_value in namespace.items():
			if attr_name.startswith('__') or callable(attr_value):
				continue  # Skip build-im attributes and methods
			
			def make_getter(attr: str) -> Any:
				def getter(self: Any) -> Any:
					return getattr(self, attr)
				
				return getter
			
			def make_setter(attr: str) -> Any:
				def setter(self: Any, value: Any) -> None:
					setattr(self, attr, value)
				
				return setter
			
			setattr(cls, f'get_{attr_name}', make_getter(attr_name))
			setattr(cls, f'set_{attr_name}', make_setter(attr_name))
		
		return cls


class Person(metaclass=AutoMethodMeta):
	name = "John"
	age = 30


p = Person()
print(p.get_name())  # John
p.set_age(31)
print(p.get_age())  # 31
