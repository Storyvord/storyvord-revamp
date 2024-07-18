# # accounts/serializers.py
# from rest_framework import serializers
# from .models import User

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'user_type']  # Change: Added user_type to fields
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             password=validated_data['password'],
#             user_type=validated_data['user_type']  # Change: Pass user_type to create_user
#         )
#         return user


from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'user_type')