from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    user_message = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    embedding = models.JSONField(default=dict)  # Store the embedding as a JSON field

    def __str__(self):
        return f"Chat session {self.session_id} at {self.created_at}"
