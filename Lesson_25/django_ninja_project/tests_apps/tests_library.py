import logging

import pytest
import requests
from apps.library.models import Book, Rental
from assertpy import assert_that
from django.contrib.auth.models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestLibraryAPI:
	"""
	Integration tests for Book Library API.
	Covers CRUD for books, search, rentals and returns.
	"""
	
	@pytest.fixture
	def user(self) -> User:
		"""Fixture: creates a test user in DB."""
		return User.objects.create_user(username="maksym", password="secret123")
	
	@pytest.fixture
	def session(self, live_server, user):
		"""Fixture: creates an authenticated session via API login."""
		logger.info("Precondition step 1: Logging in user via API...")
		s = requests.Session()
		login_url = f"{live_server.url}/api/accounts/login"
		payload = {"username": "maksym", "password": "secret123"}
		response = s.post(login_url, json=payload)
		assert response.status_code == 200
		token = response.json()["token"]
		logger.info("Step 2: Adding token to headers...")
		s.headers.update({"X-CSRFToken": token})
		return s
	
	# ------------------ Books ------------------
	def test_create_book(self, live_server, session):
		"""Verify that possible to create a new book."""
		logger.info("Step 1: create test book data")
		url = f"{live_server.url}/api/library/books/"
		payload = {"title": "Book1", "author": "Author1", "genre": "Fiction"}
		
		logger.info("Step 2: Sending POST request to create book")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: Checking response contains book.")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(Book.objects.filter(title="Book1").exists()).is_true()
	
	def test_create_book_unauthorized(self, live_server):
		"""Verify that impossible to create book without authentication."""
		logger.info("Step 1: create test book data")
		url = f"{live_server.url}/api/library/books/"
		payload = {"title": "NoAuth", "author": "Anon", "genre": "Drama"}
		
		logger.info("Step 2: sending POST request")
		response = requests.post(url, json=payload)
		
		logger.info("Step 3: Verify that the status code 404")
		assert_that(response.status_code).is_equal_to(404)
	
	def test_list_books(self, live_server, session):
		"""Verify that possible to get list all books with filters."""
		logger.info("Step 1: create test book data list")
		Book.objects.create(title="Python 101", author="Guido",
		                    genre="Programming")
		Book.objects.create(title="Django Guide", author="Adrian",
		                    genre="Programming")
		url = f"{live_server.url}/api/library/books/?author=Guido"
		
		logger.info("Step 2: sending GET request to list books by author")
		response = session.get(url)
		
		logger.info("Step 3: Checking response contains book list.")
		assert_that(response.status_code).is_equal_to(200)
		titles = [b["title"] for b in response.json()]
		assert_that(titles).contains("Python 101")
	
	def test_get_book(self, live_server, session):
		"""Verify that possible to get a single book by ID."""
		logger.info("Step 1: create test book data")
		book = Book.objects.create(title="Unique", author="Someone",
		                           genre="Drama")
		url = f"{live_server.url}/api/library/books/{book.id}"
		
		logger.info("Step 2: sending GET request to books by ID")
		response = session.get(url)
		
		logger.info("Step 3: Checking response contains book.")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.json()["title"]).is_equal_to("Unique")
	
	def test_get_nonexistent_book(self, live_server, session):
		"""Verify that impossible to retrieve non-existent book."""
		logger.info("Step 1: create test book data")
		url = f"{live_server.url}/api/library/books/9999"
		
		logger.info("Step 2: sending GET request")
		response = session.get(url)
		
		logger.info("Step 3: Verify that the status code 404")
		assert_that(response.status_code).is_equal_to(404)
	
	def test_update_book(self, live_server, session):
		"""Verify that possible to update an existing book."""
		logger.info("Step 1: create test book data")
		book = Book.objects.create(title="Old", author="Anon", genre="Sci-Fi")
		url = f"{live_server.url}/api/library/books/{book.id}"
		payload = {"title": "New", "author": "Anon", "genre": "Sci-Fi"}
		
		logger.info("Step 2: sending PUT request")
		response = session.put(url, json=payload)
		
		logger.info("Step 3: Checking response contains updated book data.")
		assert_that(response.status_code).is_equal_to(200)
		book.refresh_from_db()
		assert_that(book.title).is_equal_to("New")
	
	def test_delete_book(self, live_server, session):
		"""Verify that possible to delete a book."""
		logger.info("Step 1: create test book data")
		book = Book.objects.create(title="ToDelete", author="Anon",
		                           genre="Drama")
		url = f"{live_server.url}/api/library/books/{book.id}"
		
		logger.info("Step 2: sending DELETE request")
		response = session.delete(url)
		
		logger.info(
			"Step 3: Checking response doesn't contain deleted book data.")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(Book.objects.filter(id=book.id).exists()).is_false()
	
	# ------------------ Rentals ------------------
	def test_rent_book(self, live_server, session, user):
		"""Verify that possible to rent a book."""
		logger.info("Step 1: create test book data")
		book = Book.objects.create(title="Rentable", author="Anon",
		                           genre="Drama", available=True)
		url = f"{live_server.url}/api/library/rentals/"
		payload = {"book_id": book.id, "return_date": "2030-01-01T00:00:00"}
		
		logger.info("Step 2: sending POST request")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: Checking response contains rented book.")
		assert_that(response.status_code).is_equal_to(201)
		book.refresh_from_db()
		assert_that(book.available).is_false()
		assert_that(
			Rental.objects.filter(book=book, user=user).exists()).is_true()
	
	def test_rent_book_unauthorized(self, live_server, user):
		"""Verify that impossible to rent a book without authentication."""
		logger.info("Step 1: create test book data")
		book = Book.objects.create(title="NoAuthRent", author="Anon",
		                           genre="Drama", available=True)
		url = f"{live_server.url}/api/library/rentals/"
		payload = {"book_id": book.id, "return_date": "2030-01-01T00:00:00"}
		
		logger.info("Step 2: sending GET request")
		response = requests.post(url, json=payload)
		
		logger.info("Step 3: Verify that the status code 404")
		assert_that(response.status_code).is_equal_to(404)
	
	def test_rent_unavailable_book(self, live_server, session, user):
		"""Verify that impossible  to rent a book that is not available."""
		logger.info("Step 1: create test book data")
		book = Book.objects.create(title="Unavailable", author="Anon",
		                           genre="Drama", available=False)
		url = f"{live_server.url}/api/library/rentals/"
		payload = {"book_id": book.id, "return_date": "2030-01-01T00:00:00"}
		
		logger.info("Step 2: sending GET request")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: Verify that the status code 400")
		assert_that(response.status_code).is_equal_to(400)
	
	def test_return_book(self, live_server, session, user):
		"""Verify that possible to return a rented book."""
		logger.info("Step 1: create test book data")
		book = Book.objects.create(title="Returnable", author="Anon",
		                           genre="Drama", available=False)
		rental = Rental.objects.create(book=book, user=user,
		                               return_date="2030-01-01T00:00:00")
		url = f"{live_server.url}/api/library/rentals/{rental.id}/return"
		
		logger.info("Step 2: sending POST request")
		response = session.post(url)
		
		logger.info("Step 3: Checking response contains return book.")
		assert_that(response.status_code).is_equal_to(200)
		book.refresh_from_db()
		assert_that(book.available).is_true()
		assert_that(Rental.objects.filter(id=rental.id).exists()).is_false()
	
	def test_return_book_unauthorized(self, live_server, user):
		"""Verify that impossible to return a book without authentication."""
		logger.info("Step 1: create test book data")
		book = Book.objects.create(title="NoAuthReturn", author="Anon",
		                           genre="Drama", available=False)
		rental = Rental.objects.create(book=book, user=user,
		                               return_date="2030-01-01T00:00:00")
		url = f"{live_server.url}/api/library/rentals/{rental.id}/return"
		
		logger.info("Step 2: sending GET request")
		response = requests.post(url)
		
		logger.info("Step 3: Verify that the status code 404")
		assert_that(response.status_code).is_equal_to(404)
