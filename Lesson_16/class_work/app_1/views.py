from django.http import HttpResponse

def index (request):
    return HttpResponse("app_1 started")

def about_page(request):
	return HttpResponse("about page")
