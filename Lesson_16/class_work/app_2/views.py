from django.http import HttpResponse


def index(request):
	return HttpResponse("app_2 started")
