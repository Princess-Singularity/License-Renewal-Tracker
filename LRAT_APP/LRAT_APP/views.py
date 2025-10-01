from django.http import HttpResponse

def rootPage(request):
    return HttpResponse("Hello World!")
def settings(request):
    return HttpResponse("Settings Page")


