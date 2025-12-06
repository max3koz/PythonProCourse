from typing import Any

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistrationForm(forms.ModelForm):
	"""
	Form for registering a new user.
	Includes fields: username, email, password, password_confirm.
	"""
	password = forms.CharField(widget=forms.PasswordInput)
	password_confirm = forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ["username", "email", "password"]
	
	def clean(self):
		"""
		Performs general validation of the registration form.
			- Gets the cleared data from all fields.
			- Checks if the values ​​of the `password` and `password_confirm`
		fields match.
			- If the passwords are different → raises ValidationError.
			- If everything is OK → returns the dictionary of cleared data.
		Returns: dict[str, Any]: dictionary of cleared form data.
		Raises: ValidationError: if the passwords do not match.
		"""
		cleaned_data: dict[str, Any] = super().clean()
		password: str | None = cleaned_data.get("password")
		password_confirm: str | None = cleaned_data.get("password_confirm")
		
		if password and password_confirm and password != password_confirm:
			raise ValidationError("Паролі не співпадають!")
		
		return cleaned_data
