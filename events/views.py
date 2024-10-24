from django.shortcuts import render
from django.contrib import messages
# Create your views here.
# events/views.py
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Event
from .forms import *

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_registration = None
    is_registered = False

    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(event=event, user=request.user).first()
        is_registered = user_registration is not None

    context = {
        'event': event,
        'is_registered': is_registered,
        'user_registration': user_registration,
        'total_registrations': event.registrations.count(),
    }
    return render(request, 'events/event_detail.html', context)


@login_required
def event_list(request):
    events = Event.objects.filter(host=request.user)
    return render(request, 'events/eventlist.html', {'events': events})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.host = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('users:dashboard')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.user != event.host:
        messages.error(request, "You don't have permission to edit this event.")
        return redirect('events:detail', pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.title}" has been updated successfully.')
            return redirect(reverse('users:dashboard'))
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_edit.html', {'form': form, 'event': event})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.host:
        messages.error(request, "You don't have permission to delete this event.")
        return redirect('events:detail', pk=pk)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, f'Event "{event.title}" has been deleted.')
        return redirect(reverse('users:dashboard'))
    
    return render(request, 'events/event_confirm_delete.html', {'event': event})


# events/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .models import Event, Registration
from .forms import RegistrationForm

@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if Registration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, "You are already registered for this event.")
        return redirect(reverse('events:detail', kwargs={'pk': pk}))

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()
            messages.success(request, "You have successfully registered for this event.")
            return redirect(reverse('events:detail', kwargs={'pk': pk}))
    else:
        form = RegistrationForm()

    return render(request, 'events/register_event.html', {'form': form, 'event': event})



@login_required
def event_registrations(request, event_id):
    event = get_object_or_404(Event, id=event_id, host=request.user)
    registrations = Registration.objects.filter(event=event).select_related('user')
    
    context = {
        'event': event,
        'registrations': registrations,
    }
    return render(request, 'events/event_registrations.html', context)



from django.http import HttpResponse
import csv
import tempfile
from .models import Registration
from django.http import FileResponse
def generate_registration_report(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = Registration.objects.filter(event=event)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(['Username', 'College', 'Department', 'Semester', 'Course', 'Registration Date'])

        for registration in registrations:
            writer.writerow([
                registration.user.username,
                registration.college,
                registration.get_department_display(),
                registration.get_semester_display(),
                registration.get_course_display(),
                registration.registration_date.strftime('%B %d, %Y - %I:%M %p')
            ])

        temp_file.flush()
        return FileResponse(open(temp_file.name, 'rb'), as_attachment=True, filename=f'registrations_{event.title}.csv')