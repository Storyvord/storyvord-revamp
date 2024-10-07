from django.db import models

from accounts.models import User
from project.models import Project
from django.core.exceptions import ValidationError

# Create your models here.
class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    completion_requested = models.BooleanField(default=False)
    requester = models.ForeignKey(User, related_name='requested_tasks', null=True, blank=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.assigned_to.user_type != '2':
            raise ValidationError(f"The user {self.assigned_to} is not a crew member and cannot be assigned to a task.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title