from django.db import models

from accounts.models import User
from project.models import Project

# Create your models here.
class Announcement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipients = models.ManyToManyField(User, related_name='announcements', null=True, blank=True)

    def __str__(self):
        return self.title