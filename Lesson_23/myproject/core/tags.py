from django import template

register = template.Library()


@register.filter
def hex_color(value: str) -> str:
	"""
	A template filter that converts a string to a HEX color.
	If the string is 6 characters long, it prefixes it with '#'.
	Otherwise, it returns an error message.
	Args: value (str): A string that should contain a HEX value.
	Returns: str: A HEX color or error message.
	"""
	return f"#{value}" if len(value) == 6 else "Невірний HEX"


@register.simple_tag
def greet(name: str) -> str:
	"""
	Template tag that returns a greeting for the given name.
	Args: name (str): Username.
	Returns: str: Greeting string.
	"""
	return f"Hello, {name}!"
