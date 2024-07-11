from rest_framework import serializers
from .models import *
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

class ProjectSerializer(serializers.ModelSerializer):
    location_details = LocationDetailSerializer(many=True)
    uploaded_document = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = Project
        exclude = ['user']

    def create(self, validated_data):
        location_details_data = validated_data.pop('location_details')
        project = Project.objects.create(**validated_data)
        for location_data in location_details_data:
            location_detail, created = LocationDetail.objects.get_or_create(**location_data)
            project.location_details.add(location_detail)
        return project

    def update(self, instance, validated_data):
        location_details_data = validated_data.pop('location_details', None)
        instance = super().update(instance, validated_data)
        
        if location_details_data:
            instance.location_details.clear()
            for location_data in location_details_data:
                location_detail, created = LocationDetail.objects.get_or_create(**location_data)
                instance.location_details.add(location_detail)
        
        return instance
    
class OnboardRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardRequest
        fields = ['id', 'project', 'user', 'status', 'created_at', 'updated_at']