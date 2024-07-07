from django.conf import settings
from django.db import models

from project.models import Project

# Create your models here.
class Calendar(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='calendar')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='events', blank=True)

    def __str__(self):
        return self.title