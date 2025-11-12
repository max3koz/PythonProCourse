from typing import Any

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from .models import Task


class UserSerializer(serializers.ModelSerializer):
	"""
	User serializer for nested view.
	Fields:
		- id: User ID
		- username: Username
	"""
	
	class Meta:
		model = User
		fields = ['id', 'username']


class TaskSerializer(serializers.ModelSerializer):
	"""
	Task serializer for creating and updating.
	Fields:
	- title: Task title
	- description: Task description
	- due_date: Due date
	- user: User ID (PrimaryKey)
	Validation:
	- Due date cannot be in the past.
	"""
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
	
	class Meta:
		model = Task
		fields = ['title', 'description', 'due_date', 'user']
	
	def validate_due_date(self, value: Any) -> Any:
		"""
		Checks that the task deadline is not in the past.
		Args: value (date): Entered deadline date
		Raises:	serializers.ValidationError: If the date is in the past
		Returns: date: Valid date
		"""
		if value < timezone.now().date():
			raise serializers.ValidationError("Due date cannot be in the past.")
		return value


class TaskDisplaySerializer(serializers.ModelSerializer):
	"""
	A task serializer for output, with a nested user.
	Fields:
	- title: Task title
	- description: Task description
	- due_date: Due date
	- user: Nested user object (UserSerializer)
	"""
	user = UserSerializer(read_only=True)
	
	class Meta:
		model = Task
		fields = ['title', 'description', 'due_date', 'user']
