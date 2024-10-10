from rest_framework import serializers
from ...models import *
from crew.serializers import CrewProfileSerializer
import base64
from django.core.files.base import ContentFile

class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)

class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetail
        fields = '__all__'

class SelectCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectCrew
        fields = '__all__'

class SelectEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectEquipment
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    location_details = LocationDetailSerializer(many=True)
    selected_crew = SelectCrewSerializer(many=True)
    equipment = SelectEquipmentSerializer(many=True)
    uploaded_document = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = Project
        exclude = ['user']

    def create(self, validated_data):
        location_details_data = validated_data.pop('location_details')
        selected_crew_data = validated_data.pop('selected_crew')
        equipment_data = validated_data.pop('equipment')
        
        project = Project.objects.create(**validated_data)
        
        for location_data in location_details_data:
            location_detail, created = LocationDetail.objects.get_or_create(**location_data)
            project.location_details.add(location_detail)
        
        for crew_data in selected_crew_data:
            crew, created = SelectCrew.objects.get_or_create(**crew_data)
            project.selected_crew.add(crew)
        
        for equipment_data in equipment_data:
            equipment, created = SelectEquipment.objects.get_or_create(**equipment_data)
            project.equipment.add(equipment)
        
        return project

    def update(self, instance, validated_data):
        location_details_data = validated_data.pop('location_details', None)
        selected_crew_data = validated_data.pop('selected_crew', None)
        equipment_data = validated_data.pop('equipment', None)
        
        instance = super().update(instance, validated_data)
        
        if location_details_data:
            instance.location_details.clear()
            for location_data in location_details_data:
                location_detail, created = LocationDetail.objects.get_or_create(**location_data)
                instance.location_details.add(location_detail)
        
        if selected_crew_data:
            instance.selected_crew.clear()
            for crew_data in selected_crew_data:
                crew, created = SelectCrew.objects.get_or_create(**crew_data)
                instance.selected_crew.add(crew)
        
        if equipment_data:
            instance.equipment.clear()
            for equipment_data in equipment_data:
                equipment, created = SelectEquipment.objects.get_or_create(**equipment_data)
                instance.equipment.add(equipment)
        
        return instance
    
class OnboardRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardRequest
        fields = ['id', 'project', 'user', 'status', 'created_at', 'updated_at']
        
class OnboardRequestsByProjectSerializer(serializers.Serializer):
    pending_requests = serializers.SerializerMethodField()
    accepted_requests = serializers.SerializerMethodField()
    declined_requests = serializers.SerializerMethodField()

    def get_pending_requests(self, obj):
        onboard_requests = OnboardRequest.objects.filter(project=obj, status='pending')
        return OnboardRequestSerializer(onboard_requests, many=True).data

    def get_accepted_requests(self, obj):
        onboard_requests = OnboardRequest.objects.filter(project=obj, status='accepted')
        return OnboardRequestSerializer(onboard_requests, many=True).data

    def get_declined_requests(self, obj):
        onboard_requests = OnboardRequest.objects.filter(project=obj, status='declined')
        return OnboardRequestSerializer(onboard_requests, many=True).data

class UserSerializer(serializers.ModelSerializer):
    profile = CrewProfileSerializer(source='crewprofile', read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'profile']