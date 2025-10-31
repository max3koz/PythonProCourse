from typing import Any

from django import forms
from django.contrib.auth.forms import \
	PasswordChangeForm as DjangoPasswordChangeForm
from django.contrib.auth.models import User
from django.forms.widgets import DateInput

from .models import UserProfile


class RegistrationForm(forms.ModelForm):
	"""
	New user registration form class.
	Adds fields for entering a password and confirming a password.
	Checks the uniqueness of the username and email.
	"""
	password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
	confirm_password = forms.CharField(widget=forms.PasswordInput,
	                                   label='Підтвердження паролю')
	
	class Meta:
		model = User
		fields = ['username', 'email', 'password']
		labels = {
			'username': 'І\'мя та призвище',
			'email': 'Електронна пошта',
			'password': 'Пароль',
		}
	
	def clean(self) -> dict[str, Any]:
		"""
		The method checks: if the passwords match, if the username is already
		taken, if the email is already in use
		"""
		cleaned_data = super().clean()
		if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
			self.add_error('confirm_password', 'Паролі не співпадають')
		if User.objects.filter(username=cleaned_data.get('username')).exists():
			self.add_error('username', 'Ім’я користувача вже зайняте')
		if User.objects.filter(email=cleaned_data.get('email')).exists():
			self.add_error('email', 'Email вже використовується')
		return cleaned_data


class UserProfileForm(forms.ModelForm):
	"""
	User profile editing form class.
	Contains fields: biography, date of birth, place of residence, avatar.
	Checks avatar size.
	"""
	
	class Meta:
		model = UserProfile
		fields = ['bio', 'birth_date', 'location', 'avatar']
		labels = {
			'bio': 'Біографія',
			'birth_date': 'Дата народження',
			'location': 'Місце проживання',
			'avatar': 'Аватар',
		}
		widgets = {
			'birth_date': DateInput(
				attrs={'type': 'date',
				       'class': 'form-control',
				       'style': 'width: 200px;'}),
		}
	
	def clean_avatar(self) -> Any:
		"""The method checks if the avatar is larger than 2MB."""
		avatar = self.cleaned_data.get('avatar')
		if avatar and avatar.size > 2 * 1024 * 1024:
			raise forms.ValidationError("Максимальний розмір зображення — 2MB")
		return avatar


class CustomPasswordChangeForm(DjangoPasswordChangeForm):
	"""
	Custom password change form class.
	Adds a check for: whether the new passwords match, whether the new password
	is different from the current one
	"""
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['old_password'].label = "Поточний пароль"
		self.fields['new_password1'].label = "Новий пароль"
		self.fields['new_password2'].label = "Підтвердження нового пароля"
	
	def clean_new_password2(self):
		"""
		The method checks: whether the new passwords match,
		whether the new password is not the same as the old one
		"""
		new_password1 = self.cleaned_data.get('new_password1')
		new_password2 = self.cleaned_data.get('new_password2')
		old_password = self.cleaned_data.get('old_password')
		
		if new_password1 and new_password2 and new_password1 != new_password2:
			raise forms.ValidationError("Нові паролі не співпадають.")
		
		if new_password1 == old_password:
			raise forms.ValidationError(
				"Новий пароль має відрізнятись від поточного.")
		
		return new_password2
