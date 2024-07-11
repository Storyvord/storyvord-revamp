# # client/models.py
# from django.db import models
# from django.conf import settings

# class Profile(models.Model):


#     USER_TYPE_CHOICES = [  # Change: Added USER_TYPE_CHOICES
#         ('client', 'Client'),
#         ('crew', 'Crew'),
#         ('vendor', 'Vendor'),
#         ('internal', 'Internal Team'),
#     ]

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     address = models.CharField(max_length=255, blank=True, null=True)
#     # Add any additional fields you require for the profile

#     image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # Add this line for image upload

#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  # Change: Added user_type field


#     def __str__(self):
#         return self.user.email



# client/models.py
from django.db import models
from django.conf import settings

class ClientProfile(models.Model):
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
