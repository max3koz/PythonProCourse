from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import TaskForm


def create_task_view(request: HttpRequest) -> HttpResponse:
	"""
	Handles the creation of a new task via an HTML form.
	GET: Returns an empty form for creating a task.
	POST:
	- Valid data: creates a task, binds to request.user, saves and redirects to 'home'.
	- Invalid data: returns a form with errors.
	Args: request (HttpRequest): HTTP request from the user.
	Returns: HttpResponse: HTML page with the form or redirect.
	"""
	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.user = request.user
			task.save()
			return redirect('home')
	else:
		form = TaskForm()
	return render(request, 'create_task.html', {'form': form})
