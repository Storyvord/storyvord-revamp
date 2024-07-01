# client/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)  # Include user's email field

    class Meta:
        model = Profile
        fields = ['email', 'phone_number', 'address', 'image']  # Include 'email' in the fields list
