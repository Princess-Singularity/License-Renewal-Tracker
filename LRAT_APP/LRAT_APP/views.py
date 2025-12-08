from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import path
from DATABASE_APP.models import CustomUser, Software, Subscription
from django.db import models

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
    # fetch user subscriptions
    subscriptions = Subscription.objects.filter(user=request.user)
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
    sort = request.GET.get("sort", "software__subscription_name")
    subscriptions = (
        Subscription.objects
        .filter(user=request.user)
        .order_by(sort)
    )

    total_subscriptions = subscriptions.count()
    total_active = subscriptions.filter(currently_used=True).count()
    total_expired = subscriptions.filter(currently_used=False).count()
    raw_total_cost = subscriptions.filter(currently_used=True).aggregate(sum_cost=models.Sum("total_cost"))["sum_cost"] or 0
    total_cost = f"{raw_total_cost:,.2f}"

    context = {
        'subscriptions': subscriptions,
        'current_sort': sort,
        'total_subscriptions': total_subscriptions,
        'total_active': total_active,
        'total_expired': total_expired,
        'total_cost': total_cost,
    }

    # render the dashboard template
    return render(request, "dashboard.html", context)

@login_required
def license_info(request, software_id):
    from DATABASE_APP.models import Software   
    software = Software.objects.get(software_id=software_id)

    context = {
        'software': software
    }
    return render(request, 'license_info.html', context)

#log out user and send them back to login page
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def settings(request):
    return HttpResponse("Settings Page")