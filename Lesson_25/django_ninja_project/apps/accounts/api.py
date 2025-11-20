from django.contrib.auth import authenticate, login as django_login
from ninja import Router

from .schemas import LoginIn, LoginOut

auth_router = Router(tags=["accounts"])


@auth_router.post("/login", response=LoginOut)
def login_view(request, payload: LoginIn):
	"""Authenticate user with username and password. Uses Django session login."""
	user = authenticate(username=payload.username, password=payload.password)
	if user is None:
		return {"success": False, "token": None,
		        "message": "Invalid credentials"}
	
	django_login(request, user)
	return {"success": True, "token": "session", "message": "Login successful"}
