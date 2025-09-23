class StringProcessor:
	"""
	A class for basic string processing.
	"""
	
	@staticmethod
	def reverse_string(text: str) -> str:
		"""Returns the reversed string."""
		return text[::-1]
	
	@staticmethod
	def capitalize_string(text: str) -> str:
		"""Capitalizes the first letter."""
		return text.capitalize()
	
	@staticmethod
	def count_vowels(text: str) -> int:
		"""Returns the number of vowels in a string."""
		vowels = "aeiouAEIOU"
		return sum(1 for char in text if char in vowels)
