from django.shortcuts import render
from .models import Software
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from DATABASE_APP.models import Software 

# Create your views here.

def software_list(request):
    """Display all software entries from the database"""
    software_entries = Software.objects.filter(is_active=True).order_by('subscription_name')
    context = {
        'software_entries': software_entries,
        'total_count': software_entries.count()
    }
    return render(request, 'software_list.html', context)

# Software List View with Sorting
@login_required
def software_list(request):
    sort = request.GET.get("sort", "subscription_name")

    valid_fields = [
        "subscription_name", "-subscription_name",
        "cost", "-cost",
        "term", "-term",
        "license_start", "-license_start",
        "license_end", "-license_end",
        "is_active", "-is_active",
    ]

    # Fallback if invalid
    if sort not in valid_fields:
        sort = "subscription_name"

    # Apply ordering
    software_qs = Software.objects.all().order_by(sort)

    context = {
        "software_entries": software_qs,
        "current_sort": sort,
        "total_count": software_qs.count(),
    }

    return render(request, "software_list.html", context)