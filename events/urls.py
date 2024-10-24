# events/urls.py
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('', views.event_list, name='event_list'),
   
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('<int:pk>/', views.event_detail, name='detail'),
    path('<int:pk>/register/', views.register_event, name='register_event'),
    path('event/<int:event_id>/registrations/', views.event_registrations, name='event_registrations'),
     path('events/<int:event_id>/report/', views.generate_registration_report, name='registration_report'),

]