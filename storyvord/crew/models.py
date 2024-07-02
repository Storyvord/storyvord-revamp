from django.db import models
from django.conf import settings

# Create your models here.
class CrewProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    languages = models.CharField(max_length=256, null=True, blank=True)
    job_title = models.CharField(max_length=256, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    experience = models.CharField(max_length=256, null=True, blank=True)
    skills = models.CharField(max_length=256, null=True, blank=True)
    technicalProficiencies = models.CharField(max_length=256, null=True, blank=True)
    specializations = models.CharField(max_length=256, null=True, blank=True)
    drive = models.BooleanField(default=False)
    
class CrewCredits(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    year = models.CharField(max_length=256, null=True, blank=True)
    role = models.CharField(max_length=256, null=True, blank=True)
    production = models.CharField(max_length=256, null=True, blank=True)
    client = models.CharField(max_length=256, null=True, blank=True)
    type_of_content = models.CharField(max_length=256, null=True, blank=True)
    tags = models.CharField(max_length=256, null=True, blank=True)
    
class CrewEducation(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    academicQualifications = models.CharField(max_length=256, null=True, blank=True)
    professionalCourses = models.CharField(max_length=256, null=True, blank=True)
    workshopsAttended = models.CharField(max_length=256, null=True, blank=True)
    
class CrewRate(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    standardRate = models.CharField(max_length=256, null=True, blank=True)
    negotiation = models.BooleanField(default=False)
    
class EndorsementfromPeers(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    givenBy = models.CharField(max_length=256, null=True, blank=True)
    
class SocialLinks(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    link = models.CharField(max_length=256, null=True, blank=True)
