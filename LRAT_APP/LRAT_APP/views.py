from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import path

#Start of program
def rootPage(request):
    return redirect('login') #this is under urls.py in urlpatterns 

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'login.html')

@login_required #decantor ensuring only logged in users can access this function
def dashboard(request):
    context = {
        'user': request.user,
        'username': request.user.username,
    }
    return render(request, 'dashboard.html', context)

#log out user and send them back to login page
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def settings(request):
    return HttpResponse("Settings Page")

