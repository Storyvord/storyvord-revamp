from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_assistant.models import ChatMessage
from ai_assistant.models import ChatSession
from ai_assistant.serializers import ChatMessageSerializer
from ai_assistant.serializers import ChatSessionSerializer

class UserChatSessionsAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        chat_sessions = ChatSession.objects.filter(user=request.user)
        serializer = ChatSessionSerializer(chat_sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatHistoryAPIView(APIView):
    
    def get(self, request, id, *args, **kwargs):
        chat_messages = ChatMessage.objects.filter(session_id=id)
        if not chat_messages.exists():
            return Response({"detail": "Chat session not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChatMessageSerializer(chat_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
