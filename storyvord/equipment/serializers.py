# equipment/serializers.py
from rest_framework import serializers
from .models import EquipmentCategory, EquipmentModel, EquipmentInstance, EquipmentLog

class EquipmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = '__all__'

class EquipmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentModel
        fields = '__all__'

class EquipmentInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentInstance
        fields = '__all__'

class EquipmentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentLog
        fields = '__all__'
