import logging
import os
import socket
import subprocess
import time

import pytest
import requests
from assertpy import assert_that
from bs4 import BeautifulSoup
from core.forms import SampleForm
from core.models import CustomModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:8000"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def wait_for_server(host: str, port: int, timeout: int = 30):
	"""
	Waits for a server to start on the specified host and port.
	Connects to the server every 1 second until a response is received or a timeout occurs.
	Args:
		host (str): The IP address or domain of the server.
		port (int): The port on which the server is expected.
		timeout (int): The maximum timeout in seconds.
	Raises: RuntimeError: If the server has not started within the specified time.
	"""
	start = time.time()
	while time.time() - start < timeout:
		try:
			with socket.create_connection((host, port), timeout=2):
				print(f"The server is available at {host}:{port}")
				return
		except OSError:
			print(f"We are waiting for the server to start on {host}:{port}...")
			time.sleep(1)
	raise RuntimeError(
		f"The server did not start on{host}:{port} till {timeout} sec.")


@pytest.fixture(scope="session", autouse=True)
def run_server():
	"""
	Pytest fixture that starts the Django server before tests.
	- Creates a superuser if it doesn't already exist.
	- Starts the server on port 8000.
	- Waits for it to be available.
	- Stops the server after tests are complete.
	"""
	logger.info("Створюємо суперкористувача в реальній базі...")
	subprocess.run([
		"python", "manage.py", "shell", "-c",
		(
			"from django.contrib.auth import get_user_model; "
			"User = get_user_model(); "
			"User.objects.filter(username='admin').exists() or "
			"User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
		)], cwd=PROJECT_ROOT, check=True)
	logger.info("Запускаємо сервер Django на порту 8000...")
	
	proc = subprocess.Popen(
		["python", "manage.py", "runserver", "8000"],
		cwd=PROJECT_ROOT,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,
		text=True
	)
	
	wait_for_server("127.0.0.1", 8000)
	yield
	logger.info("Stop the server...")
	proc.terminate()


class TestUserAuth:
	"""Tests for user registration."""
	
	def test_user_registration(self):
		"""Verify that a new user can register via the form."""
		print("Opening the registration page")
		session = requests.Session()
		
		register_page = session.get("http://127.0.0.1:8000/users/register/")
		soup = BeautifulSoup(register_page.text, "html.parser")
		
		print("Receiving CSRF token")
		csrf_token = soup.find("input",
		                       attrs={"name": "csrfmiddlewaretoken"}).get(
			"value")
		
		print("Sending a POST request for registration")
		response = session.post(
			"http://127.0.0.1:8000/users/register/",
			data={
				"username": "liveuser",
				"phone_number": "+380501235689",
				"password": "securepass123",
				"csrfmiddlewaretoken": csrf_token
			},
			headers={"Referer": "http://127.0.0.1:8000/users/register/"}
		)
		
		print("Checking the response status code")
		assert_that(response.status_code).is_equal_to(200)
	
	def test_duplicate_user_registration(self):
		"""Verify that re-registration with the same username causes an error."""
		logger.info("Імітуємо повторну реєстрацію")
		session = requests.Session()
		register_page = session.get(f"{BASE_URL}/users/register/")
		soup = BeautifulSoup(register_page.text, "html.parser")
		csrf_token = soup.find("input",
		                       attrs={"name": "csrfmiddlewaretoken"}).get(
			"value")
		data = {"username": "liveuser",
		        "phone_number": "+380501235689",
		        "password": "securepass123",
		        "csrfmiddlewaretoken": csrf_token}
		
		logger.info("First registration")
		session.post(f"{BASE_URL}/users/register/", data=data,
		             headers={"Referer": f"{BASE_URL}/users/register/"})
		
		logger.info("Second registration with the same data")
		response = session.post(f"{BASE_URL}/users/register/", data=data,
		                        headers={
			                        "Referer": f"{BASE_URL}/users/register/"})
		
		logger.info("Checking error message")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.text).contains("username already exists")
	
	def test_admin_login(self):
		"""Checks that the superuser can log in to the admin area."""
		logger.info("Opening the login page")
		session = requests.Session()
		login_page = session.get("http://127.0.0.1:8000/admin/login/")
		soup = BeautifulSoup(login_page.text, "html.parser")
		
		logger.info("🔹 Receiving CSRF token")
		csrf_token = soup.find(
			"input", attrs={"name": "csrfmiddlewaretoken"}).get("value")
		
		logger.info("Sending a POST request for login")
		response = session.post(
			"http://127.0.0.1:8000/admin/login/?next=/admin/",
			data={
				"username": "admin",
				"password": "adminpass",
				"csrfmiddlewaretoken": csrf_token
			},
			headers={"Referer": "http://127.0.0.1:8000/admin/login/"}
		)
		
		logger.info("Checking that the user is logged in")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.text).contains("Log out")


