from django.db import models
from accounts.models import User
from client.models import ClientCompanyProfile
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class AddressBook(models.Model):
    company = models.ForeignKey(ClientCompanyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    pronouns = models.CharField(max_length=10, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    positions = models.TextField(null=True, blank=True)
    on_set = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    secondary_email = models.EmailField(null=True, blank=True)
    phone_office = models.CharField(max_length=20, null=True, blank=True)
    phone_work = models.CharField(max_length=20, null=True, blank=True)
    phone_home = models.CharField(max_length=20, null=True, blank=True)
    phone_private = models.CharField(max_length=20, null=True, blank=True)
    fax = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact = models.CharField(max_length=256, null=True, blank=True)
    shirt_size = models.CharField(max_length=10, null=True, blank=True)
    shoe_size = models.CharField(max_length=10, null=True, blank=True)
    pants_size = models.CharField(max_length=10, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class AddressBookSkills(models.Model):
    address_book = models.ForeignKey(AddressBook, on_delete=models.CASCADE)
    certification = models.CharField(max_length=256)
    education_and_training = models.TextField()
    driving_license = models.CharField(max_length=50)
    driving_license_classes = models.CharField(max_length=256)
    
    def __str__(self):
        return self.certification

class AddressBookCateringInformation(models.Model):
    address_book = models.ForeignKey(AddressBook, on_delete=models.CASCADE)
    specific = models.TextField()
    allergies = models.TextField()
    note = models.TextField()
    food_preferences = models.TextField()
    
    def __str__(self):
        return self.allergies

class AddressBookHomeAddress(models.Model):
    address_book = models.ForeignKey(AddressBook, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    
    def __str__(self):
        return self.address

class AddressBookFiles(models.Model):
    address_book = models.ForeignKey(AddressBook, on_delete=models.CASCADE)
    file = models.FileField(upload_to='address_book_files/')
    
    def __str__(self):
        return self.file.name

        
class ClientCompanyTask(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='company_tasks', on_delete=models.CASCADE)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    completion_requested = models.BooleanField(default=False)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='requested_company_tasks', null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_company_tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)