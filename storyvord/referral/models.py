import uuid
from django.db import models

from client.models import ClientProfile
from project.models import Project

# Create your models here.
class ProjectInvitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    crew_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    referral_code = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Invitation to {self.crew_email} for project {self.project.name}'
    
class ClientInvitation(models.Model):
    client_profile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    employee_email = models.EmailField()
    referral_code = models.UUIDField(default=uuid.uuid4, unique=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Invitation to {self.employee_email} for {self.client_profile.formalName or self.client_profile.user.email}'