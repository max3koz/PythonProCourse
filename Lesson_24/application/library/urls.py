from __future__ import annotations

from django.urls import path

from .views import (book_list_view, books_unoptimized_view,
                    books_optimized_view,
                    aggregates_view, import_form_view, task_status_view,
                    raw_sql_view, nosql_demo_view, compare_sql_nosql_view)

app_name: str = "library"

urlpatterns = [
	path("books/", book_list_view, name="book_list"),
	path("perf/unoptimized/", books_unoptimized_view, name="perf_unoptimized"),
	path("perf/optimized/", books_optimized_view, name="perf_optimized"),
	path("perf/aggregates/", aggregates_view, name="aggregates"),
	path("import/", import_form_view, name="import_form"),
	path("task/<str:task_id>/", task_status_view, name="task_status"),
	path("raw/", raw_sql_view, name="raw_sql"),
	path("nosql/", nosql_demo_view, name="nosql-demo"),
	path("compare/", compare_sql_nosql_view, name="compare"),
]
