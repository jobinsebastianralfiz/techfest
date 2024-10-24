# techfest/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser