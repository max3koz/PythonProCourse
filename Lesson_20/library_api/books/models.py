from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
	"""
	The Book model represents a book record in a library.
	It contains basic metadata about the book: title, author, genre,
	year of publication, the date the record was created, and the user
	who created it.
	"""
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	genre = models.CharField(max_length=100)
	publication_year = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User,
	                         on_delete=models.CASCADE,
	                         related_name='books',
	                         null=True)
	
	def __str__(self):
		"""Returns a text representation of the book - its title."""
		return self.title
