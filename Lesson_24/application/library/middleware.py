from typing import Callable

from django.core.cache import cache
from django.http import HttpRequest, HttpResponse

PAGE_CACHE_TIMEOUT: int = 60 * 2


class AnonymousPageCacheMiddleware:
	"""Caches the HTML content of the book list page for anonymous users."""
	
	def __init__(self,
	             get_response: Callable[[HttpRequest], HttpResponse]) -> None:
		self.get_response = get_response
	
	def __call__(self, request: HttpRequest) -> HttpResponse:
		if request.user.is_authenticated is False and request.path.startswith(
				"/library/books/"):
			key = f"pagecache:{request.get_full_path()}"
			cached = cache.get(key)
			if cached:
				return cached
			response: HttpResponse = self.get_response(request)
			cache.set(key, response, PAGE_CACHE_TIMEOUT)
			return response
		return self.get_response(request)
