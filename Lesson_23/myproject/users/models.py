from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
	"""
	Extended user model based on AbstractUser.
	Adds the field: phone_number: phone number in +380... format, maximum 15 characters.
	"""
	phone_number: str = models.CharField(max_length=15)
