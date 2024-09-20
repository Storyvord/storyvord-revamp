from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import DialogsModel, MessageModel
from .serializers import DialogSerializer, GroupMessageSerializer, MessageSerializer
from accounts.models import User
from .models import InboxGroup, InboxMessage
from .serializers import GroupSerializer, MessageSerializer

class DialogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dialogs = DialogsModel.get_dialogs_for_user(request.user)

        # Serialize the dialogs and pass the request context
        serializer = DialogSerializer(dialogs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class DialogMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)

        # Check if the dialog exists
        dialog = DialogsModel.dialog_exists(request.user, other_user)
        if not dialog:
            return Response({"detail": "Dialog not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch the messages for the dialog
        messages = MessageModel.objects.filter(
            Q(sender=request.user, recipient=other_user) |
            Q(sender=other_user, recipient=request.user)
        ).order_by('created')

        # Serialize the messages and pass the request context
        serializer = MessageSerializer(messages, many=True, context={'request': request})
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

class GroupListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = InboxGroup.objects.filter(members=request.user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        group = InboxGroup.objects.create(name=name, admin=request.user)
        group.members.add(request.user)
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupAddMemberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(InboxGroup, id=group_id)

        # Only admin can add members
        if request.user != group.admin:
            return Response({'error': 'Only admin can add members.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            group.members.add(user)
            return Response({'message': f'User {user.email} added to the group.'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)


class GroupRemoveMemberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(InboxGroup, id=group_id)

        # Only admin can remove members
        if request.user != group.admin:
            return Response({'error': 'Only admin can remove members.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            group.members.remove(user)
            return Response({'message': f'User {user.email} removed from the group.'})
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class MessageListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(InboxGroup, id=group_id)
        
        if request.user not in group.members.all():
            return Response({'error': 'You are not a member of this group.'}, status=status.HTTP_403_FORBIDDEN)

        messages = InboxMessage.objects.filter(group=group)
        serializer = GroupMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, group_id):
        group = get_object_or_404(InboxGroup, id=group_id)

        if request.user not in group.members.all():
            return Response({'error': 'You are not a member of this group.'}, status=status.HTTP_403_FORBIDDEN)

        content = request.data.get('content')
        message = InboxMessage.objects.create(group=group, sender=request.user, content=content)
        serializer = GroupMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
