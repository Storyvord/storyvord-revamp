# callsheets/serializers.py
from rest_framework import serializers
from.models import CallSheet

class CallSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallSheet
        fields = '__all__'
        