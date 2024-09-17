from django.urls import re_path
from . import consumers

websocket_ai_chat_urlpatterns = [
    re_path(r'ws/ai_assistant/$', consumers.AIChatConsumer.as_asgi()),
]
