from __future__ import annotations

from django.db import models


class Author(models.Model):
	"""Author of the book."""
	name: models.CharField = models.CharField(max_length=100, db_index=True)
	
	def __str__(self) -> str:
		return self.name


class Book(models.Model):
	"""The book belongs to the author."""
	author: models.ForeignKey = models.ForeignKey(Author,
	                                              on_delete=models.CASCADE,
	                                              related_name="books")
	title: models.CharField = models.CharField(max_length=200, db_index=True)
	published_year: models.IntegerField = models.IntegerField(null=True,
	                                                          blank=True)
	
	class Meta:
		indexes = [
			models.Index(fields=["title"]),
			models.Index(fields=["author"]),
		]
	
	def __str__(self) -> str:
		return f"{self.title} ({self.author})"


class Review(models.Model):
	"""Book review with rating."""
	book: models.ForeignKey = models.ForeignKey(Book, on_delete=models.CASCADE,
	                                            related_name="reviews")
	rating: models.IntegerField = models.IntegerField()  # 1..5
	comment: models.TextField = models.TextField(blank=True)
	
	class Meta:
		indexes = [
			models.Index(fields=["rating"]),
			models.Index(fields=["book"]),
		]
	
	def __str__(self) -> str:
		return f"Review {self.rating} for {self.book}"
