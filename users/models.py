# techfest/users/models.py

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('eventhost', 'Event Host'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')

    # Add related_name to resolve clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set'
    )

    def is_eventhost(self):
        return self.user_type == 'eventhost'


class HostProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='host_profile')
    organization = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    biography = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='host_profiles', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Host Profile"