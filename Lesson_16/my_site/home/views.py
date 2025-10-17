from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_view(request: HttpRequest) -> HttpResponse:
	"""The view for main page"""
	return render(request, "home.html")


def about_view(request: HttpRequest) -> HttpResponse:
	"""The view of the page 'About us'"""
	return render(request, "about.html")


def contact_view(request: HttpRequest) -> HttpResponse:
	"""The view of the page 'Contacts'"""
	return render(request, "contact.html")


def post_view(request: HttpRequest, id: int) -> HttpResponse:
	"The view of the page of the post by <id>"
	return render(request, "post.html", {'id': id})


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
	"The view of the page with the users profile"
	return render(request, "profile.html", {'username': username})


def event_view(request: HttpRequest, year: str, month: str,
               day: str) -> HttpResponse:
	"The view of the page with news by date"
	return render(request, "event.html",
	              {'year': year, 'month': month, 'day': day})
