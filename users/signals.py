from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, HostProfile

@receiver(post_save, sender=CustomUser)
def create_host_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == 'eventhost':
        HostProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_host_profile(sender, instance, **kwargs):
    if instance.user_type == 'eventhost':
        instance.host_profile.save()