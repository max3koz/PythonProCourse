class Person:
	"""
	The class representing a person with a name and age.
	Supports comparison by age.
	"""
	
	def __init__(self, name: str, age: int):
		"""
		Initializes a Person object.
		Args: name (str): The person's name, age (int): The person's age.
		"""
		self.name = name
		self.age = age
	
	def __lt__(self, other: 'Person') -> bool:
		"""
		Less: Compares the age of the current object with another.
		Args: other (Person): Another person.
		Returns: bool: True if self is younger than others.
		"""
		return self.age < other.age
	
	def __eq__(self, other: 'Person') -> bool:
		"""
		Equality: Compares the ages of two people.
		Args: other (object): Another object.
		Returns: bool: True if the ages are the same.
		"""
		return isinstance(other, Person) and self.age == other.age
	
	def __gt__(self, other: 'Person') -> bool:
		"""
		Greater: Compares the age of the current object with another.
		Args: other (Person): Another person.
		Returns: bool: True if self is older than others.
		"""
		return self.age > other.age
	
	def __repr__(self) -> str:
		"""
		Returns a string representation of an object.
		Returns: str: Format "Person(name, age)"
		"""
		return f"Person({self.name}, {self.age})"


people_list = [Person("Name_1", 11),
               Person("Name_3", 23),
               Person("Name_2", 31),
               Person("Name_3", 25),
               Person("Name_2", 32),
               Person("Name_4", 44)]

print("Sorted people list:")
sorted_people = sorted(people_list)
for person in sorted_people:
	print(person)
print()

print("Sorted people by the name then the age:")
sorted_people_by_name_age = sorted(people_list, key=lambda p: (p.name, p.age))
for person in sorted_people_by_name_age:
	print(person)
