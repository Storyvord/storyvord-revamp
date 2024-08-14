from rest_framework import serializers
from .models import File, Folder
from accounts.models import User
from django.shortcuts import get_object_or_404
# import base64
# from django.core.files.base import ContentFile

# class Base64FileField(serializers.FileField):
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
#         return super().to_internal_value(data)


class FileSerializer(serializers.ModelSerializer):
    # file = Base64FileField(required=False, allow_null=True)
    class Meta:
        model = File
        fields = '__all__'
        # fields = ['id', 'name', 'file', 'folder']

        
class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)
    allowed_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Folder 
        fields = ['id', 'description', 'icon', 'name', 'project', 'default', 'files', 'allowed_users', 'created_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('exclude_files'):
            representation.pop('files', None)
        return representation

    def validate(self, data):
        project = data.get('project')
        name = data.get('name')
        if project and Folder.objects.filter(project=project, name=name).exists():
            raise serializers.ValidationError({"detail": "Folder with the same name already exists in this project."})
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user  # Set created_by with the request user

        allowed_users = validated_data.pop('allowed_users', [])
        folder = Folder.objects.create(**validated_data)

        # Add the user creating the folder to allowed_users
        folder.allowed_users.add(request.user)
        folder.allowed_users.add(*allowed_users)

        return folder




        
class FolderUpdateSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)
    allowed_users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)
    add_users = serializers.ListField(child=serializers.EmailField(), write_only=True, required=False)
    remove_users = serializers.ListField(child=serializers.EmailField(), write_only=True, required=False)
    created_by = serializers.ReadOnlyField(source='created_by.id')

    class Meta:
        model = Folder 
        fields = ['id', 'description', 'icon', 'name', 'project', 'default', 'files', 'allowed_users', 'add_users', 'remove_users', 'created_by']

    def validate(self, data):
        folder = self.instance
        user = self.context['request'].user

        # Prevent changing the project field
        if 'project' in data:
            raise serializers.ValidationError({"project": "You cannot change the project of a folder."})

        # Prevent editing allowed_users directly
        if 'allowed_users' in data:
            raise serializers.ValidationError({"allowed_users": "You cannot update allowed_users field directly. Use 'add_users' and 'remove_users' fields instead."})

        # Ensure the user is the owner of the project
        if folder and folder.created_by != user and not folder.project.user == user:
            raise serializers.ValidationError({"detail": "You do not have permission to edit this folder."})

        return data
    
    def update(self, instance, validated_data):
        add_users_emails = validated_data.pop('add_users', [])
        remove_users_emails = validated_data.pop('remove_users', [])
        
        # Add users
        for user_email in add_users_emails:
            user = get_object_or_404(User, email=user_email)
            if user not in instance.project.crew_profiles.all():
                raise serializers.ValidationError({"add_users": f"User {user_email} is not part of the project crew."})
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
