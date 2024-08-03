from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Calendar, Event, Project
from .serializers import CalendarSerializer, EventSerializer
from rest_framework.permissions import IsAuthenticated

class CalendarView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarSerializer
    def get(self, request, project_id=None):
        if project_id:
            calendar = get_object_or_404(Calendar, project=project_id)
            if not calendar.project.crew_profiles.filter(pk=request.user.pk).exists():
                return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to access this calendar"})
            serializer = CalendarSerializer(calendar)
        else:
            # calendars = Calendar.objects.all()
            calendars = Calendar.objects.filter(project__crew_profiles=request.user).distinct()
            serializer = CalendarSerializer(calendars, many=True)
        return Response(serializer.data)

class EventView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    def get(self, request, project_id, pk=None):
        calendar = get_object_or_404(Calendar, project=project_id)
        if not calendar.project.crew_profiles.filter(pk=request.user.pk).exists():
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to access this calendar"})
        if pk:
            event = get_object_or_404(Event, pk=pk, calendar=calendar)
            if not event.participants.filter(pk=request.user.pk).exists():
                return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to access this event"})
            serializer = EventSerializer(event)
        else:
            events = calendar.events.filter(participants=request.user)
            serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        calendar = get_object_or_404(Calendar, project=project_id)
        if not calendar.project.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Only the project owner can add events to the calendar"})
        data = request.data.copy()
        data['calendar'] = calendar.id 
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save(calendar=calendar)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id, pk):
        calendar = get_object_or_404(Calendar, project=project_id)
        if not calendar.project.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Only the project owner can update events to the calendar"})
        event = get_object_or_404(Event, pk=pk, calendar=calendar)
        data = request.data.copy()
        data['calendar'] = calendar.id 
        serializer = EventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, pk):
        calendar = get_object_or_404(Calendar, project=project_id)
        if not calendar.project.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Only the project owner can delete events to the calendar"})
        event = get_object_or_404(Event, pk=pk, calendar=calendar)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
