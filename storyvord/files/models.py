from django.db import models
from project.models import Project


# Create your models here.
class File(models.Model):
    file = models.FileField(upload_to='files/')
    allowed_users = models.ManyToManyField('accounts.User') 
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files', null=True, blank=True) 

    def __str__(self):
        return self.file.name

    def is_crew_user_allowed(self, user):
        return self.allowed_users.filter(id=user.id, user_type='crew').exists()