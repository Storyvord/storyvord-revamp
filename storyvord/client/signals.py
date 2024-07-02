# client/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ClientProfile
from crew.models import CrewProfile
from accounts.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'client':
            ClientProfile.objects.create(user=instance)
        elif instance.user_type == 'crew':
            CrewProfile.objects.create(user=instance)
