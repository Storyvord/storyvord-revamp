from rest_framework import serializers

from crew.models import CrewEvent
from .models import Calendar, Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

    def validate_participants(self, value):
        calendar_id = self.initial_data.get('calendar')
        calendar = Calendar.objects.get(id=calendar_id)
        project = calendar.project
        crew_profiles = project.crew_profiles.all()

        for user in value:
            if user not in crew_profiles:
                raise serializers.ValidationError(f"User {user} is not part of the crew_profiles for this project.")

        return value

class CalendarSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Calendar
        fields = '__all__'


class CrewEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewEvent
        fields = '__all__'