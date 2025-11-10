from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import path
from DATABASE_APP.models import CustomUser, Subscription


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

@login_required
def dashboard(request):
    # read sort option from dropdown
    sort_by = request.GET.get('sort', 'date_subscribed')

    # define allowed sorting fields
    valid_fields = [
        'software__subscription_name', '-software__subscription_name',
        'date_subscribed', '-date_subscribed',
        'date_expired', '-date_expired',
        'total_cost', '-total_cost',
        'currently_used', '-currently_used'
    ]

    # verify the sort value
    if sort_by not in valid_fields:
        sort_by = 'date_subscribed'

    # apply sorting to the query
    user_subscriptions = Subscription.objects.filter(user=request.user).order_by(sort_by)

    # send current sort info to the template
    context = {
        'user': request.user,
        'subscriptions': user_subscriptions,
        'current_sort': sort_by.lstrip('-'),
        'direction': 'desc' if sort_by.startswith('-') else 'asc',
    }

    return render(request, 'dashboard.html', context)

#log out user and send them back to login page
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def settings(request):
    return HttpResponse("Settings Page")

