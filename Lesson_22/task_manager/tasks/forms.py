from django import forms
from django.utils import timezone

from .models import Task


class TaskForm(forms.ModelForm):
	"""
	Form for creating and editing a task.
	Fields:
	- title: Task title (required)
	- description: Task description (optional)
	- due_date: Deadline date (required)
	Validation:
	- Deadline date cannot be in the past.
	"""
	
	class Meta:
		model = Task
		fields = ['title', 'description', 'due_date']
	
	def clean_due_date(self):
		"""
		Checks that the task deadline is not in the past.
		Raises:
		forms.ValidationError: If the deadline is before the current date.
		Returns: datetime.date: The valid deadline date.
		"""
		due_date = self.cleaned_data['due_date']
		if due_date < timezone.now().date():
			raise forms.ValidationError("Due date cannot be in the past.")
		return due_date
