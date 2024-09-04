from rest_framework import serializers
from .models import DialogsModel, MessageModel

class DialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialogsModel
        fields = ['id', 'user1', 'user2']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.id')  # Using PK for the sender
    recipient = serializers.ReadOnlyField(source='recipient.id')  # Using PK for the recipient

    class Meta:
        model = MessageModel
        fields = ['id', 'sender', 'recipient', 'text', 'read', 'created']
