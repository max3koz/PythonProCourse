from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .forms import TaskForm
from .models import Task
from .serializers import TaskSerializer, TaskDisplaySerializer


class TaskFormTestCase(TestCase):
	"""Test suite covered TaskForm functionality"""
	
	def test_valid_task_form(self) -> None:
		"""Verify that the form is valid with correct data"""
		form = TaskForm(data={
			'title': 'Test Task',
			'description': 'Details',
			'due_date': timezone.now().date() + timedelta(days=1)
		})
		self.assertTrue(form.is_valid())
	
	def test_task_form_invalid_with_empty_required_fields(self) -> None:
		"""Verify that form is invalid without required fields"""
		form = TaskForm(data={})
		self.assertFalse(form.is_valid())
		self.assertIn('title', form.errors)
		self.assertIn('due_date', form.errors)
	
	def test_task_form_due_date_in_past(self) -> None:
		"""Verify that form is invalid with a past date"""
		form = TaskForm(data={
			'title': 'Test Task',
			'description': 'Details',
			'due_date': timezone.now().date() - timedelta(days=1)
		})
		self.assertFalse(form.is_valid())
		self.assertIn('due_date', form.errors)


class TaskSerializerTestCase(TestCase):
	"""Test suite covered TaskSerializer functionality """
	
	def setUp(self) -> None:
		self.user: User = User.objects.create_user(username='maksym',
		                                           password='12345')
	
	def test_valid_task_serializer(self) -> None:
		"""Verify that serializer is valid with correct data"""
		data = {
			'title': 'Test Task',
			'description': 'Details',
			'due_date': str(timezone.now().date() + timedelta(days=1)),
			'user': self.user.id
		}
		serializer = TaskSerializer(data=data)
		self.assertTrue(serializer.is_valid())
	
	def test_task_serializer_missing_title(self) -> None:
		"""Verify that serializer is invalid without header"""
		data = {
			'description': 'Details',
			'due_date': str(timezone.now().date() + timedelta(days=1)),
			'user': self.user.id
		}
		serializer = TaskSerializer(data=data)
		self.assertFalse(serializer.is_valid())
		self.assertIn('title', serializer.errors)
	
	def test_task_serializer_due_date_in_past(self) -> None:
		"""Verify that serializer is invalid with a past date"""
		data = {
			'title': 'Test Task',
			'description': 'Details',
			'due_date': str(timezone.now().date() - timedelta(days=1)),
			'user': self.user.id
		}
		serializer = TaskSerializer(data=data)
		self.assertFalse(serializer.is_valid())
		self.assertIn('due_date', serializer.errors)
	
	def test_task_serializer_ignores_extra_fields(self) -> None:
		"""Verify that serializer ignores extra fields"""
		data = {
			'title': 'Extra Field Task',
			'description': 'Testing extra field',
			'due_date': str(timezone.now().date() + timedelta(days=2)),
			'user': self.user.id,
			'unexpected_field': 'I should be ignored'
		}
		serializer = TaskSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		self.assertNotIn('unexpected_field', serializer.validated_data)


class TaskNestedSerializerTestCase(TestCase):
	"""est suite covered TaskDisplaySerializer functionality """
	
	def setUp(self) -> None:
		self.user: User = User.objects.create_user(username='maksym',
		                                           password='12345')
	
	def test_task_serializer_invalid_user(self) -> None:
		"""Verify that invalid serializer with non-existent user"""
		data = {
			'title': 'Invalid User Task',
			'description': 'Details',
			'due_date': str(timezone.now().date() + timedelta(days=1)),
			'user': 9999
		}
		serializer = TaskSerializer(data=data)
		self.assertFalse(serializer.is_valid())
		self.assertIn('user', serializer.errors)
	
	def test_task_serializer_representation_includes_user(self) -> None:
		"""Verify that serializer correctly outputs the nested user"""
		task = Task.objects.create(
			title='Serialized Task',
			description='Details',
			due_date=timezone.now().date() + timedelta(days=1),
			user=self.user
		)
		serializer = TaskDisplaySerializer(instance=task)
		self.assertEqual(serializer.data['user']['id'], self.user.id)
		self.assertEqual(serializer.data['user']['username'],
		                 self.user.username)
	
	def test_task_display_serializer_output_structure(self) -> None:
		"""Verify that serializer returns the complete data structure"""
		task = Task.objects.create(
			title='Full Output Task',
			description='Details',
			due_date=timezone.now().date() + timedelta(days=3),
			user=self.user
		)
		serializer = TaskDisplaySerializer(instance=task)
		self.assertIn('title', serializer.data)
		self.assertIn('description', serializer.data)
		self.assertIn('due_date', serializer.data)
		self.assertIn('user', serializer.data)
		self.assertIn('id', serializer.data['user'])
		self.assertIn('username', serializer.data['user'])
