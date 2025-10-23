from django.shortcuts import render
from .models import Software

# Create your views here.

def software_list(request):
    """Display all software entries from the database"""
    software_entries = Software.objects.filter(is_active=True).order_by('subscription_name')
    context = {
        'software_entries': software_entries,
        'total_count': software_entries.count()
    }
    return render(request, 'software_list.html', context)
