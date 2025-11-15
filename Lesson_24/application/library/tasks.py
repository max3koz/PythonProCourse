from __future__ import annotations

import csv
from pathlib import Path

from celery import shared_task
from django.core.mail import send_mail
from django.db import transaction

from .models import Author, Book


@shared_task
def import_books_task(csv_path: str, user_email: str) -> str:
	"""
	Imports books from CSV (columns: author_name,title,year), saves to database.
	Sends email to user when finished.
	"""
	created_count: int = 0
	path = Path(csv_path)
	if not path.exists():
		return "CSV not found"
	
	with path.open("r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		with transaction.atomic():
			for row in reader:
				author, _ = Author.objects.get_or_create(name=row["author"])
				Book.objects.get_or_create(
					author=author,
					title=row["title"],
					defaults={
						"published_year": int(row.get("year") or 0) or None},
				)
				created_count += 1
	
	send_mail(
		subject="Імпорт завершено",
		message=f"Імпортовано {created_count} записів.",
		from_email="no-reply@example.com",
		recipient_list=[user_email],
		fail_silently=True,
	)
	return f"OK: {created_count}"
