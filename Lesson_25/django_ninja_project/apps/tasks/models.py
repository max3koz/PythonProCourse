import datetime

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
	"""
	Task model.
	Fields:
	- user (ForeignKey): User who owns the task.
	- title (CharField): Task title (maximum 200 characters).
	- description (TextField): Task description (can be empty).
	- status (CharField): Task status ("pending" or "done").
	- due_date (DateField): Deadline date. Default is today.
	- created_at (DateTimeField): Date and time the task was created.
	"""
	STATUS_CHOICES = [
		("pending", "Pending"),
		("done", "Done"),
	]
	
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES,
	                          default="pending")
	due_date = models.DateField(default=datetime.date.today)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	
	def __str__(self):
		return self.title
