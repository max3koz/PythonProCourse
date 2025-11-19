from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
	"""Represents a book in the library."""
	title: str = models.CharField(max_length=200)
	author: str = models.CharField(max_length=100)
	genre: str = models.CharField(max_length=50)
	available: bool = models.BooleanField(default=True)
	
	def __str__(self) -> str:
		return f"{self.title} by {self.author}"


class Rental(models.Model):
	"""Represents a rental of a book by a user."""
	book: Book = models.ForeignKey(Book, on_delete=models.CASCADE,
	                               related_name="rentals")
	user: User = models.ForeignKey(User, on_delete=models.CASCADE)
	rented_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
	return_date: models.DateTimeField = models.DateTimeField(null=True,
	                                                         blank=True)
	
	def __str__(self) -> str:
		return f"{self.book.title} rented by {self.user.username}"
