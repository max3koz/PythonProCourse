from typing import Optional

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import RegistrationForm, UserProfileForm, CustomPasswordChangeForm
from .models import UserProfile


def register_view(request: HttpRequest) -> HttpResponse:
	"""
	The function handles new user registration.
	If POST method: validates form, creates user, creates profile, logs in.
	If GET method: shows empty registration form.
	Redirects to profile page after successful registration.
	"""
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.save()
			UserProfile.objects.create(user=user)
			login(request, user)
			messages.success(request, 'Реєстрація успішна!')
			return redirect('profile')
	else:
		form = RegistrationForm()
	return render(request, 'register.html', {'form': form})


@login_required
def edit_profile_view(request: HttpRequest) -> HttpResponse:
	"""
	The function allows an authorized user to edit their profile.
	If POST method: saves changes to the form.
	If GET method: shows the form with the current data.
	After saving, redirects to the profile page.
	"""
	profile = request.user.userprofile
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			messages.success(request, 'Профіль оновлено!')
			return redirect('profile')
	else:
		form = UserProfileForm(instance=profile)
	return render(request, 'edit_profile.html', {'form': form})


@login_required
def change_password_view(request: HttpRequest) -> HttpResponse:
	"""
	The function allows an authorized user to change their password.
	If POST method: validates the form, changes the password, refreshes
	the session. If GET method: displays the password change form.
	After changing the password, redirects to the profile page.
	"""
	if request.method == 'POST':
		form = CustomPasswordChangeForm(user=request.user, data=request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Пароль змінено!')
			return redirect('profile')
	else:
		form = CustomPasswordChangeForm(user=request.user)
	return render(request, 'change_password.html', {'form': form})


@login_required
def profile_view(request: HttpRequest,
                 username: Optional[str] = None) -> HttpResponse:
	"""
	The function displays the current user's profile.
	If the profile does not exist, it will be created automatically.
	"""
	try:
		profile = request.user.userprofile
	except UserProfile.DoesNotExist:
		profile = UserProfile.objects.create(user=request.user)
	return render(request, 'profile.html', {'profile': profile})


@login_required
def delete_account_view(request: HttpRequest) -> HttpResponse:
	"""
	The function allows an authorized user to delete their account.
	If POST method: Logs out, deletes the user, redirects to the login page.
	If GET method: Shows the deletion confirmation page.
	"""
	if request.method == 'POST':
		user = request.user
		logout(request)
		user.delete()
		return redirect('login')
	return render(request, 'accounts/delete_account.html')
