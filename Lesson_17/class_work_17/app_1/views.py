from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'app_1/home.html')


def about(request: HttpRequest) -> HttpResponse:
    context = {
        'description': "It is class_work_17 project.",
    }
    return render(request, 'app_1/about.html', context)


def contact(request: HttpRequest) -> HttpResponse:
    context = {
        'email': 'info@example.com',
        'phone': '+380 99 999 9999',
        'address': 'New av., 123, City',
    }
    return render(request, 'app_1/contact.html', context)
