
# # callsheets/serializers.py
# from rest_framework import serializers
# from .models import CallSheet

# class CallSheetSerializer(serializers.ModelSerializer):
#     date = serializers.DateField(input_formats=['%d/%m/%Y'], allow_null=True, required=False)

#     calltime = serializers.TimeField(format='%I:%M %p')  # format: 10:52 AM/PM
#     breakfast = serializers.TimeField(format='%I:%M %p')
#     lunch = serializers.TimeField(format='%I:%M %p') 
#     sunrise = serializers.TimeField(format='%I:%M %p')  # Keep it as TimeField
#     sunset = serializers.TimeField(format='%I:%M %p') 

#     class Meta:
#         model = CallSheet
#         fields = '__all__'



# callsheets/serializers.py
from rest_framework import serializers
from .models import CallSheet
from project.models import Project
from crew.serializers import CrewProfileSerializer 

class CallSheetSerializer(serializers.ModelSerializer):
    # date = serializers.DateField(input_formats=['%d/%m/%Y'], allow_null=True, required=False)
    date = serializers.DateField(input_formats=['%d/%m/%Y'], required=True)
    calltime = serializers.TimeField(format='%I:%M %p')  # format: 10:52 AM/PM
    breakfast = serializers.TimeField(format='%I:%M %p')
    lunch = serializers.TimeField(format='%I:%M %p') 
    # sunrise = serializers.TimeField(format='%I:%M %p')
    # sunset = serializers.TimeField(format='%I:%M %p') 

    class Meta:
        model = CallSheet
        fields = '__all__'  # Include all fields defined in the CallSheet model

# equipment
    equipment = serializers.SerializerMethodField()
    def get_equipment(self, obj):
     project = obj.project
     equipment = project.equipment.all()
     return [{ 'title': eq.title, 'quantity': eq.quantity} for eq in equipment]

# crew 
    crew_members = serializers.SerializerMethodField()
    def get_crew_members(self, obj):
        project = obj.project
        crew_members = project.crew_profiles.all()
        return CrewProfileSerializer(crew_members, many=True).data


    def create(self, validated_data):
        # Project information is fetched and passed through serializer
        project = validated_data.get('project')
        # project_data = Project.objects.get(id=project.id)  # Ensure correct field to get project data
        project_data = Project.objects.get(project_id=project.project_id)  
        # Create the CallSheet instance
        call_sheet = CallSheet.objects.create(
            project=project,
            title=validated_data.get('title'),
            date=validated_data.get('date'),
            calltime=validated_data.get('calltime'),
            breakfast=validated_data.get('breakfast'),
            lunch=validated_data.get('lunch'),
            # sunrise=validated_data.get('sunrise'),
            # sunset=validated_data.get('sunset'),
            additional_details=validated_data.get('additional_details', 'No additional details provided'),
            # project_name=project_data.name,
            location=project_data.location_details.first().location if project_data.location_details.exists() else '',
            street=validated_data.get('street', 'Default Street'),
            city=validated_data.get('city', 'Default City'),
            country=validated_data.get('country', 'Default Country'),
            website=validated_data.get('website', 'https://example.com'),
            contact_number=validated_data.get('contact_number', '000-000-0000'),
            producer=validated_data.get('producer', 'Default Producer'),
            producer_number=validated_data.get('producer_number', '000-000-0000'),
            director=validated_data.get('director', 'Default Director'),
            director_number=validated_data.get('director_number', '000-000-0000'),
            # production_manager=validated_data.get('production_manager', 'Default Production Manager'),
            # production_manager_number=validated_data.get('production_manager_number', '000-000-0000'),
            # weather=validated_data.get('weather', 'Default Weather'),
            nearest_hospital_address=validated_data.get('nearest_hospital_address', 'Default Hospital Address'),
            nearest_police_station=validated_data.get('nearest_police_station', 'Default Police Station'),
            nearest_fire_station=validated_data.get('nearest_fire_station', 'Default Fire Station')
        )
        
        return call_sheet
