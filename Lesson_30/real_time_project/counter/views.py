from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
	"""
	HTML page with a WebSocket connection and displaying a counter
	of online users.
	"""
	return render(request, "realtime_dashboard.html")
