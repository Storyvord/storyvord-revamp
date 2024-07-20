# callsheets/models.py
from django.db import models
from django.utils import timezone
from project.models import Project

class CallSheet(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    calltime = models.TimeField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    contact_number = models.CharField(max_length=20)
    producer = models.CharField(max_length=255)
    producer_number = models.CharField(max_length=20)
    director = models.CharField(max_length=255)
    director_number = models.CharField(max_length=20)
    production_manager = models.CharField(max_length=255)
    production_manager_number = models.CharField(max_length=20)
    breakfast = models.TimeField()
    lunch = models.TimeField()
    sunrise = models.TimeField()  # Keep it as TimeField
    sunset = models.TimeField()
    weather = models.CharField(max_length=255, blank=True)
    nearest_hospital_address = models.CharField(max_length=255, blank=True)
    nearest_police_station = models.CharField(max_length=255, blank=True)
    nearest_fire_station = models.CharField(max_length=255, blank=True)
    additional_details = models.TextField(blank=True)
    project_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title