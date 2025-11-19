from datetime import date

from ninja import Schema


class GenreIn(Schema):
	name: str


class GenreOut(Schema):
	id: int
	name: str


class MovieIn(Schema):
	title: str
	description: str
	release_date: date
	rating: float
	genre_ids: list[int]


class MovieOut(Schema):
	id: int
	title: str
	description: str
	release_date: date
	rating: float
	genres: list[GenreOut]


class ReviewIn(Schema):
	movie_id: int
	text: str
	score: int


class ReviewOut(Schema):
	id: int
	movie_id: int
	text: str
	score: int
	user_id: int
