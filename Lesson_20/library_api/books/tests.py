import logging
from random import randint

import pytest
from assertpy import assert_that
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from .models import Book

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture
def user() -> User:
	"""The fixture: regular user."""
	return User.objects.create_user(username='user', password='pass123')


@pytest.fixture
def admin() -> User:
	"""The fixture: administrator."""
	return User.objects.create_superuser(username='admin', password='adminpass')


@pytest.fixture
def client() -> APIClient:
	"""DRF API client"""
	return APIClient()
 

@pytest.mark.django_db
def test_create_book_authenticated(client: APIClient, user: User) -> None:
	"""Verify that a book create by an authorized user"""
	logger.info("Step 1: User authorization. ")
	client.force_authenticate(user=user)
	
	logger.info("Step 2: Sending a POST request to create a book.")
	response = client.post('/api/books/', {
		'title': 'Test Book',
		'author': 'Author1',
		'genre': 'Drama',
		'publication_year': 2022
	})
	
	logger.info(f"Step 3:Verify that response status 201 and "
	            f"the book title 'Test Book'")
	assert_that(response.status_code == 201).is_true()
	assert_that(response.data['title']).is_equal_to('Test Book')


@pytest.mark.django_db
def test_get_book_detail():
	"""Verify that all book parameters are displayed as expected."""
	logger.info("Step 1: Creating a test user and a test book. ")
	user = User.objects.create_user(username='user1', password='pass123')
	book = Book.objects.create(
		title='Test Book',
		author='Test Author',
		genre='Test Genre',
		publication_year=2020,
		user=user
	)
	
	logger.info("Step 2: User authorization. ")
	client = APIClient()
	client.force_authenticate(user=user)
	
	logger.info("Step 3: Sending a GET request to get the detailed a book.")
	response = client.get(f'/api/books/{book.id}/')
	
	logger.info(f"Step 4: Verify that response status 200 and "
	            f"all book details are expected.")
	assert_that(response.status_code == 200).is_true()
	data = response.json()
	assert_that(data['id']).is_not_none()
	assert_that(data['title']).is_equal_to('Test Book')
	assert_that(data['author']).is_equal_to('Test Author')
	assert_that(data['genre']).is_equal_to('Test Genre')
	assert_that(data['publication_year']).is_equal_to(2020)
	assert_that(data['user']).is_equal_to(user.id)


@pytest.mark.django_db
def test_list_books_authenticated(client: APIClient, user: User) -> None:
	"""Verify that it is possible to get a list of books by an authorized user"""
	logger.info("Step 1: Creating a test user and 2 test book. ")
	client.force_authenticate(user=user)
	Book.objects.create(title='Book1',
	                    author='Author1',
	                    genre='Drama',
	                    publication_year=2020)
	Book.objects.create(title='Book2',
	                    author='Author2',
	                    genre='History',
	                    publication_year=2010)
	
	logger.info("Step 2: Sending a GET request to get the book list.")
	response = client.get('/api/books/')
	
	logger.info(f"Step 3: Verify that response status 200 and "
	            f"book list contain one book.")
	assert_that(response.status_code == 200).is_true()
	assert_that(len(response.data['results'])).is_equal_to(2)


@pytest.mark.django_db
def test_list_books_unauthenticated(client: APIClient) -> None:
	"""
	Verify that it is not possible to get a list of books
	by an unauthorized user
	"""
	logger.info("Step 1: Creating a test book. ")
	Book.objects.create(title='Book1',
	                    author='Author1',
	                    genre='Drama',
	                    publication_year=2020)
	
	logger.info("Step 2: Sending a GET request to get the book list.")
	response = client.get('/api/books/')
	
	logger.info(f"Step 3: Verify that response status 401 and get warning "
	            f"that authentication credentials were not provided.")
	assert_that(response.status_code == 401).is_true()
	assert_that(response.data['detail']).is_equal_to(
		'Authentication credentials were not provided.')


@pytest.mark.django_db
def test_filter_books_by_author():
	"""Verify that filtering by author name works"""
	logger.info("Step 1: Creating a test user and 2 test book. ")
	user = User.objects.create_user(username='user1',
	                                password='pass123')
	Book.objects.create(title='Book A',
	                    author='Author X',
	                    genre='Genre',
	                    publication_year=2000,
	                    user=user)
	Book.objects.create(title='Book B',
	                    author='Author Y',
	                    genre='Genre',
	                    publication_year=2001,
	                    user=user)
	
	logger.info("Step 2: User authorization. ")
	client = APIClient()
	client.force_authenticate(user=user)
	
	logger.info("Step 3: Sending a GET request to get the book by author name.")
	response = client.get('/api/books/?author=Author X')
	
	logger.info(f"Step 4: Verify that response status 200 and "
	            f"get expected book by the filtered author name.")
	assert_that(response.status_code == 200).is_true()
	data = response.json()['results']
	assert_that(len(data)).is_equal_to(1)
	assert_that(data[0]['author']).is_equal_to('Author X')


@pytest.mark.django_db
def test_filter_books_by_title():
	"""Verify that filtering by title works"""
	logger.info("Step 1: Creating a test user and 2 test book. ")
	user = User.objects.create_user(username='user2',
	                                password='pass123')
	Book.objects.create(title='Python one book',
	                    author='Author A',
	                    genre='Genre',
	                    publication_year=2010,
	                    user=user)
	Book.objects.create(title='Django second book',
	                    author='Author B',
	                    genre='Genre',
	                    publication_year=2011,
	                    user=user)
	
	logger.info("Step 2: User authorization. ")
	client = APIClient()
	client.force_authenticate(user=user)
	
	logger.info("Step 3: Sending a GET request to get the book by title.")
	response = client.get('/api/books/?search=Python')
	
	logger.info(f"Step 4: Verify that response status 200 and "
	            f"get expected book by the filtered title.")
	assert_that(response.status_code == 200).is_true()
	data = response.json()['results']
	assert_that(len(data)).is_equal_to(1)
	assert_that('Python' in data[0]['title']).is_true()


