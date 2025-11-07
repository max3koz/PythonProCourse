from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Task(models.Model):
	"""
	A task model that contains a title, description, deadline, and user binding.
	Fields:
	- title (str): Task title, required, up to 255 characters.
	- description (str): Task description, optional.
	- due_date (date): Task due date, required.
	- user (User): User to whom the task belongs.
	Validation:
	- The deadline date cannot be in the past.
	"""
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	due_date = models.DateField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def clean(self):
		"""
		Checks that the task deadline is not in the past.
		Raises:	ValidationError: If the deadline is before the current date.
		"""
		if self.due_date and self.due_date < timezone.now().date():
			raise ValidationError("Due date cannot be in the past.")
	
	def __str__(self):
		"""
		Returns a text representation of the problem.
		Returns: str: The name of the problem.
		"""
		return self.title
