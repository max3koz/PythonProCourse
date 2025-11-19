from django.contrib.auth import authenticate, login as django_login
from ninja import Router, Schema

auth_router = Router(tags=["accounts"])


class LoginIn(Schema):
	username: str
	password: str


class LoginOut(Schema):
	success: bool
	token: str | None = None
	message: str | None = None


@auth_router.post("/login", response=LoginOut)
def login_view(request, payload: LoginIn):
	"""Authenticate user with username and password. Uses Django session login."""
	user = authenticate(username=payload.username, password=payload.password)
	if user is None:
		return {"success": False, "token": None,
		        "message": "Invalid credentials"}
	
	django_login(request, user)
	return {"success": True, "token": "session", "message": "Login successful"}
