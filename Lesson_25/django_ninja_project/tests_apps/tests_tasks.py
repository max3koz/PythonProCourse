import logging

import pytest
from apps.tasks.models import Task
from assertpy import assert_that
from django.contrib.auth.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestTasksAPI:
	
	@pytest.fixture
	def user(self, client):
		"""The fixture generates the user"""
		logger.info("Precondition 1: Create a user...")
		user = User.objects.create_user(username="maksym", password="secret123")
		
		logger.info("Precondition 2: Lodin user")
		client.login(username="maksym", password="secret123")
		return user
	
	@pytest.fixture
	def task(self, user):
		"""The fixture generates a test task"""
		logger.info("Precondition:3 Creating a test task...")
		task = Task.objects.create(
			user=user,
			title="Test Task",
			description="Some description",
			status="pending",
			due_date="2025-11-20"
		)
		
		logger.info(f"Precondition 4: The task: {task.title}")
		return task
	
	@pytest.fixture
	def tasks_suite(self, user):
		"""Generates a set of test cases to validate the list."""
		logger.info("Precondition 3: Generate a set of test tasks...")
		tasks = [
			Task.objects.create(
				user=user,
				title="Task A",
				description="First test task",
				status="pending",
				due_date="2025-11-20"
			),
			Task.objects.create(
				user=user,
				title="Task B",
				description="Second test task",
				status="done",
				due_date="2025-11-21"
			),
			Task.objects.create(
				user=user,
				title="Task C",
				description="Third test task",
				status="pending",
				due_date="2025-11-22"
			),
		]
		logger.info(
			f"Precondition 4: Tasks created: {[t.title for t in tasks]}")
		return tasks
	
	def test_create_task(self, client, user):
		logger.info("Step 1: send a POST request to create a task.")
		payload = {
			"title": "New Task",
			"description": "Created via test",
			"status": "done",
			"due_date": "2025-11-21"
		}
		response = client.post("/api/tasks/", payload,
		                       content_type="application/json")
		
		logger.info("Step 2: check the status code.")
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step 3: Check the response body.")
		data = response.json()
		assert_that(data["title"]).is_equal_to("New Task")
		
		logger.info("Step 4: check that the task is saved in the database.")
		assert_that(Task.objects.filter(title="New Task").exists()).is_true()
	
	def test_list_tasks(self, client, user, tasks_suite):
		logger.info("Крок 1: надсилаємо GET-запит для отримання списку задач.")
		response = client.get("/api/tasks/")
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step 2: check the response format.")
		data = response.json()
		assert_that(data).is_type_of(list)
		assert_that(len(data)).is_equal_to(3)
		
		logger.info("Step 3: check that all task names are present.")
		titles = [task["title"] for task in data]
		assert_that(titles).contains("Task A", "Task B", "Task C")
	
	def test_filter_tasks_by_status(self, client, user, tasks_suite):
		logger.info(
			"Step 1: send a GET request with the status=pending filter.")
		response = client.get("/api/tasks/?status=pending")
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step 2: check the number of tasks.")
		data = response.json()
		assert_that(data).is_length(2)
		
		logger.info("Step 3: check the status of tasks.")
		assert_that(data[0]["status"]).is_equal_to("pending")
	
	def test_get_task(self, client, user, task):
		logger.info(f"Step 1: send a GET request for the task id={task.id}.")
		response = client.get(f"/api/tasks/{task.id}")
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step 2: Check the response body.")
		data = response.json()
		assert_that(data["title"]).is_equal_to("Test Task")
	
	def test_update_task(self, client, user, task):
		logger.info(
			f"Step 1: send a PUT request to update the task id={task.id}.")
		payload = {
			"title": "Updated Task",
			"description": "Updated description",
			"status": "done",
			"due_date": "2025-12-01"
		}
		response = client.put(f"/api/tasks/{task.id}", payload,
		                      content_type="application/json")
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step 2: Check the response body.")
		data = response.json()
		assert_that(data["title"]).is_equal_to("Updated Task")
		assert_that(data["description"]).is_equal_to("Updated description")
		assert_that(data["status"]).is_equal_to("done")
		assert_that(data["due_date"]).is_equal_to("2025-12-01")
		
		logger.info("Step 3: check that the changes are saved in the database.")
		task.refresh_from_db()
		assert_that(task.title).is_equal_to("Updated Task")
		assert_that(task.description).is_equal_to("Updated description")
		assert_that(task.status).is_equal_to("done")
		assert_that(str(task.due_date)).is_equal_to("2025-12-01")
	
	def test_delete_task(self, client, user, task):
		logger.info(f"Step 1: send a DELETE request for task id={task.id}.")
		response = client.delete(f"/api/tasks/{task.id}")
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Step 2: Check the response body.")
		data = response.json()
		assert_that(data).contains_key("success")
		assert_that(data["success"]).is_true()
		
		logger.info("Step 3: verify that the task has been deleted "
		            "from the database.")
		exists = Task.objects.filter(id=task.id).exists()
		assert_that(exists).is_false()
