

# Create your models here.
from django.db import models
from django.conf import settings

class CrewProfile(models.Model):
    # USER_TYPE_CHOICES = [  # Change: Added USER_TYPE_CHOICES
    #     ('client', 'Client'),
    #     ('crew', 'Crew'),
    #     ('vendor', 'Vendor'),
    #     ('internal', 'Internal Team'),
    # ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    # user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  # Change: Added user_type field

    def __str__(self):
        return f'{self.user.email}'
