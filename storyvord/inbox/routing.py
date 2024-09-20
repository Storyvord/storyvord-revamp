from django.urls import path

from .consumers.chat_consumer import *

websocket_urlpatterns = [
    path('ws/chat/<int:user_id>/', ChatConsumer.as_asgi()),
    path('ws/groupchat/<int:group_id>/', InboxChatConsumer.as_asgi()),
]