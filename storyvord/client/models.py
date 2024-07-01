# client/models.py
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    # Add any additional fields you require for the profile

    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Add this line for image upload

    def __str__(self):
        return self.user.email
