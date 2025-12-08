from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm


def register(request: HttpRequest) -> HttpResponse:
	"""
	Register a new user.
	- If POST → creates a user and logs them in.
	- If GET → shows the form.
	"""
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data["password"])
			user.save()
			login(request, user)
			return redirect("dashboard")
	else:
		form = RegistrationForm()
	
	return render(request, "register.html", {"form": form})
