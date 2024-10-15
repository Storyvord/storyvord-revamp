from rest_framework import serializers
from ..models import User, Project, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['project_id' ,'name', 'brief', 'created_at', 'created_by']
        
class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    completed = serializers.BooleanField(read_only=True)
    completion_requested = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user
        project_pk = self.context.get('project_pk')

        # Check if the project exists
        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            raise serializers.ValidationError({'project': 'Project not found.'})

        # Check if assigned user is a crew member in the project
        assigned_to = validated_data.get('assigned_to')
        if assigned_to is not None and not project.crew_profiles.filter(pk=assigned_to.pk).exists():
            raise serializers.ValidationError({'assigned_to': 'The user is not a crew member of the project.'})

        # Set created_by to the current user
        validated_data['created_by'] = user
        validated_data['project'] = project

        # Create and return the Task instance
        return Task.objects.create(**validated_data)



class TaskCompletionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('completion_requested', 'requester')
        read_only_fields = ('requester',)