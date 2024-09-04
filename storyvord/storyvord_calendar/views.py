from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Calendar, Event
from .serializers import CalendarSerializer, EventSerializer
from rest_framework.permissions import IsAuthenticated
from client.models import ClientProfile

class CalendarView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarSerializer

    def get(self, request, project_id=None):
        if project_id:
            calendar = get_object_or_404(Calendar, project=project_id)
            serializer = self.serializer_class(calendar)
        else:
            calendars = Calendar.objects.filter(
                project__crew_profiles=request.user
            ).distinct() | Calendar.objects.filter(
                project__user=request.user
            ).distinct()

            serializer = self.serializer_class(calendars, many=True)
        return Response(serializer.data)

class EventView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    def get(self, request, project_id, pk=None):
        calendar = get_object_or_404(Calendar, project=project_id)

        user_is_crew = calendar.project.crew_profiles.filter(pk=request.user.pk).exists()
        user_is_creator = calendar.project.user == request.user
        client_profile = ClientProfile.objects.get(user=calendar.project.user)
        user_is_employee = client_profile.employee_profile.filter(pk=request.user.pk).exists()
 
        if not (user_is_crew or user_is_creator or user_is_employee):
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to access this calendar"})
        if pk:
            event = get_object_or_404(Event, pk=pk, calendar=calendar)
            if not (event.participants.filter(pk=request.user.pk).exists() or user_is_creator):
                return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to access this event"})
            serializer = EventSerializer(event)
        else:
            if user_is_creator:
                events = calendar.events.all()
            else:
                events = calendar.events.filter(participants=request.user)

            # Debugging: Log the queryset to see if it's empty
            if not events.exists():
                return Response({"detail": "No events found for this user"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = EventSerializer(events, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        calendar = get_object_or_404(Calendar, project=project_id)
        data = request.data.copy()
        data['calendar'] = calendar.id 
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, project_id, pk):
        calendar = get_object_or_404(Calendar, project=project_id)
        event = get_object_or_404(Event, pk=pk, calendar=calendar)
        data = request.data.copy()
        data['calendar'] = calendar.id 
        serializer = self.serializer_class(event, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, pk):
        calendar = get_object_or_404(Calendar, project=project_id)
        event = get_object_or_404(Event, pk=pk, calendar=calendar)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)