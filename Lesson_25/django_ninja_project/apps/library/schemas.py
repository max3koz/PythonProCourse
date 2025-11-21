from datetime import datetime

from ninja import Schema


class BookIn(Schema):
	title: str
	author: str
	genre: str


class BookOut(Schema):
	id: int
	title: str
	author: str
	genre: str
	available: bool


class RentalIn(Schema):
	book_id: int
	return_date: datetime


class RentalOut(Schema):
	id: int
	book_id: int
	user_id: int
	rented_at: datetime
	return_date: datetime | None
