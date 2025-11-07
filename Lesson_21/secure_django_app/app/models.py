from django.db import models


class User(models.Model):
	"""User model with basic fields."""
	username: str = models.CharField(max_length=150, unique=True)
	email: str = models.EmailField(unique=True)
	password: str = models.CharField(max_length=128)
	
	def __str__(self) -> str:
		return self.username
