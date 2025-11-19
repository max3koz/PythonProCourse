from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
	"""Represents a movie genre."""
	name = models.CharField(max_length=100, unique=True)
	
	def __str__(self) -> str:
		return self.name


class Movie(models.Model):
	"""Represents a movie entity."""
	title = models.CharField(max_length=200)
	description = models.TextField()
	release_date = models.DateField()
	rating = models.FloatField(default=0.0)
	genres = models.ManyToManyField(Genre, related_name="movies")
	
	def __str__(self) -> str:
		return self.title


class Review(models.Model):
	"""Represents a user review for a movie."""
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
	                          related_name="reviews")
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	score = models.IntegerField()
	
	def __str__(self) -> str:
		return f"Review for {self.movie.title} by {self.user.username}"
