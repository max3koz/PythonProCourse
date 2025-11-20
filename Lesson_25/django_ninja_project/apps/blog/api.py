from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.responses import Response

from .models import Post, Tag, Comment
from .schemas import PostIn, PostOut, TagIn, TagOut, CommentIn, CommentOut

blog_router = Router(tags=["blog"])


# ------------------ Tags ------------------
@blog_router.post("/tags/", response=TagOut)
@login_required
def create_tag(request, payload: TagIn) -> Response:
	"""Create a new tag. Requires authentication."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	tag = Tag.objects.create(**payload.dict())
	return Response(TagOut.from_orm(tag), status=201)


@blog_router.get("/tags/", response=list[TagOut])
@login_required
def list_tags(request):
	"""Retrieve all tags."""
	return Tag.objects.all()


# ------------------ Posts ------------------
@blog_router.post("/", response=PostOut)
@login_required
def create_post(request, payload: PostIn) -> Response:
	"""Create a new blog post. Requires authentication."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	post = Post.objects.create(
		title=payload.title,
		content=payload.content,
		author=request.user,
	)
	post.tags.set(Tag.objects.filter(id__in=payload.tag_ids))
	return Response(PostOut.from_orm(post), status=201)


@blog_router.get("/", response=list[PostOut])
@login_required
def list_posts(request, tag: str = None):
	"""Retrieve all blog posts. Supports filtering by tag name."""
	qs = Post.objects.all()
	if tag:
		qs = qs.filter(tags__name__icontains=tag)
	return qs


@blog_router.get("/{post_id}", response=PostOut)
@login_required
def get_post(request, post_id: int):
	"""Retrieve a single blog post by ID."""
	return get_object_or_404(Post, id=post_id)


@blog_router.put("/{post_id}", response=PostOut)
@login_required
def update_post(request, post_id: int, payload: PostIn):
	"""Update an existing blog post. Requires authentication."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	post = get_object_or_404(Post, id=post_id)
	post.title = payload.title
	post.content = payload.content
	post.save()
	post.tags.set(Tag.objects.filter(id__in=payload.tag_ids))
	return post


@blog_router.delete("/{post_id}")
@login_required
def delete_post(request, post_id: int):
	"""Delete a blog post. Requires authentication."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	post = get_object_or_404(Post, id=post_id)
	post.delete()
	return {"success": True}


# ------------------ Comments ------------------
@blog_router.post("/comments/", response=CommentOut)
@login_required
def add_comment(request, payload: CommentIn) -> Response:
	"""Add a comment to a blog post. Requires authentication."""
	if not request.user.is_authenticated:
		return Response({"detail": "Authentication required"}, status=401)
	post = get_object_or_404(Post, id=payload.post_id)
	comment = Comment.objects.create(post=post, user=request.user,
	                                 text=payload.text)
	return Response(CommentOut.from_orm(comment), status=201)


@blog_router.get("/comments/{post_id}", response=list[CommentOut])
@login_required
def list_comments(request, post_id: int):
	"""Retrieve all comments for a specific blog post."""
	post = get_object_or_404(Post, id=post_id)
	return post.comments.all()
