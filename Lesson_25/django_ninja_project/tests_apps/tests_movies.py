import logging
from datetime import date

import pytest
import requests
from apps.movies.models import Genre, Movie, Review
from assertpy import assert_that
from django.contrib.auth.models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestMoviesAPIWithAuth:
	"""
	Integration tests for Movie Collection API.
	Covers CRUD for genres, movies, and reviews.
	"""
	
	@pytest.fixture
	def user(self):
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
		logger.info(f"Precondition step 2: Received token: {token}")
		s.headers.update({"X-CSRFToken": token})
		return s
	
	# ------------------ Genres ------------------
	def test_create_genre(self, live_server, session):
		"""Verify that possible to create a new genre via POST request."""
		logger.info("Step 1: create test data with new genre")
		url = f"{live_server.url}/api/movies/genres/"
		payload = {"name": "Action"}
		
		logger.info("Step 2: sending POST request to create genre...")
		response = session.post(url, json=payload)
		assert_that(response.status_code).is_equal_to(201)
		data = response.json()
		
		logger.info("Step 3: verify that genre was created")
		assert_that(data["name"]).is_equal_to("Action")
		assert_that(Genre.objects.filter(name="Action").exists()).is_true()
	
	def test_list_genres(self, live_server, session):
		"""Verify that possible to get the list all genres via GET request."""
		logger.info("Step 1: create list of genfe")
		Genre.objects.create(name="Drama")
		Genre.objects.create(name="Comedy")
		url = f"{live_server.url}/api/movies/genres/"
		
		logger.info("Step 2: Sending GET request to list genres...")
		response = session.get(url)
		
		logger.info("Step 3: Verify the genre list")
		assert_that(response.status_code).is_equal_to(200)
		names = [g["name"] for g in response.json()]
		assert_that(names).contains("Drama", "Comedy")
	
	# ------------------ Movies ------------------
	def test_create_movie(self, live_server, session):
		"""Verify that possible to create a new movie via POST request"""
		logger.info("Step 1 : create the test data with the movie")
		genre = Genre.objects.create(name="Genre 1")
		url = f"{live_server.url}/api/movies/"
		payload = {"title": "Title 1",
		           "description": "description",
		           "release_date": str(date(2014, 11, 7)),
		           "rating": 9.0,
		           "genre_ids": [genre.id],}
		
		logger.info("Step 2: Sending POST request to create movie...")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: verify that the movie was created")
		assert_that(response.status_code).is_equal_to(201)
		data = response.json()
		assert_that(data["title"]).is_equal_to("Title 1")
		assert_that(
			Movie.objects.filter(title="Title 1").exists()).is_true()
	
	def test_create_movie_unauthorized(self, live_server):
		"""Verify that impossible to create movie without authentication."""
		logger.info("Step 1 : create the test data with the movie "
		            "from the unauthorized user.")
		url = f"{live_server.url}/api/movies/"
		payload = {
			"title": "Unauthorized",
			"description": "Should fail",
			"release_date": str(date(2022, 1, 1)),
			"rating": 5.0,
			"genre_ids": [],
		}
		
		logger.info("Step 2: Sending POST request without authentication...")
		response = requests.post(url, json=payload)
		assert_that(response.status_code).is_equal_to(401)
	
	def test_get_movie(self, live_server, session):
		"""Verify that possible to retrieve a single movie by ID via GET request.

		Steps:
		1. Створюємо фільм у БД.
		2. Надсилаємо GET-запит на /api/movies/{id}.
		3. Перевіряємо статус-код = 200.
		4. Переконуємось, що дані відповідають створеному фільму.
		"""
		logger.info("Step 1 : create the test data with the movie")
		movie = Movie.objects.create(
			title="Matrix",
			description="Sci-fi classic",
			release_date=date(1999, 3, 31),
			rating=9.0
		)
		url = f"{live_server.url}/api/movies/{movie.id}"
		
		logger.info("Step 2: Sending GET request to retrieve movie...")
		response = session.get(url)
		
		logger.info("Step 3: verify adde data")
		assert_that(response.status_code).is_equal_to(200)
		data = response.json()
		assert_that(data["title"]).is_equal_to("Matrix")
		assert_that(data["rating"]).is_equal_to(9.0)
	
	def test_get_nonexistent_movie(self, live_server, session):
		"""Verify that impossible to retrieve non-existent movie."""
		url = f"{live_server.url}/api/movies/9999"
		logger.info("Step 1: Sending GET request for non-existent movie...")
		response = session.get(url)
		assert_that(response.status_code).is_equal_to(404)
	
	def test_list_movies(self, live_server, session):
		"""Verify that possible to get list all movies via GET request."""
		logger.info("Step 1 : create the test data with the movies list")
		Movie.objects.create(title="Movie1", description="Desc1",
		                     release_date=date(2020, 1, 1), rating=7.5)
		Movie.objects.create(title="Movie2", description="Desc2",
		                     release_date=date(2021, 1, 1), rating=8.0)
		
		url = f"{live_server.url}/api/movies/"
		logger.info("Step 2: Sending GET request to list movies...")
		response = session.get(url)
		
		logger.info("Step 3: verify the movies list")
		assert_that(response.status_code).is_equal_to(200)
		titles = [m["title"] for m in response.json()]
		assert_that(titles).contains("Movie1", "Movie2")
	
	def test_update_movie(self, live_server, session):
		"""
		Test: Update an existing movie via PUT request.
		Steps:
		1. Створюємо фільм у БД.
		2. Формуємо payload з новими даними.
		3. Надсилаємо PUT-запит на /api/movies/{id}.
		4. Перевіряємо статус-код = 200.
		5. Перевіряємо, що дані у БД оновились.
		"""
		logger.info("Step 1: create test movie for update")
		movie = Movie.objects.create(title="Old", description="Old desc",
		                             release_date=date(2010, 1, 1), rating=5.0)
		url = f"{live_server.url}/api/movies/{movie.id}"
		
		logger.info("Step 2: prepare data for update")
		payload = {
			"title": "New",
			"description": "New desc",
			"release_date": str(date(2015, 1, 1)),
			"rating": 8.0,
			"genre_ids": [],
		}
		logger.info("Step 3 Sending PUT request to update movie...")
		response = session.put(url, json=payload)
		
		logger.info("Step 4: verify that the movie was updated.")
		assert_that(response.status_code).is_equal_to(200)
		movie.refresh_from_db()
		assert_that(movie.title).is_equal_to("New")
		assert_that(movie.rating).is_equal_to(8.0)
	
	def test_delete_movie(self, live_server, session):
		"""Verify that possible to delete an existing movie via DELETE request."""
		logger.info("Step 1: create test movie")
		movie = Movie.objects.create(title="ToDelete", description="Temp",
		                             release_date=date(2012, 1, 1), rating=6.0)
		url = f"{live_server.url}/api/movies/{movie.id}"
		
		logger.info("Step 2: sending DELETE request to remove movie")
		response = session.delete(url)
		
		logger.info("Step 3: verify that the movie was deleted")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(Movie.objects.filter(id=movie.id).exists()).is_false()
	
	# ------------------ Reviews ------------------
	def test_add_review(self, live_server, session, user):
		"""Verify that possible to add review to a movie via POST request."""
		logger.info("Step 1: create test movie")
		movie = Movie.objects.create(
			title="Reviewed",
			description="Desc",
			release_date=date(2019, 1, 1),
			rating=7.0
		)
		url = f"{live_server.url}/api/movies/reviews/"
		payload = {"movie_id": movie.id, "text": "Great movie!", "score": 9}
		
		logger.info("Step 2: Sending POST request to add review...")
		response = session.post(url, json=payload)
		assert_that(response.status_code).is_equal_to(201)
		
		logger.info("Step 3: Verify that the review was added")
		data = response.json()
		assert_that(data["text"]).is_equal_to("Great movie!")
		assert_that(
			Review.objects.filter(movie=movie, user=user).exists()).is_true()
	
	def test_list_reviews(self, live_server, session, user):
		"""Verify that possible to get list reviews for a movie via GET request.

		Steps:
		1. Створюємо фільм у БД.
		2. Додаємо кілька відгуків від користувача.
		3. Надсилаємо GET-запит на /api/movies/reviews/{movie_id}.
		4. Перевіряємо статус-код = 200.
		5. Переконуємось, що у відповіді є створені відгуки.
		"""
		logger.info("Step 1: create test movie with review")
		movie = Movie.objects.create(
			title="Reviewed2",
			description="Desc2",
			release_date=date(2020, 1, 1),
			rating=8.0)
		
		logger.info("Step 2: create test review for the movie")
		Review.objects.create(movie=movie, user=user, text="Nice!", score=8)
		Review.objects.create(movie=movie, user=user, text="Could be better",
		                      score=6)
		url = f"{live_server.url}/api/movies/reviews/{movie.id}"
		
		logger.info("Step 3: Sending GET request to list reviews...")
		response = session.get(url)
		
		logger.info("Step 3: verify that review was added")
		assert_that(response.status_code).is_equal_to(200)
		texts = [r["text"] for r in response.json()]
		assert_that(texts).contains("Nice!", "Could be better")
