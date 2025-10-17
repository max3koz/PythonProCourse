import random

import pytest
from assertpy import assert_that
from django.http import HttpResponse
from django.test import Client

client: Client = Client()


def test_home_view() -> None:
	"""
	Verify that the main page returns a status of 200 and contains
	the expected text.	"""
	response: HttpResponse = client.get('/home/')
	assert_that(response.status_code).is_equal_to(200)
	assert_that(response.content.decode()).contains("Welcome to the home page")


def test_about_view() -> None:
	"""
	Verify that the 'about' page returns a status of 200 and contains
	the text 'About Us'.	"""
	response: HttpResponse = client.get('/about/')
	assert_that(response.status_code).is_equal_to(200)
	assert_that(response.content.decode()).contains("About Us")


def test_contact_view() -> None:
	"""
	Verify that the 'contact' page returns a status of 200 and contains
	the text 'Contact us'.	"""
	response: HttpResponse = client.get('/contact/')
	assert_that(response.status_code).is_equal_to(200)
	assert_that(response.content.decode()).contains("Contact Us")


@pytest.mark.parametrize("post_id", [1, 123, 999])
def test_post_view(post_id: int) -> None:
	"""
	Verify that the page "post <id>' returns a status of 200 and contains
	the post ID.	"""
	response: HttpResponse = client.get(f'/post/{post_id}/')
	assert_that(response.status_code).is_equal_to(200)
	assert_that(response.content.decode()).contains(str(post_id))


@pytest.mark.parametrize("username", ["john", "Maria", "admin"])
def test_profile_view(username: str) -> None:
	"""
	Verify that the page 'profile/<username>' returns a status of 200
	and contains the <username>.	"""
	response: HttpResponse = client.get(f'/profile/{username}/')
	assert_that(response.status_code).is_equal_to(200)
	assert_that(response.content.decode()).contains(username)


def test_event_view() -> None:
	"""
	Checks that the page '/event/<year>/<month>/<day>/' returns a status of 200
	and contains a date.	"""
	year = random.randint(1900, 2025)
	month = random.randint(1, 12)
	day = random.randint(1, 28)
	response: HttpResponse = client.get(f'/event/{year}/{month}/{day}/')
	assert_that(response.status_code).is_equal_to(200)
	assert_that(response.content.decode()).contains(
		f"Event date: {year}-{month}-{day}")


def test_invalid_post_id() -> None:
	"""Verify that the request '/post/abc/' returns a 404 error."""
	response: HttpResponse = client.get('/post/abc/')
	assert_that(response.status_code).is_equal_to(404)


def test_invalid_profile_username() -> None:
	"""Verify that the request '/profile/user123/' returns a 404 error."""
	response: HttpResponse = client.get('/profile/user123/')
	assert_that(response.status_code).is_equal_to(404)


def test_invalid_event_date() -> None:
	"""Verify that the request '/event/20a5/1x/3z/' returns a 404 error."""
	response: HttpResponse = client.get('/event/20a5/1x/3z/')
	assert_that(response.status_code).is_equal_to(404)
