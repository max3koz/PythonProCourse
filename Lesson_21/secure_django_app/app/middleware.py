import logging
from typing import Callable

from django.http import (HttpResponseNotFound, HttpResponseServerError,
                         HttpRequest, HttpResponse)

logger = logging.getLogger(__name__)


class ProtectedPageLoggerMiddleware:
	"""Logging access to protected pages."""
	
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		if request.path.startswith('/secure/'):
			logger.info(f"Access attempt: {request.user} to {request.path}")
		return self.get_response(request)


class ErrorHandlingMiddleware:
	"""Handling 404 and 500 errors."""
	
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		try:
			response = self.get_response(request)
			if response.status_code == 404:
				return HttpResponseNotFound("Сторінку не знайдено")
			return response
		except Exception:
			logger.error("Помилка сервера", exc_info=True)
			return HttpResponseServerError("Внутрішня помилка сервера")


class CookieSecurityMiddleware:
	"""
	Middleware for setting a secure cookie.
	Adds a cookie with the following parameters:
	- HttpOnly: prevents access via JavaScript
	- Secure: transmitted only via HTTPS
	- SameSite=Lax: protects against CSRF
	"""
	
	def __init__(self,
	             get_response: Callable[[HttpRequest], HttpResponse]) -> None:
		self.get_response = get_response
	
	def __call__(self, request: HttpRequest) -> HttpResponse:
		response = self.get_response(request)
		response.set_cookie(
			key='my_cookie',
			value='value',
			httponly=True,
			secure=True,
			samesite='Lax'
		)
		return response


class CSPMiddleware:
	"""
	Middleware for adding the Content-Security-Policy (CSP) header.
	CSP restricts content sources, which helps prevent XSS attacks.
	The header is only added to HTML responses.
	"""
	
	def __init__(self,
	             get_response: Callable[[HttpRequest], HttpResponse]) -> None:
		self.get_response = get_response
	
	def __call__(self, request: HttpRequest) -> HttpResponse:
		response = self.get_response(request)
		content_type = response.get('Content-Type', '')
		if content_type.startswith('text/html'):
			response.headers['Content-Security-Policy'] = (
				"default-src 'self'; "
				"script-src 'self'; "
				"style-src 'self'; "
				"img-src 'self'; "
				"font-src 'self'; "
				"frame-src 'none'; "
				"frame-ancestors 'none'; "
				"form-action 'self'; "
				"object-src 'none'; "
				"base-uri 'self';"
			)
		return response


class CustomServerHeaderMiddleware:
	"""
	Middleware to replace the 'Server' header in HTTP responses.
	This hides the version of the web server, which reduces the risk of attacks
	on known vulnerabilities.
	"""
	
	def __init__(self,
	             get_response: Callable[[HttpRequest], HttpResponse]) -> None:
		self.get_response = get_response
	
	def __call__(self, request: HttpRequest) -> HttpResponse:
		response = self.get_response(request)
		response.headers['Server'] = 'SecureApp'
		return response
