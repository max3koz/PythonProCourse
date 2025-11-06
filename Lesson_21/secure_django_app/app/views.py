from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .forms import RegistrationForm, LoginForm


def logout_view(request) -> redirect:
	"""User logout."""
	logout(request)
	return redirect('login')


def register_view(request):
	"""User registration processing."""
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
	else:
		form = RegistrationForm()
	return render(request, 'app/register.html', {'form': form})


def login_view(request):
	"""User authorization processing."""
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			request.session['user'] = username
			return redirect('home')
	else:
		form = LoginForm()
	return render(request, 'app/login.html', {'form': form})


def home_view(request):
	"""Home page after logging in."""
	username = request.session.get('user')
	return render(request, 'app/home.html', {'username': username})
