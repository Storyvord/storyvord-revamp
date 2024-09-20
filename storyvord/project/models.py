import uuid
from django.conf import settings
from django.db import models

from accounts.models import User
from .storage_utils import upload_to_project_files_bucket  # Highlighted import
from google.cloud import storage
import os
from django.core.files.storage import default_storage

class StatusChoices(models.TextChoices):
    PLANNING = 'PLANNING', 'Planning'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    PAUSED = 'PAUSED', 'Paused'
    DEVELOPMENT = 'DEVELOPMENT', 'Development'
    PRE_PRODUCTION = 'PRE_PRODUCTION', 'Pre-Production'
    POST_PRODUCTION = 'POST_PRODUCTION', 'Post-Production'
    RELEASED = 'RELEASED', 'Released'
    
# Create your models here.
class LocationDetail(models.Model):
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    mode_of_shooting = models.CharField(max_length=255)
    permits = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.location} ({self.start_date} - {self.end_date})"
    
class SelectCrew(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    
    def __srt__(self):
        return self.title

class SelectEquipment(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    
    def __srt__(self):
        return self.title

class Document(models.Model):
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    
    def __str__(self):
        return self.document.name
    

class Project(models.Model):
    
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    brief = models.TextField()
    additional_details = models.TextField()
    budget_currency = models.CharField(max_length=256, default='$')
    budget_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    content_type = models.CharField(max_length=256)
    selected_crew = models.ManyToManyField(SelectCrew, related_name='SelectCrew')
    equipment = models.ManyToManyField(SelectEquipment, related_name='SelectEquipment')
    documents = models.ManyToManyField(Document, related_name='uploaded_documents')
    location_details = models.ManyToManyField(LocationDetail, related_name='projects')
    status = models.CharField(
        max_length=30, choices=StatusChoices.choices, default=StatusChoices.PLANNING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    crew_profiles = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', blank=True)
    
    class Meta:
        ordering = ['project_id']
    
    def __str__(self):
        return self.name
    
    # We need to setup the gcp buckets
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.uploaded_document:
    #         self.upload_document_to_bucket()

    # def upload_document_to_bucket(self):
    #     bucket_name = f"{self.name}-{self.project_id}"
    #     client = storage.Client()
    #     bucket = client.bucket(bucket_name)

    #     if not bucket.exists():
    #         bucket.create()

    #     blob = bucket.blob(self.uploaded_document.name)
    #     document_file = self.uploaded_document.file

    #     blob.upload_from_file(document_file, rewind=True)

class OnboardRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'crew'})
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)