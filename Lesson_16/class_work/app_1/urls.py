from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	re_path(r'^about/$', views.about_page, name='about')
]