class TestCoreView:
	"""Tests for CustomView, accessible via the /core/ route."""
	
	def test_core_home_view(self):
		"""
		Verify that the page /core/ returns a status of 200
		and contains the text 'Hello'.
		"""
		logger.info("Sending GET request to /core/")
		response = requests.get("http://127.0.0.1:8000/core/")
		
		logger.info(f"Response status: {response.status_code}")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.text).contains("Hello")
	
	def test_custom_model_stats(self):
		"""Verify that the /core/ page contains a message from CBV."""
		logger.info("Verify that CBV adds a message to the template")
		response = requests.get("http://127.0.0.1:8000/core/")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.text).contains("Hello from CBV")
	
	def test_custom_view_template_content(self):
		"""Verify that the template contains an HTML structure (e.g. <h1>)."""
		logger.info("Checking for HTML elements in the response")
		response = requests.get(f"{BASE_URL}/core/")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.text).contains("<h1>")


class TestMiddleware:
	"""Tests for custom middleware."""
	
	def test_custom_header(self):
		"""Verify that the middleware adds the X-Custom-Header to the response."""
		logger.info("Sending a request to /core/ to check headers")
		response = requests.get("http://127.0.0.1:8000/core/")
		assert_that(response.status_code).is_equal_to(200)
		
		logger.info("Checking for the presence of the X-Custom-Header")
		assert_that(response.headers).contains_key("X-Custom-Header")
		assert_that(response.headers["X-Custom-Header"]).is_equal_to("MyValue")


class TestRestAPI:
	"""Tests for REST API working with CustomModel."""
	
	def test_create_custom_model_via_api(self):
		"""Checks for creation of CustomModel object via POST request."""
		logger.info("Sending a POST request to create a CustomModel")
		response = requests.post(f"{BASE_URL}/core/api/custommodel/",
		                         json={"name": "Created via API",
		                               "data": {"key": "value"}})
		assert_that(response.status_code).is_equal_to(201)
		json_data = response.json()
		
		logger.info(
			"Verifying that the	object was created with the correct name")
		assert_that(json_data["name"]).is_equal_to("Created via API")
	
	def test_custom_model_api_structure(self) -> None:
		"""
		Verify the response structure of a GET request to the CustomModel API.
		"""
		logger.info("Getting a list of CustomModel objects via the API")
		response = requests.get(f"{BASE_URL}/core/api/custommodel/")
		assert_that(response.status_code).is_equal_to(200)
		json_data = response.json()
		
		logger.info(
			"Checking that the response is a list with the expected fields")
		assert_that(json_data).is_type_of(list)
		for item in json_data:
			assert_that(item).contains("id", "name", "data")


class TestUserAccessControl:
	"""Tests for controlling access to protected pages."""
	
	def test_profile_requires_login(self):
		"""
		Checks that the profile page is not accessible without authorization.
		"""
		logger.info("🔹 Opening /users/profile/ without login")
		response = requests.get(f"{BASE_URL}/users/profile/",
		                        allow_redirects=False)
		assert_that(response.status_code).is_equal_to(302)
		assert_that(response.headers["Location"]).contains("/login")
	
	def test_profile_access_after_login(self):
		"""
		Checks that the profile page is available after login.
		"""
		logger.info("Let's log in as superuser")
		session = requests.Session()
		login_page = session.get(f"{BASE_URL}/admin/login/")
		soup = BeautifulSoup(login_page.text, "html.parser")
		csrf_token = soup.find(
			"input", attrs={"name": "csrfmiddlewaretoken"}).get("value")
		session.post(
			f"{BASE_URL}/admin/login/?next=/admin/",
			data={
				"username": "admin",
				"password": "adminpass",
				"csrfmiddlewaretoken": csrf_token
			},
			headers={"Referer": f"{BASE_URL}/admin/login/"}
		)
		
		logger.info("🔹 Opening the profile page")
		response = session.get(f"{BASE_URL}/users/profile/")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.text).contains("Welcome, admin")


class TestSampleFormValidation:
	"""
	Tests for the SampleForm form, which contains:
	- a number field with a parity validator
	- a choice field with a custom widget
	"""
	
	def test_valid_even_number(self):
		"""Verify that the form accepts an even number."""
		logger.info("Creating a form with an even number: 4")
		form = SampleForm(data={"number": 4, "choice": "1"})
		
		logger.info(f"- is_valid: {form.is_valid()}")
		assert_that(form.is_valid()).is_true()
		
		logger.info(f"- cleaned_data: {form.cleaned_data}")
		assert_that(form.cleaned_data["number"]).is_equal_to(4)
	
	def test_invalid_odd_number(self):
		"""
		Checks that the form does not accept an odd number.
		Expected validation error.
		"""
		logger.info("Creating a form with an odd number: 3")
		form = SampleForm(data={"number": 3, "choice": "2"})
		
		logger.info(f"- is_valid: {form.is_valid()}")
		assert_that(form.is_valid()).is_false()
		
		logger.info(f"- errors: {form.errors}")
		assert_that(form.errors["number"]).contains("The value must be even!")
	
	def test_missing_fields(self):
		"""Verify that the form is not valid without required fields."""
		logger.info("Creating a form without data")
		form = SampleForm(data={})
		
		logger.info(f"🔸 is_valid: {form.is_valid()}")
		assert_that(form.is_valid()).is_false()
		
		logger.info(f"🔸 errors: {form.errors}")
		assert_that(form.errors).contains_key("number")
		assert_that(form.errors).contains_key("choice")
