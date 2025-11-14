from django.urls import path

from .views import RegistrationView, profile_view

urlpatterns = [
	path('register/', RegistrationView.as_view(), name='user-register'),
	path("profile/", profile_view, name="user-profile"),
]
