from django import forms
from django.core.exceptions import ValidationError


def validate_even(value: int) -> None:
	"""
	A validator that checks if a value is even.
	Args: value (int): The value to validate.
	Raises: ValidationError: If the value is not even.
	"""
	if value % 2 != 0:
		raise ValidationError("The value must be even!")


class CustomSelect(forms.Select):
	"""
	Custom widget for select field. Uses template 'widgets/custom select.html'.
	"""
	template_name = 'widgets/custom_select.html'


class SampleForm(forms.Form):
	"""
	A form with two fields:
	- number: an integer that must be even
	- choice: a choice from a list, with a custom widget
	The validate_even validator is used to check for evenness.
	"""
	number: int = forms.IntegerField(validators=[validate_even])
	choice: str = forms.ChoiceField(choices=[('1', 'One'), ('2', 'Two')],
	                                widget=CustomSelect)
