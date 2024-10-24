# techfest/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from events.models import*

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Print the user's details for debugging
            print(f"User created: {user.username}, Password valid: {user.check_password(form.cleaned_data['password1'])}")
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('users:dashboard')
        else:
            # Print form errors for debugging
            print(f"Form errors: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})




# techfest/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from events.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('users:dashboard')
            else:
                # Debugging information
                try:
                    user = User.objects.get(username=username)
                    messages.error(request, "User found, but authentication failed. Check password.")
                except User.DoesNotExist:
                    messages.error(request, f"No user found with username {username}")
        else:
            messages.error(request, "Invalid form submission. Please check your input.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# ... rest of your views ...
from events.models import Event

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('main:home')  # Assuming you have a 'home' URL pattern defined

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from events.models import Event, Registration
from datetime import datetime, timedelta
@login_required
def dashboard(request):
    if request.user.is_eventhost():
        # Fetch events created by this host
        events = Event.objects.filter(host=request.user).order_by('-date')
        event_registrations = {event.id: Registration.objects.filter(event=event, user=request.user).select_related('event') for event in events}
        context = {
            'events': events,
            'event_registrations': event_registrations,
        }
        return render(request, 'users/eventhost_dashboard.html', context)
    else:
        # Fetch events the user has registered for
        current_date = datetime.now().date()
    upcoming_date = current_date + timedelta(days=5)
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    registered_events = [reg.event for reg in registrations]
    upcoming_events = Event.objects.filter(date__gt=upcoming_date).order_by('date')

    context = {
        'registrations': registrations,
        'registered_events': registered_events,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'users/user_dashboard.html', context)

from django.shortcuts import render, redirect, get_object_or_404

from .models import HostProfile
@login_required
def update_host_profile(request):
    host_profile = get_object_or_404(HostProfile, user=request.user)

    if request.method == 'POST':
        organization = request.POST.get('organization')
        designation = request.POST.get('designation')
        phone_number = request.POST.get('phone_number')
        biography = request.POST.get('biography')
        profile_picture = request.FILES.get('profile_picture')

        host_profile.organization = organization
        host_profile.designation = designation
        host_profile.phone_number = phone_number
        host_profile.biography = biography
        if profile_picture:
            host_profile.profile_picture = profile_picture
        host_profile.save()

        return redirect('users:host_dashboard')

    return render(request, 'users/update_host_profile.html', {'host_profile': host_profile})