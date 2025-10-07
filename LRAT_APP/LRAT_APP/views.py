from django.http import HttpResponse
from django.urls import path

def rootPage(request):
    return HttpResponse("Hello World!")
def settings(request):
    return HttpResponse("Settings Page")