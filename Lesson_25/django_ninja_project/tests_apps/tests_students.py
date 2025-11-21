import logging

import pytest
import requests
from apps.students.models import Student, Course, Enrollment, ExamResult
from assertpy import assert_that
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


@pytest.fixture
def user() -> User:
	"""Fixture: creates a test user in DB."""
	return User.objects.create_user(username="maksym", password="secret123")


@pytest.fixture
def session(live_server, user):
	"""Fixture: creates an authenticated session via API login."""
	logger.info("Precondition step 1: Logging in user via API...")
	s = requests.Session()
	login_url = f"{live_server.url}/api/accounts/login"
	payload = {"username": "maksym", "password": "secret123"}
	response = s.post(login_url, json=payload)
	assert response.status_code == 200
	token = response.json()["token"]
	
	logger.info("Precondition step 2: Adding token to headers...")
	s.headers.update({"X-CSRFToken": token})
	s.base_url = live_server.url
	return s


@pytest.mark.django_db
class TestStudentsAPIAuth:
	"""
	Integration tests for Student Course Management API with authentication.
	Covers CRUD for students and courses, enrollments, exam results and averages.
	"""
	
	# ------------------ Students ------------------
	def test_create_student(self, session):
		"""Positive: create a new student."""
		logger.info("Step 1: prepare student payload")
		url = f"{session.base_url}/api/students/students/"
		payload = {"name": "Kate", "email": "kate@example.com"}
		
		logger.info("Step 2: send POST request with auth token")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: verify response and DB state")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(
			Student.objects.filter(email="kate@example.com").exists()).is_true()
	
	def test_list_students(self, session):
		"""Positive: list all students."""
		logger.info("Step 1: create sample students in DB")
		Student.objects.create(name="Boris", email="boris@example.com")
		Student.objects.create(name="Kate", email="kate@example.com")
		url = f"{session.base_url}/api/students/students/"
		
		logger.info("Step 2: send GET request")
		response = session.get(url)
		
		logger.info("Step 3: verify response contains created students")
		assert_that(response.status_code).is_equal_to(200)
		emails = [s["email"] for s in response.json()]
		assert_that(emails).contains("boris@example.com", "kate@example.com")
	
	def test_get_student(self, session):
		"""Positive: retrieve single student by ID."""
		logger.info("Step 1: create student in DB")
		student = Student.objects.create(name="Kate", email="kate@example.com")
		url = f"{session.base_url}/api/students/students/{student.id}"
		
		logger.info("Step 2: send GET request")
		response = session.get(url)
		
		logger.info("Step 3: verify response matches DB record")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.json()["email"]).is_equal_to("kate@example.com")
	
	def test_update_student(self, session):
		"""Positive: update existing student."""
		logger.info("Step 1: create student in DB")
		student = Student.objects.create(name="Kate", email="kate@example.com")
		url = f"{session.base_url}/api/students/students/{student.id}"
		payload = {"name": "Kate", "email": "kate1@example.com"}
		
		logger.info("Step 2: send PUT request with new data")
		response = session.put(url, json=payload)
		
		logger.info("Step 3: verify DB record updated")
		assert_that(response.status_code).is_equal_to(200)
		student.refresh_from_db()
		assert_that(student.email).is_equal_to("kate1@example.com")
	
	def test_delete_student(self, session):
		"""Positive: delete student."""
		logger.info("Step 1: create student in DB")
		student = Student.objects.create(name="Boris",
		                                 email="boris@example.com")
		url = f"{session.base_url}/api/students/students/{student.id}"
		
		logger.info("Step 2: send DELETE request")
		response = session.delete(url)
		
		logger.info("Step 3: verify student removed from DB")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(Student.objects.filter(id=student.id).exists()).is_false()
	
	def test_get_nonexistent_student(self, session):
		"""Negative: retrieve non-existent student."""
		logger.info("Step 1: prepare invalid student ID")
		url = f"{session.base_url}/api/students/students/9999"
		
		logger.info("Step 2: send GET request")
		response = session.get(url)
		
		logger.info("Step 3: verify 404 response")
		assert_that(response.status_code).is_equal_to(404)
	
	# ------------------ Courses ------------------
	def test_create_course(self, session):
		"""Positive: create new course."""
		logger.info("Step 1: prepare course payload")
		url = f"{session.base_url}/api/students/courses/"
		payload = {"title": "Math", "description": "Basic Math"}
		
		logger.info("Step 2: send POST request")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: verify course created in DB")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(Course.objects.filter(title="Math").exists()).is_true()
	
	def test_list_courses(self, session):
		"""Positive: list all courses."""
		logger.info("Step 1: create sample courses in DB")
		Course.objects.create(title="Physics", description="Intro Physics")
		Course.objects.create(title="Chemistry", description="Intro Chemistry")
		url = f"{session.base_url}/api/students/courses/"
		
		logger.info("Step 2: send GET request")
		response = session.get(url)
		
		logger.info("Step 3: verify response contains created courses")
		assert_that(response.status_code).is_equal_to(200)
		titles = [c["title"] for c in response.json()]
		assert_that(titles).contains("Physics", "Chemistry")
	
	def test_get_course(self, session):
		"""Positive: retrieve single course by ID."""
		logger.info("Step 1: create course in DB")
		course = Course.objects.create(title="Biology",
		                               description="Intro Biology")
		url = f"{session.base_url}/api/students/courses/{course.id}"
		
		logger.info("Step 2: send GET request")
		response = session.get(url)
		
		logger.info("Step 3: verify response matches DB record")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.json()["title"]).is_equal_to("Biology")
	
	def test_update_course(self, session):
		"""Positive: update existing course."""
		logger.info("Step 1: create course in DB")
		course = Course.objects.create(title="History",
		                               description="Old History")
		url = f"{session.base_url}/api/students/courses/{course.id}"
		payload = {"title": "Modern History", "description": "Updated"}
		
		logger.info("Step 2: send PUT request with new data")
		response = session.put(url, json=payload)
		
		logger.info("Step 3: verify DB record updated")
		assert_that(response.status_code).is_equal_to(200)
		course.refresh_from_db()
		assert_that(course.title).is_equal_to("Modern History")
	
	def test_delete_course(self, session):
		"""Positive: delete course."""
		logger.info("Step 1: create course in DB")
		course = Course.objects.create(title="Geography",
		                               description="Intro Geography")
		url = f"{session.base_url}/api/students/courses/{course.id}"
		
		logger.info("Step 2: send DELETE request")
		response = session.delete(url)
		
		logger.info("Step 3: verify course removed from DB")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(Course.objects.filter(id=course.id).exists()).is_false()
	
	def test_get_nonexistent_course(self, session):
		"""Negative: retrieve non-existent course."""
		logger.info("Step 1: prepare invalid course ID")
		url = f"{session.base_url}/api/students/courses/9999"
		
		logger.info("Step 2: send GET request")
		response = session.get(url)
		
		logger.info("Step 3: verify 404 response")
		assert_that(response.status_code).is_equal_to(404)
	
	# ------------------ Enrollment ------------------
	def test_enroll_student(self, session):
		"""Positive: enroll student in course."""
		logger.info("Step 1: create student and course in DB")
		student = Student.objects.create(name="Kate", email="kate@example.com")
		course = Course.objects.create(title="Programming",
		                               description="Python basics")
		url = f"{session.base_url}/api/students/enrollments/"
		payload = {"student_id": student.id, "course_id": course.id}
		
		logger.info("Step 2: send POST request to enroll student")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: verify enrollment created in DB")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(Enrollment.objects.filter(student=student,
		                                      course=course).exists()).is_true()
	
	def test_enroll_nonexistent_student(self, session):
		"""Negative: try to enroll non-existent student."""
		logger.info("Step 1: create course in DB")
		course = Course.objects.create(title="Networks",
		                               description="Intro Networks")
		url = f"{session.base_url}/api/students/enrollments/"
		payload = {"student_id": 9999, "course_id": course.id}
		
		logger.info("Step 2: send POST request with invalid student ID")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: verify 404 response")
		assert_that(response.status_code).is_equal_to(404)
	
	def test_enroll_nonexistent_course(self, session):
		"""Negative: try to enroll in non-existent course."""
		logger.info("Step 1: create student in DB")
		student = Student.objects.create(name="Leo", email="leo@example.com")
		url = f"{session.base_url}/api/students/enrollments/"
		payload = {"student_id": student.id, "course_id": 9999}
		
		logger.info("Step 2: send POST request with invalid course ID")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: verify 404 response")
		assert_that(response.status_code).is_equal_to(404)
