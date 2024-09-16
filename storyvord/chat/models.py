from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10)  # 'user' or 'ai'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Context(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='contexts')
    key = models.CharField(max_length=255)
    value = models.JSONField()  # Can store complex objects like dicts
