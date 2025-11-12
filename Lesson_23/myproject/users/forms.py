from django import forms

from .models import CustomUser


class RegistrationForm(forms.ModelForm):
	"""
	User registration form.
	Fields:
	- username: unique username
	- phone_number: phone number, must start with '+'
	- password: password
	"""
	class Meta:
		model = CustomUser
		fields = ['username', 'phone_number', 'password']
	
	def clean_phone_number(self) -> str:
		"""
		Checks that the phone number starts with '+'.
		Returns: str: Validated phone number.
		Raises: forms.ValidationError: If the number does not start with '+'.
		"""
		phone = self.cleaned_data['phone_number']
		if not phone.startswith('+'):
			raise forms.ValidationError("The number must start with '+'")
		return phone
