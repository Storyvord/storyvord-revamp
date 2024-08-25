# client/serializers.py
from rest_framework import serializers

from storyvord.utils import Base64FileField
from .models import *
from accounts.models import User
from django.shortcuts import get_object_or_404

class ProfileSerializer(serializers.ModelSerializer):
    image = Base64FileField(required=False, allow_null=True)
    # email = serializers.EmailField(source='user.email', read_only=True)  # Include user's email field

    class Meta:
        model = ClientProfile
        fields = ['firstName', 'lastName', 'formalName', 'role', 'description', 'address', 'countryName', 'locality', 'personalWebsite', "image", "phone_number", "employee_profile"]  # Change: Added user_type to fields
    
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        if self.instance:  # Checks if an instance is being updated
            self.fields.pop('user', None)  # Removes 'user' field from serializer if updating an instance
    
class ClientCompanyProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ClientCompanyProfile
        fields = "__all__"

class ClientCompanyFolderSerializer(serializers.ModelSerializer):
    files = serializers.StringRelatedField(many=True, required=False)
    allowed_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClientCompanyFolder
        fields = ['id', 'name', 'description', 'icon', 'company', 'files', 'allowed_users', 'created_by']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        allowed_users = validated_data.pop('allowed_users', [])
        if user:
            validated_data['created_by'] = request.user

        # Create the folder instance
        folder = ClientCompanyFolder.objects.create(**validated_data)

        # Add the user creating the folder to allowed_users
        if request and hasattr(request, 'user'):
            folder.allowed_users.add(request.user)

        # Add the company owner (if company exists) to allowed_users
        if folder.company:
            company_owner = folder.company.user
            folder.allowed_users.add(company_owner)

        # Add any other allowed users
        folder.allowed_users.add(*allowed_users)

        return folder

    def update(self, instance, validated_data):
        allowed_users = validated_data.pop('allowed_users', [])
        instance = super().update(instance, validated_data)
        instance.allowed_users.set(allowed_users)
        return instance

class ClientCompanyFileSerializer(serializers.ModelSerializer):
    file = Base64FileField(required=False, allow_null=True)
    class Meta:
        model = ClientCompanyFile
        fields = ['id', 'name', 'file', 'folder']

    def validate(self, data):
        folder = data.get('folder')
        if not folder:
            raise serializers.ValidationError("Folder is required.")
        return data

class ClientCompanyFileUpdateSerializer(serializers.ModelSerializer):
    folder = serializers.PrimaryKeyRelatedField(read_only = True)
    
    class Meta:
        model = ClientCompanyFile
        fields = ['id', 'name', 'file', 'folder']
    
    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        folder = data.get('folder')

        if folder and folder.created_by != user:
            raise serializers.ValidationError("You do not have permission to edit files in this folder.")
        
        return data

class ClientCompanyFolderUpdateSerializer(serializers.ModelSerializer):
    files = ClientCompanyFileSerializer(many=True, required=False)
    allowed_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    add_users = serializers.ListField(child=serializers.EmailField(), write_only=True, required=False)
    remove_users = serializers.ListField(child=serializers.EmailField(), write_only=True, required=False)
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = ClientCompanyFolder
        fields = ['id', 'description', 'icon', 'name', 'company', 'files', 'allowed_users', 'add_users', 'remove_users', 'created_by']

    def validate(self, data):
        folder = self.instance
        user = self.context['request'].user

        # Prevent changing the company field
        if 'company' in data:
            raise serializers.ValidationError({"company": "You cannot change the company of a folder."})

        # Prevent editing allowed_users directly
        if 'allowed_users' in data:
            raise serializers.ValidationError({"allowed_users": "You cannot update allowed_users field directly. Use 'add_users' and 'remove_users' fields instead."})

        # Ensure the user is the owner of the folder or has permissions
        if folder and folder.created_by != user:
            raise serializers.ValidationError({"detail": "You do not have permission to edit this folder."})

        return data

    def update(self, instance, validated_data):
        add_users_emails = validated_data.pop('add_users', [])
        remove_users_emails = validated_data.pop('remove_users', [])

        # Add users
        for user_email in add_users_emails:
            user = get_object_or_404(User, email=user_email)
            if user not in instance.company.crew_profiles.all():
                raise serializers.ValidationError({"add_users": f"User {user_email} is not part of the company crew."})
            instance.allowed_users.add(user)

        # Remove users
        for user_email in remove_users_emails:
            user = get_object_or_404(User, email=user_email)
            instance.allowed_users.remove(user)

        # Make sure the user performing the update is in the allowed_users list
        if self.context['request'].user not in instance.allowed_users.all():
            instance.allowed_users.add(self.context['request'].user)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('exclude_files'):
            representation.pop('files', None)
        return representation
        

# Calendar

class ClientCompanyEventSerializer(serializers.ModelSerializer):
    calendar = serializers.PrimaryKeyRelatedField(read_only=True)
    document = Base64FileField(required=False, allow_null=True)

    class Meta:
        model = ClientCompanyEvent
        fields = '__all__'

    def validate(self, data):
        request = self.context.get('request')
        user = request.user

        # Ensure that the user has a company profile
        try:
            company_profile = ClientCompanyProfile.objects.get(user=user)
        except ClientCompanyProfile.DoesNotExist:
            raise serializers.ValidationError("Company profile not found for this user.")

        # Ensure the end time is after the start time
        if data.get('start') and data.get('end') and data['start'] >= data['end']:
            raise serializers.ValidationError("The end time must be after the start time.")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # Pop participants from validated data to handle them separately
        participants = validated_data.pop('participants', [])

        # Fetch or create the company calendar
        company_profile = ClientCompanyProfile.objects.get(user=user)
        calendar, created = ClientCompanyCalendar.objects.get_or_create(company=company_profile)

        # Associate the calendar with the event
        validated_data['calendar'] = calendar

        # Create the event
        event = ClientCompanyEvent.objects.create(**validated_data)

        # Add participants to the event
        event.participants.set(participants)

        return event

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        # Ensure that the event belongs to the user's company
        company_profile = ClientCompanyProfile.objects.get(user=user)
        if instance.calendar.company != company_profile:
            raise serializers.ValidationError("You do not have permission to update this event.")

        # Handle participants separately
        participants = validated_data.pop('participants', None)
        if participants is not None:
            instance.participants.set(participants)

        # Ensure the calendar is not being changed
        validated_data['calendar'] = instance.calendar

        # Update the event with the validated data
        return super().update(instance, validated_data)