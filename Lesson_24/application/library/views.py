from __future__ import annotations

import random
import time
from typing import Dict, Any, List

from celery.result import AsyncResult
from django.core.cache import cache
from django.db import connection
from django.db.models import Avg, Count
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from .models import Author, Review
from .models import Book
from .services import nosql_save_books, nosql_read_books
from .tasks import import_books_task

CACHE_KEY_BOOK_LIST: str = "library:book_list"


@cache_page(60 * 5)
def books_unoptimized_view(request) -> Any:
	"""Without optimization: N+1 for author and reviews. Execution time measurement."""
	t0: float = time.perf_counter()
	data: List[Dict[str, Any]] = []
	for b in Book.objects.all():
		author = b.author
		reviews = list(b.reviews.all())
		data.append({"book": b, "author": author, "reviews": reviews})
	elapsed_unoptimized: float = time.perf_counter() - t0
	return render(request, "library/performance_results.html",
	              {"data": data, "elapsed": elapsed_unoptimized,
	               "optimized": False})


@cache_page(60 * 5)
def books_optimized_view(request) -> Any:
	"""
	With optimization: select_related for author, prefetch_related for reviews.
	Execution time measurement.
	"""
	t0: float = time.perf_counter()
	qs = (Book.objects.select_related("author").
	      prefetch_related(Prefetch("reviews",
	                                queryset=Review.objects.all())))
	data = [{"book": b, "author": b.author, "reviews": list(b.reviews.all())}
	        for b in qs]
	elapsed_optimized: float = time.perf_counter() - t0
	return render(request,
	              "library/performance_results.html",
	              {"data": data, "elapsed": elapsed_optimized,
	               "optimized": True})


@cache_page(60 * 5)
def book_list_view(request) -> Any:
	"""Displays a list of books with authors. Caches the result."""
	data = cache.get(CACHE_KEY_BOOK_LIST)
	if data is None:
		qs = (Book.objects.select_related("author").
		      annotate(review_count=Count("reviews")))
		data = list(qs.values("id", "title", "author__name", "review_count"))
		cache.set(CACHE_KEY_BOOK_LIST, data, timeout=60 * 5)
	return render(request,
	              "library/book_list.html",
	              {"books": data})


@cache_page(60 * 5)
def aggregates_view(request) -> Any:
	"""
	Calculating the average rating of each author's books, the number of reviews
	for each book, sorting books by the number of reviews and the average rating.
	"""
	authors_stats = (
		Author.objects.annotate(
			avg_book_rating=Avg("books__reviews__rating"),
			review_count=Count("books__reviews"), )
		.order_by("-avg_book_rating")
	)
	
	books_stats = (
		Book.objects.annotate(
			review_count=Count("reviews"),
			avg_rating=Avg("reviews__rating"), )
		.order_by("-review_count", "-avg_rating")
	)
	
	return render(
		request,
		"library/aggregates.html",
		{"authors": authors_stats, "books": books_stats}, )


def raw_sql_view(request: HttpRequest) -> HttpResponse:
	"""
	Select authors who have books with more than N reviews.
	Count the total number of books.
	"""
	try:
		threshold: int = int(request.GET.get("threshold", "10"))
	except ValueError:
		threshold = 10
	
	with connection.cursor() as cursor:
		cursor.execute("""
                SELECT a.id, a.name, COUNT(r.id) as review_count
                FROM library_author a
                JOIN library_book b ON b.author_id = a.id
                JOIN library_review r ON r.book_id = b.id
                GROUP BY a.id, a.name
                HAVING COUNT(r.id) > %s
                ORDER BY review_count DESC
            """, [threshold])
		authors = cursor.fetchall()
		
		cursor.execute("SELECT COUNT(*) FROM library_book")
		(total_books,) = cursor.fetchone()
		
		cursor.execute("""
                SELECT COUNT(*) FROM (
                    SELECT b.id
                    FROM library_book b
                    JOIN library_review r ON r.book_id = b.id
                    GROUP BY b.id
                    HAVING COUNT(r.id) >= %s
                ) AS filtered_books
            """, [threshold])
		(filtered_books_count,) = cursor.fetchone()
	
	authors_data = [
		{"id": row[0], "name": row[1], "review_count": row[2]}
		for row in authors
	]
	
	return render(request, "library/raw.html", {
		"authors": authors_data,
		"total_books": total_books,
		"filtered_books_count": filtered_books_count,
		"threshold": threshold,
	})


def import_form_view(request) -> Any:
	"""Form to start CSV import and view status."""
	if request.method == "POST":
		csv_path = request.POST.get("csv_path", "")
		email = request.POST.get("email", "")
		async_res = import_books_task.delay(csv_path, email)
		return HttpResponseRedirect(reverse("library:task_status",
		                                    kwargs={"task_id": async_res.id}))
	return render(request, "library/import_form.html")


def task_status_view(request, task_id: str) -> Any:
	"""Shows the status of a Celery task."""
	res = AsyncResult(task_id)
	return render(request,
	              "library/task_status.html",
	              {"task_id": task_id, "state": res.state,
	               "result": res.result})


def nosql_demo_view(request: HttpRequest) -> Any:
	"""Demonstration of writing/reading with MongoDB."""
	if request.method == "POST":
		random_id = random.randint(1, 1000)
		random_year = random.choice(range(1990, 2025))
		random_author = random.choice(
			["Anon", "TestUser", "RandomAuthor", "Guest"])
		random_title = f"NoSQL Book {random_id}"
		
		items = [{
			"title": random_title,
			"author": random_author,
			"year": random_year,
			"reviews": random.randint(0, 30),
		}]
		nosql_save_books(items)
	
	docs = nosql_read_books()
	
	return render(request,
	              "library/nosql_list.html",
	              {"nosql_docs": docs, })


def compare_sql_nosql_view(request: HttpRequest):
	"""Порівняння продуктивності SQL та NoSQL для підрахунку книг з відгуками ≥ threshold."""
	try:
		threshold = int(request.GET.get("threshold", "10"))
	except ValueError:
		threshold = 10
	
	t0 = time.perf_counter()
	with connection.cursor() as cursor:
		cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT b.id
                FROM library_book b
                JOIN library_review r ON r.book_id = b.id
                GROUP BY b.id
                HAVING COUNT(r.id) >= %s
            ) AS filtered_books
        """, [threshold])
		(sql_count,) = cursor.fetchone()
	sql_time = time.perf_counter() - t0

	if request.method == "POST":
		items = [{
			"title": f"NoSQL Book {random.randint(1, 1000)}",
			"author": random.choice(["Anon", "Tester", "RandomAuthor"]),
			"year": random.choice(range(1990, 2025)),
			"reviews": random.randint(0, 30),
		}]
		nosql_save_books(items)
	
	t1 = time.perf_counter()
	docs = nosql_read_books()
	nosql_count = sum(1 for d in docs if d.get("reviews", 0) >= threshold)
	nosql_time = time.perf_counter() - t1
	
	return render(request,
	              "library/compare_sql_nosql.html",
	              {"threshold": threshold,
	               "sql_count": sql_count, "sql_time": sql_time,
	               "nosql_count": nosql_count, "nosql_time": nosql_time, })
