from typing import Optional

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
	"""
	Extended user profile class.
	Stores additional information about the user: biography, date of birth,
	place of residence, avatar (profile image).
	Connected to the base User model via OneToOneField.
	"""
	user: User = models.OneToOneField(User, on_delete=models.CASCADE)
	bio: Optional[str] = models.TextField(max_length=500,
	                                      blank=True,
	                                      help_text="Коротка біографія "
	                                                "(максимум 500 символів)")
	birth_date: Optional[str] = models.DateField(null=True, blank=True)
	location: Optional[str] = models.CharField(max_length=100, blank=True)
	avatar: Optional[models.ImageField] = models.ImageField(
		upload_to='avatars/', blank=True, null=True)
	
	def __str__(self) -> str:
		"""The function returns a string representation of the user's profile."""
		return f"{self.user.username}'s profile"
