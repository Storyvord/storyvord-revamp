from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import check_password
from client.models import ClientProfile
from crew.models import CrewProfile
from accounts.models import User,PersonalInfo,UserType
from django.contrib.auth import authenticate
from django.db import IntegrityError
import logging
import datetime

logger = logging.getLogger(__name__)

### Version 2 START ####
    
class V2RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already exists")]
    )
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    terms_accepted = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = ['id','email', 'password', 'confirm_password', 'terms_accepted']

    def validate(self, data):
        if 'email' not in data:
            raise serializers.ValidationError("Email field is required")
        if 'password' not in data:
            raise serializers.ValidationError("Password field is required")
        if 'confirm_password' not in data:
            raise serializers.ValidationError("Confirm Password field is required")
        if not data.get('terms_accepted'):
            raise serializers.ValidationError("You must agree to the Terms and Conditions.")
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        # Create the user with the validated data

        validated_data.pop('terms_accepted')
        validated_data.pop('confirm_password')
        try: 
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                created_at=datetime.datetime.now(),
                last_login=datetime.datetime.now(),
                user_stage=0,
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError("Email already exists")  # Handle unique constraint violation
    
class V2LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Authenticate the user using email and password
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')
        
        # Check the password using check_password
        if not check_password(data['password'], user.password):
            raise serializers.ValidationError('Invalid email or password')
             
        if user.is_active:
            self.context['user'] = user
            return data
        
        raise serializers.ValidationError('User account is disabled')
    
    
    
class V2UserDataSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = '__all__'
        
class SelectUserTypeSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_type']
        
    def validate_user_type(self, value):
        try:
            user_type_instance = UserType.objects.get(name=value)
            return user_type_instance
        except UserType.DoesNotExist:
            raise serializers.ValidationError("Invalid user type provided.")

    def update(self, instance, validated_data):
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.user_stage = 1
        instance.save()
        return instance

class PersonalInfoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        model = PersonalInfo
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}  # Prevent user from being included in the input data
        }

    def validate(self, data):
        user = self.context.get('user')
        user_id = user.id if user else None
        if user_id is not None:
            if PersonalInfo.objects.filter(user_id=user_id).exists():
                raise serializers.ValidationError("Personal info already exists for the user.")
        return data
        
class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}  # Prevent user from being included in the input data
        }

class CrewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}  # Prevent user from being included in the input data
        }
        
class UnifiedProfileSerializer(serializers.Serializer):
    personal_info = PersonalInfoSerializer()
    client_profile = ClientProfileSerializer(required=False)
    crew_profile = CrewProfileSerializer(required=False)

    def validate(self, data):
        user_type_id = self.context.get('user_type_id')
        
        if user_type_id is None:
            raise serializers.ValidationError({"error": "User type is not provided in context."})
        
        # Ensure only one of the profiles is provided based on user_type
        if user_type_id == 1 and 'client_profile' not in data:
            raise serializers.ValidationError({"client_profile": "Client profile data is required."})
        elif user_type_id == 2 and 'crew_profile' not in data:
            raise serializers.ValidationError({"crew_profile": "Crew profile data is required."})
        return data

class V2EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']   

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.DictField()
    personal_info = PersonalInfoSerializer()
    client_profile = ClientProfileSerializer(required=False)
    crew_profile = CrewProfileSerializer(required=False)
    
    class Meta:
        model= User
        fields = ['user', 'personal_info', 'client_profile', 'crew_profile']
    
### END #### 
