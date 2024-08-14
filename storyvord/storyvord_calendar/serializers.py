from rest_framework import serializers

from crew.models import CrewEvent
from .models import Calendar, Event
import base64
from django.core.files.base import ContentFile

class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)
class EventSerializer(serializers.ModelSerializer):
    document = Base64FileField(required=False, allow_null=True)
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