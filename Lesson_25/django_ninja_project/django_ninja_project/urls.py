"""
URL configuration for django_ninja_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from apps.accounts.api import auth_router
from apps.blog.api import blog_router
from apps.library.api import library_router
from apps.monitoring.api import monitoring_router
from apps.movies.api import movies_router
from apps.shop.api import shop_router
from apps.tasks.api import router as tasks_router
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI(title="Multi-API Project", version="1.0")

# Tasks API
api.add_router("/tasks/", tasks_router)

# Auth API
api.add_router("/accounts/", auth_router)

# Shop API
api.add_router("/shop/", shop_router)

# Movies API
api.add_router("/movies", movies_router)

# Blog API
api.add_router("/blog", blog_router)

# Monitoring API
api.add_router("/monitoring", monitoring_router)

# Library API
api.add_router("/library", library_router)


def root_redirect(request):
	return redirect("/api/docs")


urlpatterns = [
	path("admin/", admin.site.urls),
	path("api/", api.urls),
	path("login/", auth_views.LoginView.as_view(), name="login"),
	path("logout/", auth_views.LogoutView.as_view(), name="logout"),
	path("", root_redirect),

]
