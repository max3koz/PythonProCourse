from typing import Any

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import RegistrationForm


class RegistrationView(FormView):
	"""
	View for registering a new user.
	Displays the registration form and saves the user after successful validation.
	"""
	template_name = 'registration.html'
	form_class = RegistrationForm
	success_url = reverse_lazy('user-register')
	
	def form_valid(self, form: RegistrationForm) -> Any:
		"""
		Called when the form is valid.
		Saves the new user and calls standard processing.
		Args: form (RegistrationForm): The validated registration form.
		Returns: Any: The HTTP response after successful processing.
		"""
		form.save()
		return super().form_valid(form)


@login_required
def profile_view(request):
	"""
	Displays the user profile. Access is restricted to authorized users only.
	Args: request (HttpRequest): The current HTTP request.
	Returns: HttpResponse: Response with the profile template.
	"""
	return render(request,
	              "users/profile.html",
	              {"user": request.user})
