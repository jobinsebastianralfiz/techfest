# events/admin.py

from django.contrib import admin
from django.apps import apps

# Get the app config
app = apps.get_app_config('events')

# Register all models
for model_name, model in app.models.items():
    admin.site.register(model)