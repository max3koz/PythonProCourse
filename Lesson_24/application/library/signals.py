from __future__ import annotations

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Book
from .views import CACHE_KEY_BOOK_LIST


@receiver([post_save, post_delete], sender=Book)
def invalidate_book_list_cache(sender, instance: Book, **kwargs) -> None:
	"""Invalidate cache when adding/changing/deleting a book."""
	cache.delete(CACHE_KEY_BOOK_LIST)
