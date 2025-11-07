import bleach
from django import forms
from django.contrib.auth.hashers import make_password, check_password

from .models import User


class RegistrationForm(forms.ModelForm):
	"""User registration form."""
	password_confirm = forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		widgets = {'password': forms.PasswordInput}
	
	def clean(self) -> dict:
		"""
		The function performs overall form validation after all fields have
		been processed individually.
		Allows you to check relationships between fields
		"""
		cleaned_data = super().clean()
		if cleaned_data['password'] != cleaned_data['password_confirm']:
			raise forms.ValidationError("Паролі не співпадають")
		cleaned_data['password'] = make_password(cleaned_data['password'])
		return cleaned_data


class LoginForm(forms.Form):
	"""User authorization form."""
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	
	def clean(self) -> dict:
		"""
		The function performs general validation of the login form:
		checks whether a user with that name exists and whether
		the password is correct.
		"""
		cleaned_data = super().clean()
		try:
			user = User.objects.get(username=cleaned_data['username'])
			if not check_password(cleaned_data['password'], user.password):
				raise forms.ValidationError("Невірний пароль")
		except User.DoesNotExist:
			raise forms.ValidationError("Користувача не знайдено")
		return cleaned_data


class CommentForm(forms.Form):
	"""
	A form for user input of a comment. Contains one text field and sanitizes
	the entered HTML content to protect against XSS attacks.
	"""
	comment = forms.CharField(widget=forms.Textarea)
	
	def clean_comment(self):
		"""
		The function validates and cleans the comment field — removes
		potentially dangerous HTML code (e.g. <script>, <iframe>, styles)
		to prevent XSS attacks.
		"""
		comment = self.cleaned_data['comment']
		return bleach.clean(comment)
