from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
	"""
	Represents a tag that can be assigned to blog posts.

	Attributes:
		name (str): The unique name of the tag.
	"""
	name: str = models.CharField(max_length=50, unique=True)
	
	def __str__(self) -> str:
		return self.name


class Post(models.Model):
	"""
	Represents a blog post.

	Attributes:
		title (str): The title of the post.
		content (str): The main content of the post.
		author (User): The user who created the post.
		created_at (datetime): The timestamp when the post was created.
		updated_at (datetime): The timestamp when the post was last updated.
		tags (ManyToManyField): Tags associated with the post.
	"""
	title: str = models.CharField(max_length=200)
	content: str = models.TextField()
	author: User = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
	updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
	tags: models.ManyToManyField = models.ManyToManyField(Tag,
	                                                      related_name="posts")
	
	def __str__(self) -> str:
		return self.title


class Comment(models.Model):
	"""
	Represents a comment on a blog post.

	Attributes:
		post (Post): The blog post being commented on.
		user (User): The user who wrote the comment.
		text (str): The content of the comment.
		created_at (datetime): The timestamp when the comment was created.
	"""
	post: Post = models.ForeignKey(Post, on_delete=models.CASCADE,
	                               related_name="comments")
	user: User = models.ForeignKey(User, on_delete=models.CASCADE)
	text: str = models.TextField()
	created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
	
	def __str__(self) -> str:
		return f"Comment by {self.user.username} on {self.post.title}"
