from __future__ import annotations

from django import forms


class LoginForm(forms.Form):
	"""Form for entering name and age."""
	name: forms.CharField = forms.CharField(max_length=50, label="Ім'я")
	age: forms.IntegerField = forms.IntegerField(min_value=1, max_value=120,
	                                             label="Вік")
	
	def clean_age(self) -> int:
		"""Additional age validation."""
		age: int = self.cleaned_data["age"]
		return age
