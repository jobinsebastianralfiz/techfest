# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.apps import apps
from .models import CustomUser  # Import your CustomUser model

# Register CustomUser with UserAdmin
admin.site.register(CustomUser, UserAdmin)

# Get the app config
app = apps.get_app_config('users')

# Register all other models
for model_name, model in app.models.items():
    if model != CustomUser:  # Skip CustomUser as it's already registered
        admin.site.register(model)