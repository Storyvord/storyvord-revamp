# chat/urls.py
from django.urls import path
from .views.template_view import chat_page , wss_page  # Import template view
from .views.api_view import *    # Import API view
from .views.api_view import UserChatSessionsAPIView, ChatHistoryAPIView

urlpatterns = [
    # URL for rendering chat UI
    path('', chat_page, name='chat_page'), 
    
    # URL for rendering WebSocket page
    path('ai_chat/', wss_page, name='wss_page'),
    
    # URL for retrieving chat sessions for the authenticated user
    path('ai_chat/sessions/', UserChatSessionsAPIView.as_view(), name='user_chat_sessions'),
    
    # URL for retrieving chat history for a specific session ID
    path('ai_chat/history/<str:id>/', ChatHistoryAPIView.as_view(), name='chat_history'),

]