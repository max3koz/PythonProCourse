import logging

import pytest
import requests
from apps.blog.models import Post, Tag, Comment
from assertpy import assert_that
from django.contrib.auth.models import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestBlogAPI:
	"""
	Integration tests for Blog Platform API.
	Covers CRUD for tags, posts, and comments.
	"""
	
	@pytest.fixture
	def user(self) -> User:
		"""Fixture: creates a test user in DB."""
		return User.objects.create_user(username="maksym", password="secret123")
	
	@pytest.fixture
	def session(self, live_server, user):
		"""
		Fixture: creates an authenticated session via API login."""
		logger.info("Precondition step 1: Logging in user via API ")
		s = requests.Session()
		login_url = f"{live_server.url}/api/accounts/login"
		payload = {"username": "maksym", "password": "secret123"}
		response = s.post(login_url, json=payload)
		assert response.status_code == 200
		
		token = response.json()["token"]
		logger.info(f"Precondition step 2: Received token: {token}")
		s.headers.update({"X-CSRFToken": token})
		return s
	
	# ------------------ Tags ------------------
	def test_create_tag(self, live_server, session):
		"""Verify that possible to create a new tag."""
		logger.info("Step 1: repare payload with tag name")
		url = f"{live_server.url}/api/blog/tags/"
		payload = {"name": "Tech"}
		
		logger.info("Step 2: Sending POST request to create tag")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: verify tag exists in DB")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(Tag.objects.filter(name="Tech").exists()).is_true()
	
	def test_list_tags(self, live_server, session):
		"""Verify that possible to get the list all tags."""
		logger.info("Step 1: create tags in DB.")
		Tag.objects.create(name="Python")
		Tag.objects.create(name="Django")
		url = f"{live_server.url}/api/blog/tags/"
		
		logger.info("Step 2: sending GET request to list tags")
		response = session.get(url)
		
		logger.info("Step 3: verify response contains created tags")
		assert_that(response.status_code).is_equal_to(200)
		names = [t["name"] for t in response.json()]
		assert_that(names).contains("Python", "Django")
	
	# ------------------ Posts ------------------
	def test_create_post(self, live_server, session, user):
		"""Verify that possible to create a new blog post."""
		logger.info("Step 1: create tag in DB.")
		tag = Tag.objects.create(name="AI")
		url = f"{live_server.url}/api/blog/"
		payload = {"title": "My First Post", "content": "Hello World",
		           "tag_ids": [tag.id]}
		
		logger.info("Step 2: Sending POST request to create post")
		response = session.post(url, json=payload)
		
		logger.info("step 3: Verify post exists in DB.")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(
			Post.objects.filter(title="My First Post").exists()).is_true()
	
	def test_create_post_unauthorized(self, live_server):
		"""Verify that impossible to create a post without authentication."""
		logger.info("Step 1: prepare payload with post data.")
		url = f"{live_server.url}/api/blog/"
		payload = {"title": "Unauthorized", "content": "Fail", "tag_ids": []}
		
		logger.info("Step 2: sending POST request without authentication")
		response = requests.post(url, json=payload)
		
		logger.info("Step 3: verify status code = 404.")
		assert_that(response.status_code).is_equal_to(404)
	
	def test_list_posts(self, live_server, session):
		"""Verify that possible to get list all blog posts."""
		logger.info("Step 1: create posts in DB")
		Post.objects.create(title="Post1", content="Content1",
		                    author=User.objects.first())
		Post.objects.create(title="Post2", content="Content2",
		                    author=User.objects.first())
		url = f"{live_server.url}/api/blog/"
		
		logger.info("Step 2: sending GET request to list posts ")
		response = session.get(url)
		
		logger.info("Step 3: verify response contains created posts.")
		assert_that(response.status_code).is_equal_to(200)
		titles = [p["title"] for p in response.json()]
		assert_that(titles).contains("Post1", "Post2")
	
	def test_get_post(self, live_server, session, user):
		"""Verify that possible to retrieve a single post by ID."""
		logger.info("Step 1: create post in DB")
		post = Post.objects.create(title="Unique", content="Details",
		                           author=user)
		url = f"{live_server.url}/api/blog/{post.id}"
		
		logger.info("Step 2: sending GET request to retrieve post ")
		response = session.get(url)
		
		logger.info("Step 3: verify response matches created post")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(response.json()["title"]).is_equal_to("Unique")
	
	def test_update_post(self, live_server, session, user):
		"""Verify that possible  to  update an existing post."""
		logger.info("Step 1: create post in DB.")
		post = Post.objects.create(title="Old", content="Old content",
		                           author=user)
		url = f"{live_server.url}/api/blog/{post.id}"
		payload = {"title": "New", "content": "New content", "tag_ids": []}
		
		logger.info("Step 3: sending PUT request to update post ")
		response = session.put(url, json=payload)
		
		logger.info("Step 3: Verify DB updated.")
		assert_that(response.status_code).is_equal_to(200)
		post.refresh_from_db()
		assert_that(post.title).is_equal_to("New")
	
	def test_update_post_nonexistent(self, live_server, session):
		"""Verify that impossible to update a non-existent post."""
		logger.info("Step 1: prepare post data.")
		url = f"{live_server.url}/api/blog/9999"
		payload = {"title": "DoesNotExist", "content": "Fail", "tag_ids": []}
		
		logger.info("Step 2: sending PUT request for non-existent post ")
		response = session.put(url, json=payload)
		
		logger.info("Step 3: Verify status code = 404.")
		assert_that(response.status_code).is_equal_to(404)
	
	def test_delete_post(self, live_server, session, user):
		"""Verify that possible to delete a post."""
		logger.info("Step 1: Create post in DB.")
		post = Post.objects.create(title="ToDelete", content="Temp",
		                           author=user)
		url = f"{live_server.url}/api/blog/{post.id}"
		
		logger.info("Step 2: sending DELETE request to remove post")
		response = session.delete(url)
		
		logger.info("Step 3: Verify post removed from DB.")
		assert_that(response.status_code).is_equal_to(200)
		assert_that(Post.objects.filter(id=post.id).exists()).is_false()
	
	def test_delete_post_unauthorized(self, live_server, user):
		"""Verify that impossible to delete a post without authentication."""
		logger.info("Step 1: create post in DB")
		post = Post.objects.create(title="Protected", content="Secret",
		                           author=user)
		url = f"{live_server.url}/api/blog/{post.id}"
		
		logger.info("Step 2: sending DELETE request without authentication ")
		response = requests.delete(url)
		
		logger.info("Step 3: Verify status code = 404.")
		assert_that(response.status_code).is_equal_to(404)
	
	# ------------------ Comments ------------------
	def test_add_comment(self, live_server, session, user):
		"""Verify that possible to add a comment to a blog post."""
		logger.info("Step 1: reate a post in the database.")
		post = Post.objects.create(title="Commented", content="Desc",
		                           author=user)
		url = f"{live_server.url}/api/blog/comments/"
		payload = {"post_id": post.id, "text": "Nice post!"}
		
		logger.info("Step 2: sending POST request to add comment")
		response = session.post(url, json=payload)
		
		logger.info("Step 3: verify comment exists")
		assert_that(response.status_code).is_equal_to(201)
		assert_that(Comment.objects.filter(post=post, user=user,
		                                   text="Nice post!").exists()).is_true()
	
	def test_add_comment_unauthorized(self, live_server, user):
		"""Verify that impossible to add a comment without authentication."""
		logger.info("Step 1: create post in DB")
		post = Post.objects.create(title="NoAuth", content="Desc", author=user)
		url = f"{live_server.url}/api/blog/comments/"
		payload = {"post_id": post.id, "text": "Fail comment"}
		
		logger.info("Step 2: sending POST request without authentication")
		response = requests.post(url, json=payload)
		
		logger.info("Step 3: verify status code = 404")
		assert_that(response.status_code).is_equal_to(404)
	
	def test_list_comments(self, live_server, session, user):
		"""Verify that possible to get list comments for a specific blog post."""
		logger.info("Step 1: Create a post in the database.")
		post = Post.objects.create(title="Commented2", content="Desc2",
		                           author=user)
		Comment.objects.create(post=post, user=user, text="First comment")
		Comment.objects.create(post=post, user=user, text="Second comment")
		url = f"{live_server.url}/api/blog/comments/{post.id}"
		
		logger.info("Step 2: sending GET request to list comments")
		response = session.get(url)
		
		logger.info("Step 3: Verify response contains created comments")
		assert_that(response.status_code).is_equal_to(200)
		texts = [c["text"] for c in response.json()]
		assert_that(texts).contains("First comment", "Second comment")
	
	def test_list_comments_nonexistent_post(self, live_server, session):
		"""Verify that impossible to get list comments for a non-existent post."""
		url = f"{live_server.url}/api/blog/comments/9999"
		logger.info(
			"Step 1: sending GET request for non-existent post comments")
		response = session.get(url)
		assert_that(response.status_code).is_equal_to(404)
