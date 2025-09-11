from typing import Any, Type


class LimitedAttributesMeta(type):
	"""
	The metaclass that limits the number of attributes in a class.
	If a class has more than MAX_ATTRIBUTES attributes (not counting special ones),
	a TypeError error will be raised.
	"""
	MAX_ATTRIBUTES: int = 3
	
	def __new__(mcs: Type[type], name: str, bases: tuple[type, ...],
	            namespace: dict[str, Any]) -> type:
		"""
		Creates a new class and checks the number of attributes.
		Arguments:
			mcs (Type[type]): Metaclass.
			name (str): Class name.
			bases (tuple[type, ...]): Base classes.
			namespace (dict[str, Any]): Class attributes.
		Returns:
			type: New class, if the number of attributes is valid, otherwise
			return the TypeError exception.
		"""
		# Ignoring special attributes
		user_attributes = [key for key in namespace if not key.startswith('__')]
		
		if len(user_attributes) > LimitedAttributesMeta.MAX_ATTRIBUTES:
			raise TypeError(f"Class {name} cannot have more than "
			                f"{LimitedAttributesMeta.MAX_ATTRIBUTES} attributes.")
		
		return super().__new__(LimitedAttributesMeta, name, bases, namespace)


class LimitedClass(metaclass=LimitedAttributesMeta):
	attr1 = 1
	attr2 = 2
	attr3 = 3
	attr4 = 4  # Call exception


obj = LimitedClass()
