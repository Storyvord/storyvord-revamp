from django.core.exceptions import ValidationError
from django.db import models
from accounts.models import User,PersonalInfo
from django.conf import settings
from storyvord_calendar.models import Event


# Create your models here.
class CrewProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE , related_name='crew_profile', null=True, blank=True)
    experience = models.CharField(max_length=256, null=True, blank=True)
    skills = models.CharField(max_length=256, null=True, blank=True)
    standardRate = models.CharField(max_length=256, null=True, blank=True)
    technicalProficiencies = models.CharField(max_length=256, null=True, blank=True)
    specializations = models.CharField(max_length=256, null=True, blank=True)
    drive = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    
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

    
class CrewPortfolio(models.Model):
    crew = models.ForeignKey(CrewProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    link = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='portfolio/thumbnail/', blank=True, null=True)
    contentTag = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    providedService = models.TextField(null=True, blank=True)
    verification_type = models.CharField(max_length=50, choices=[
        ('client_reference', 'Client Reference'),
        ('imbd_link', 'IMDB Link'),
        ('work_sample', 'Work Sample'),
        ('email_agreement', 'Email Agreement'),
    ], null=True, blank=True)
    verified = models.BooleanField(default=False)
    # Link to the verification model based on the verification_type
    client_reference_verification = models.OneToOneField('ClientReferenceVerification', null=True, blank=True, on_delete=models.SET_NULL)
    imbd_link_verification = models.OneToOneField('ImbdLinkVerification', null=True, blank=True, on_delete=models.SET_NULL)
    work_sample_verification = models.OneToOneField('WorkSampleVerification', null=True, blank=True, on_delete=models.SET_NULL)
    email_agreement_verification = models.OneToOneField('EmailAgreement', null=True, blank=True, on_delete=models.SET_NULL)

class ClientReferenceVerification(models.Model):
    crew_portfolio = models.OneToOneField(CrewPortfolio, on_delete=models.CASCADE)
    fname = models.CharField(max_length=256)
    lname = models.CharField(max_length=256)
    email = models.EmailField()
    company_name = models.CharField(max_length=256)

class ImbdLinkVerification(models.Model):
    crew_portfolio = models.OneToOneField(CrewPortfolio, on_delete=models.CASCADE)
    link = models.URLField()

class WorkSampleVerification(models.Model):
    crew_portfolio = models.OneToOneField(CrewPortfolio, on_delete=models.CASCADE)
    minutes = models.PositiveIntegerField()
    seconds = models.PositiveIntegerField()

class EmailAgreement(models.Model):
    crew_portfolio = models.OneToOneField(CrewPortfolio, on_delete=models.CASCADE)
    document = models.FileField(upload_to='portfolio/document/', blank=True, null=True)


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