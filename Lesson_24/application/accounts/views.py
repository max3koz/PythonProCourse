from __future__ import annotations

from datetime import timedelta
from typing import Dict, Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .forms import LoginForm

COOKIE_NAME: str = "user_name"
COOKIE_AGE_SECONDS: int = 60 * 30


def login_view(request: HttpRequest) -> HttpResponse:
	"""Login: Saves name in cookies and age in session."""
	if request.method == "POST":
		form: LoginForm = LoginForm(request.POST)
		if form.is_valid():
			name: str = form.cleaned_data["name"]
			age: int = form.cleaned_data["age"]
			response: HttpResponse = redirect(reverse("accounts:greeting"))

			response.set_cookie(
				COOKIE_NAME, name, max_age=COOKIE_AGE_SECONDS, samesite="Lax")
			
			request.session["age"] = age
			request.session["last_activity"] = timezone.now().isoformat()
			return response
	else:
		form = LoginForm()
	return render(request, "accounts/login.html", {"form": form})


def greeting_view(request: HttpRequest) -> HttpResponse:
	"""
	Greeting: uses name from cookies and age from session.
	Checks cookies for validity and presence in session.
	"""
	name: Optional[str] = request.COOKIES.get(COOKIE_NAME)
	age: Optional[int] = request.session.get("age")
	
	if not name or age is None:
		return redirect(reverse("accounts:login"))
	
	context: Dict[str, object] = {"name": name, "age": age}
	return render(request, "accounts/greeting.html", context)


def logout_view(request: HttpRequest) -> HttpResponse:
	"""Deletes cookies and session data ('Logout' button)."""
	response: HttpResponse = redirect(reverse("accounts:login"))
	response.delete_cookie(COOKIE_NAME)
	request.session.flush()
	return response
