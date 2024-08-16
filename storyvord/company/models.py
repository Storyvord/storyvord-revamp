from django.db import models
from accounts.models import User
from client.models import ClientCompanyProfile

# Create your models here.
class AddressBook(models.Model):
    company = models.ForeignKey(ClientCompanyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    positions = models.TextField(null=True, blank=True)
    on_set = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    secondary_email = models.EmailField(null=True, blank=True)
    phone_office = models.CharField(max_length=20, null=True, blank=True)
    phone_work = models.CharField(max_length=20, null=True, blank=True)
    phone_home = models.CharField(max_length=20, null=True, blank=True)
    phone_private = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name