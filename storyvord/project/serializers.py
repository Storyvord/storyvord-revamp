from rest_framework import serializers
from .models import LocationDetail, Project

class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetail
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    location_details = LocationDetailSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

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