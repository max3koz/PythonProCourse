from datetime import datetime

from ninja import Schema


class TagIn(Schema):
	name: str


class TagOut(Schema):
	id: int
	name: str


class PostIn(Schema):
	title: str
	content: str
	tag_ids: list[int]


class PostOut(Schema):
	id: int
	title: str
	content: str
	author_id: int
	created_at: datetime
	updated_at: datetime
	tags: list[TagOut]


class CommentIn(Schema):
	post_id: int
	text: str


class CommentOut(Schema):
	id: int
	post_id: int
	user_id: int
	text: str
	created_at: datetime
