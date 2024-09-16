from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .services import generate_response

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ViewSet):
    def create(self, request, conversation_id):
        conversation = Conversation.objects.get(id=conversation_id)
        user_message = request.data.get('content')
        
        # Save user message
        Message.objects.create(conversation=conversation, sender='user', content=user_message)
        
        # Generate and save AI response
        ai_response = generate_response(conversation.id, user_message)
        
        return Response({'response': ai_response}, status=status.HTTP_201_CREATED)
