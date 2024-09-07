from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import DialogsModel, MessageModel
from .serializers import DialogSerializer, MessageSerializer
from accounts.models import User

class DialogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dialogs = DialogsModel.get_dialogs_for_user(request.user)
        serialized_data = [{'user1_id': dialog[0], 'user2_id': dialog[1]} for dialog in dialogs]
        return Response(serialized_data, status=status.HTTP_200_OK)

class DialogMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        dialog = DialogsModel.dialog_exists(request.user, other_user)
        if not dialog:
            return Response({"detail": "Dialog not found"}, status=status.HTTP_404_NOT_FOUND)

        messages = MessageModel.objects.filter(
            Q(sender=request.user, recipient=other_user) |
            Q(sender=other_user, recipient=request.user)
        ).order_by('created')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        recipient = get_object_or_404(User, id=user_id)
        text = request.data.get('text', '')

        if not text:
            return Response({"detail": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        message = MessageModel.objects.create(sender=request.user, recipient=recipient, text=text)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, message_id):
        message = get_object_or_404(MessageModel, id=message_id, recipient=request.user)

        if message.read:
            return Response({"detail": "Message already marked as read"}, status=status.HTTP_400_BAD_REQUEST)

        message.read = True
        message.save()
        return Response({"detail": "Message marked as read"}, status=status.HTTP_200_OK)
