from django.http import HttpResponse
from django.urls import path
from . import views

def rootPage(request):
    return HttpResponse("Hello World!")
def settings(request):
    return HttpResponse("Settings Page")


urlpatterns = [
    path('login/', views.login_view, name="login"),
]
