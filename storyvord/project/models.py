import uuid
from django.db import models

from accounts.models import User


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

class Project(models.Model):
    
    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    brief = models.TextField()
    additional_details = models.TextField()
    budget_currency = models.CharField(max_length=256, default='$')
    budget_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    content_type = models.CharField(max_length=256)
    selected_crew = models.TextField()
    equipment = models.TextField()
    uploaded_document = models.FileField(blank=True, null=True)
    location_details = models.ManyToManyField(LocationDetail, related_name='projects')
    status = models.CharField(
        max_length=30, choices=StatusChoices.choices, default=StatusChoices.PLANNING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['project_id']
    
    def __str__(self):
        return self.name