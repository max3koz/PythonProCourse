from __future__ import annotations

from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from .views import COOKIE_NAME, COOKIE_AGE_SECONDS


class AutoExtendCookieMiddleware:
	"""
	If the user is active (has a session last_activity), extends the cookie
	lifetime. Checks for cookie and session; if cookie is absent at the time
	of activity, does nothing.
	"""
	
	def __init__(self,
	             get_response: Callable[[HttpRequest], HttpResponse]) -> None:
		self.get_response = get_response
	
	def __call__(self, request: HttpRequest) -> HttpResponse:
		response: HttpResponse = self.get_response(request)
		
		name_cookie = request.COOKIES.get(COOKIE_NAME)
		last_activity = request.session.get("last_activity")
		
		if name_cookie and last_activity:
			request.session["last_activity"] = timezone.now().isoformat()
			response.set_cookie(
				COOKIE_NAME,
				name_cookie,
				max_age=COOKIE_AGE_SECONDS,
				samesite="Lax",
			)
		return response
