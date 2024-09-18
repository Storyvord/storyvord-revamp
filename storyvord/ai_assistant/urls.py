# chat/urls.py
from django.urls import path
from .views.template_view import chat_page , wss_page  # Import template view
from .views.api_view import *    # Import API view

urlpatterns = [
    path('', chat_page, name='chat_page'),             # URL for rendering chat UI
    path('ai_chat/', wss_page, name='wss_page'),
    path('chat/', ChatAPIView.as_view(), name='chat_api'),  # URL for handling chat logic via API
]
