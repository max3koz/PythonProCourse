from __future__ import annotations

from django.urls import path

from .views import login_view, greeting_view, logout_view

app_name: str = "accounts"

urlpatterns = [
	path("login/", login_view, name="login"),
	path("greeting/", greeting_view, name="greeting"),
	path("logout/", logout_view, name="logout"),
]
