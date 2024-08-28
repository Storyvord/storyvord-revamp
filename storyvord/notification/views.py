# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Announcement, Notification
from .serializers import NotificationSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class NotificationListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class UnreadNotificationCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        count = Notification.objects.filter(user=request.user, read=False).count()
        return Response({'count': count})