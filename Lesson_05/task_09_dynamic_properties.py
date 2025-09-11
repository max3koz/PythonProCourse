class DynamicProperties:
	"""
	The class that allows properties to be dynamically added during program
	execution.
	Properties are created using the built-in property() function
	and have getters and setters that work through the internal _values
	dictionary.
	"""
	
	def __init__(self):
		"""
		Initializes an object with empty dictionary for storing property values.
		"""
		self.value: dict[str, object] = {}
	
	def add_property(self, name: str, default_value: object = None) -> None:
		"""
		Adds a new property to a class with a getter and setter.
		Arguments:
			name (str): The name of the property.
			default_value (object, optional): The initial value of the property.
			The default is None.
		Return: None. The property is added to the class dynamically.
		"""
		self.value[name] = default_value
		
		def getter(self) -> object:
			return self.value[name]
		
		def setter(self, value: object) -> None:
			self.value[name] = value
		
		setattr(self.__class__, name, property(getter, setter))


obj = DynamicProperties()
obj.add_property('name', 'default_name')

print(obj.name)
obj.name = "Maksym"
print(obj.name)
