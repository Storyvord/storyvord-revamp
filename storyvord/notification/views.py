# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Announcement, Notification
from .serializers import NotificationSerializer
from django.contrib.auth.models import User

class NotificationListAPIView(APIView):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
