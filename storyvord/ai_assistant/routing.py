from django.urls import path
from . import consumers

websocket_ai_chat_urlpatterns = [
    path('ws/ai_assistant/', consumers.AIChatConsumer.as_asgi()),
]