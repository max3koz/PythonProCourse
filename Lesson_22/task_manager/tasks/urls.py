from django.urls import path

from .views import create_task_view

urlpatterns = [
	path('create/', create_task_view, name='create-task'),
]
