# views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from notification.models import Notification
from .models import Announcement
from .serializers import AnnouncementSerializer
from django.contrib.auth.models import User


# Create your views here.
class AnnouncementListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementSerializer
    def get(self, request):
        announcements = Announcement.objects.all()
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            announcement = serializer.save()
            # Create notifications for recipients
            for user in announcement.recipients.all():
                Notification.objects.create(user=user, announcement=announcement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AnnouncementRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementSerializer

    def get_object(self, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        self.check_object_permissions(self.request, announcement)
        return announcement

    def get(self, request, pk):
        announcement = self.get_object(pk)
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data)

    def put(self, request, pk):
        announcement = self.get_object(pk)
        serializer = AnnouncementSerializer(announcement, data=request.data)
        if serializer.is_valid():
            announcement = serializer.save()
            # Create notifications for recipients
            for user in announcement.recipients.all():
                Notification.objects.create(user=user, announcement=announcement)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        announcement = self.get_object(pk)
        announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RecipientAnnouncementListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementSerializer
    def get(self, request):
        # Get announcements where the authenticated user is a recipient
        announcements = Announcement.objects.filter(recipients=request.user)
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)

class RecipientAnnouncementDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnnouncementSerializer
    def get_object(self, pk):
        # Get announcement where the authenticated user is a recipient
        announcement = get_object_or_404(Announcement, pk=pk, recipients=self.request.user)
        return announcement

    def get(self, request, pk):
        announcement = self.get_object(pk)
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data)