from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from storyvord_calendar.models import Event

# Create your models here.
class CrewProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    languages = models.CharField(max_length=256, null=True, blank=True)
    job_title = models.CharField(max_length=256, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    experience = models.CharField(max_length=256, null=True, blank=True)
    skills = models.CharField(max_length=256, null=True, blank=True)
    technicalProficiencies = models.CharField(max_length=256, null=True, blank=True)
    specializations = models.CharField(max_length=256, null=True, blank=True)
    drive = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.email
    
class CrewCredits(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    year = models.CharField(max_length=256, null=True, blank=True)
    role = models.CharField(max_length=256, null=True, blank=True)
    production = models.CharField(max_length=256, null=True, blank=True)
    client = models.CharField(max_length=256, null=True, blank=True)
    type_of_content = models.CharField(max_length=256, null=True, blank=True)
    tags = models.CharField(max_length=256, null=True, blank=True)
    
    def __str__(self):
        return self.crew.user.email
    
class CrewEducation(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    academicQualifications = models.CharField(max_length=256, null=True, blank=True)
    professionalCourses = models.CharField(max_length=256, null=True, blank=True)
    workshopsAttended = models.CharField(max_length=256, null=True, blank=True)
    
    def __str__(self):
        return self.crew.user.email
    
class CrewRate(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    standardRate = models.CharField(max_length=256, null=True, blank=True)
    negotiation = models.BooleanField(default=False)
    
    def __str__(self):
        return self.crew.user.email
    
class EndorsementfromPeers(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    givenBy = models.CharField(max_length=256, null=True, blank=True)
    
    def __str__(self):
        return self.crew.user.email
    
class SocialLinks(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    link = models.CharField(max_length=256, null=True, blank=True)
    
    def __str__(self):
        return self.crew.user.email


class CrewCalendar(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crew_calendar')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class CrewEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='crew_events')
    crew_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crew_events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def clean(self):
        overlapping_events = CrewEvent.objects.filter(
            crew_member=self.crew_member,
            start__lt=self.end,
            end__gt=self.start
        ).exclude(pk=self.pk)
        
        if overlapping_events.exists():
            raise ValidationError("This crew member has another event at the same time.")