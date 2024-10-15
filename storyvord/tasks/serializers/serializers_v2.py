from rest_framework import serializers
from ..models import ProjectTask, Membership
from accounts.models import User
    

class ProjectTaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.ListField(
        child=serializers.IntegerField(),  # Expect list of user IDs as integers
        allow_empty=False
    )
    
    class Meta:
        model = ProjectTask
        fields = ['id', 'project', 'title', 'description', 'assigned_to', 'due_date', 'status', 'is_completed']
        
    def validate(self, data):
        assigned_to_data = data.get('assigned_to', [])
        project = data.get('project')

        if project is None:
            raise serializers.ValidationError({'project': 'Project is required to validate assigned users.'})
        
        # Check if each assigned user exists
        users = User.objects.filter(id__in=assigned_to_data)
        if users.count() != len(assigned_to_data):
            raise serializers.ValidationError({'assigned_to': 'One or more assigned users do not exist.'})

        # Ensure that assigned_to contains valid user IDs and members of the project
        project_members = Membership.objects.filter(project=project).values_list('user_id', flat=True)
        invalid_members = [user_id for user_id in assigned_to_data if user_id not in project_members]

        if invalid_members:
            raise serializers.ValidationError({'assigned_to': f'The following users are not members of the project: {invalid_members}'})
        return data
    
    def create(self, validated_data):
        try:
            assigned_to_data = validated_data.pop('assigned_to', [])
            user_membership = Membership.objects.get(user=self.context['request'].user)
            validated_data['assigned_by'] = user_membership
            task = ProjectTask.objects.create(**validated_data)
            task.assigned_to.set(assigned_to_data)
            return task
        except Exception as exc:
            print(f"Error in task creation: {exc}")
            raise exc
        
    def update(self, instance, validated_data):
        assigned_to_data = validated_data.pop('assigned_to', None)
        
        # Update fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.status = validated_data.get('status', instance.status)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.assigned_by = validated_data.get('assigned_by', instance.assigned_by)
        
        # Update many-to-many relationship for assigned_to
        if assigned_to_data is not None:
            instance.assigned_to.set(assigned_to_data)
        
        instance.save()
        return instance
        
