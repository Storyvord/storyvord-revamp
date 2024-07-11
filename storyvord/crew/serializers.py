from rest_framework import serializers
from .models import *

class CrewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewProfile
        fields = '__all__'
        read_only_fields = ('user',)

class CrewCreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewCredits
        fields = '__all__'
        
class CrewEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewEducation
        fields = '__all__'
        
class CrewRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewRate
        fields = '__all__'
        
class EndorsementfromPeersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndorsementfromPeers
        fields = '__all__'

class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = '__all__'