from __future__ import annotations

import random
from typing import List

from django.core.management.base import BaseCommand
from library.models import Author, Book, Review


class Command(BaseCommand):
	"""Заповнює базу тестовими даними (автори, книги, відгуки)."""
	
	def handle(self, *args, **kwargs) -> None:
		authors: List[Author] = []
		for i in range(10):
			authors.append(Author.objects.create(name=f"Author {i + 1}"))
		
		books: List[Book] = []
		for a in authors:
			for j in range(5):
				books.append(Book.objects.create(author=a,
				                                 title=f"Book {a.name}-{j + 1}",
				                                 published_year=random.choice(
					                                 [2018, 2019, 2020, 2021,
					                                  2022])))
		
		for b in books:
			for _ in range(random.randint(0, 20)):
				Review.objects.create(book=b, rating=random.randint(1, 5),
				                      comment="Nice!")
		self.stdout.write(
			self.style.SUCCESS("Seeded 10 authors, 50 books, ~reviews"))
