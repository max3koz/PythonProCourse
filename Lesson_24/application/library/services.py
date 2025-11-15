from __future__ import annotations

from typing import List, Dict, Any

from pymongo import MongoClient


def get_mongo_client() -> MongoClient:
	"""Initializing the MongoDB client."""
	return MongoClient("mongodb://127.0.0.1:27017")


def nosql_save_books(items: List[Dict[str, Any]]) -> int:
	"""Stores a list of books in MongoDB."""
	client = get_mongo_client()
	db = client["application"]
	res = db.books.insert_many(items)
	return len(res.inserted_ids)


def nosql_read_books(limit: int = 1000) -> List[Dict[str, Any]]:
	"""Reads books with MongoDB."""
	client = get_mongo_client()
	db = client["application"]
	docs = list(db.books.find().limit(limit))
	return docs


def nosql_delete_book_by_title(title: str) -> int:
	"""Delete book by the title with MongoDB."""
	client = get_mongo_client()
	db = client["application"]
	res = db.books.delete_one({"title": title})
	return res.deleted_count


def nosql_clear_books() -> int:
	"""Clear database with MongoDB."""
	client = get_mongo_client()
	db = client["application"]
	res = db.books.delete_many({})
	return res.deleted_count
