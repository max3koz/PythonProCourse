from django.http import HttpResponse
from .models import Profile
from django.shortcuts import render, redirect
from .forms import ProfileForm


def hello_view(request):
    return render(request, "hello.html")

def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm()

    profiles = Profile.objects.all()
    return render(request, "profile.html", {"form": form, "profiles": profiles})