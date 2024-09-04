from rest_framework import serializers
from django.core.files.base import ContentFile
from .models import Calendar, Event
from client.models import ClientProfile
import base64

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
        client_profile = ClientProfile.objects.get(user=project.user)
        employee_profiles = client_profile.employee_profile.all()

        for user in value:
            if user not in crew_profiles and not employee_profiles.filter(id=user.id).exists():
                raise serializers.ValidationError(
                    f"User {user.email} is not part of the crew or an employee of the client."
                )

        return value

class CalendarSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Calendar
        fields = '__all__'

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method in ['POST', 'PUT']:
            project = data['project']
            crew_profiles = project.crew_profiles.all()
            client_profile = ClientProfile.objects.get(user=project.user)
            employee_profiles = client_profile.employee_profile.all()

            if request.user not in crew_profiles and not employee_profiles.filter(id=request.user.id).exists():
                raise serializers.ValidationError(
                    "You do not have permission to create or modify events in this calendar."
                )

        return data