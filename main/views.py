# main/views.py

from django.shortcuts import render
from events.models import Event  # Import Event model if you want to display events on the home page

def home(request):
    events = Event.objects.all()[:5]  # Get the first 5 events
    return render(request, 'users/home.html', {'events': events})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')