@pytest.mark.django_db
def test_filter_books_by_publication_year():
	"""Verify that filtering by publication year works"""
	logger.info("Step 1: Creating a test user and 2 test book. ")
	user = User.objects.create_user(username='user3',
	                                password='pass123')
	Book.objects.create(title='Book 2000',
	                    author='Author A',
	                    genre='Genre',
	                    publication_year=2000,
	                    user=user)
	Book.objects.create(title='Book 2020',
	                    author='Author B',
	                    genre='Genre',
	                    publication_year=2020,
	                    user=user)
	
	logger.info("Step 2: User authorization. ")
	client = APIClient()
	client.force_authenticate(user=user)
	
	logger.info(
		"Step 3: Sending a GET request to get the book by publication year.")
	response = client.get('/api/books/?publication_year=2020')
	
	logger.info(f"Step 4: Verify that response status 200 and "
	            f"get expected book by the filtered year.")
	assert response.status_code == 200
	data = response.json()['results']
	assert len(data) == 1
	assert data[0]['publication_year'] == 2020


@pytest.mark.django_db
def test_books_pagination_page_size_10():
	"""Pagination check of 10 items per page"""
	logger.info("Step 1: Creating a test user. ")
	user = User.objects.create_user(username='user1', password='pass123')
	
	logger.info("Step 2: User authorization. ")
	client = APIClient()
	client.force_authenticate(user=user)
	
	logger.info("Step 3: Creating 25 test books. ")
	for i in range(25):
		Book.objects.create(
			title=f'Book {i}',
			author=f'Author {randint(1, 10)}',
			genre='Genre',
			publication_year=2000 + randint(1, 25),
			user=user
		)
	
	logger.info("Step 4: Sending a GET request to get books from page 1.")
	response_page_1 = client.get('/api/books/?page=1')
	
	logger.info(f"Step 5: Verify that response status 200 and "
	            f"get expected 10 book on page 1.")
	assert_that(response_page_1.status_code == 200).is_true()
	data_1 = response_page_1.json()
	assert_that(len(data_1['results'])).is_equal_to(10)
	assert_that(data_1['count']).is_equal_to(25)
	assert_that(data_1['next']).is_not_none()
	assert_that(data_1['previous']).is_none()
	
	logger.info("Step 6: Sending a GET request to get books from page 3.")
	response_page_3 = client.get('/api/books/?page=3')
	
	logger.info(f"Step 7: Verify that response status 200 and "
	            f"get expected 10 book on page 1.")
	assert_that(response_page_3.status_code == 200).is_true()
	data_3 = response_page_3.json()
	assert_that(len(data_3['results'])).is_equal_to(5)
	assert_that(data_3['next']).is_none()
	assert_that(data_3['previous']).is_not_none()


@pytest.mark.django_db
def test_update_book_authenticated(client: APIClient, user: User) -> None:
	"""Verify that an authorized user can update a book"""
	logger.info("Step 1: Creating a test user and 2 test book. ")
	client.force_authenticate(user=user)
	book = Book.objects.create(title='Old Title',
	                           author='Author1',
	                           genre='Drama',
	                           publication_year=2020)
	
	logger.info("Step 2: Sending a PATCH request to update books title.")
	response = client.patch(f'/api/books/{book.id}/', {'title': 'New Title'})
	
	logger.info(f"Step 3: Verify that response status 200 and "
	            f"get expected book title updated.")
	assert response.status_code == 200
	assert response.data['title'] == 'New Title'


@pytest.mark.django_db
def test_delete_book_admin_only(client: APIClient, admin: User) -> None:
	"""Verify that a book can be deleted by an administrator"""
	logger.info("Step 1: Creating a administrator user and test book. ")
	client.force_authenticate(user=admin)
	book = Book.objects.create(title='Book to Delete',
	                           author='Author1',
	                           genre='Drama',
	                           publication_year=2020)
	
	logger.info("Step 2: Sending a DELETE request to delete book.")
	response = client.delete(f'/api/books/{book.id}/')
	
	logger.info(f"Step 3: Verify that response status 204.")
	assert_that(response.status_code).is_equal_to(204)


@pytest.mark.django_db
def test_delete_book_non_admin_forbidden(client: APIClient, user: User) -> None:
	"""Verify that a non-administrator cannot delete a workbook"""
	logger.info("Step 1: Creating a non-administrator user and test book. ")
	client.force_authenticate(user=user)
	book = Book.objects.create(title='Book to Delete',
	                           author='Author1',
	                           genre='Drama',
	                           publication_year=2020)
	
	logger.info("Step 2: Sending a DELETE request to delete book.")
	response = client.delete(f'/api/books/{book.id}/')
	
	logger.info(f"Step 3: Verify that response status 403.")
	assert_that(response.status_code == 403).is_true()
	
	logger.info(f"Step 4: Verify that response contain message "
	            f"the only administrator can delete book.")
	assert_that(response.data['detail']).is_equal_to(
		'Only an administrator can delete books.')
	
	logger.info("Step 5: Sending a GET request to get the detailed a book.")
	response = client.get(f'/api/books/{book.id}/')
	
	logger.info(f"Step 6: Verify that response status 200 and "
	            f"all book details are expected.")
	assert_that(response.status_code == 200).is_true()
	data = response.json()
	assert_that(data['id']).is_not_none()
