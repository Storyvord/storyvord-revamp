
# callsheets/serializers.py
from rest_framework import serializers
from .models import CallSheet

class CallSheetSerializer(serializers.ModelSerializer):
    date = serializers.DateField(input_formats=['%d/%m/%Y'], allow_null=True, required=False)

    calltime = serializers.TimeField(format='%I:%M %p')  # format: 10:52 AM/PM
    breakfast = serializers.TimeField(format='%I:%M %p')
    lunch = serializers.TimeField(format='%I:%M %p') 
    sunrise = serializers.TimeField(format='%I:%M %p')  # Keep it as TimeField
    sunset = serializers.TimeField(format='%I:%M %p') 

    class Meta:
        model = CallSheet
        fields = '__all__'