from rest_framework import serializers
from .models import ChatMessage, ChatSession

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id','user_message', 'ai_response']

class ChatSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession 
        fields = '__all__'
