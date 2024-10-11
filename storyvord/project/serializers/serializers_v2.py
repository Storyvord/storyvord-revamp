from rest_framework import serializers
from ..models import (
    ProjectDetails, ProjectRequirements, ShootingDetails, 
    Role, Permission, Membership, CrewRequirements, EquipmentRequirements,
    ProjectCrewRequirement, ProjectEquipmentRequirement
)
from accounts.models import Permission as AccountPermission
from rest_framework.exceptions import PermissionDenied

# Permission Serializer
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['name', 'description']

# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    permission = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ['name', 'permission', 'description', 'project', 'is_global']


# Membership Serializer
class MembershipSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    user = serializers.StringRelatedField()  # Show the username or other identifier for the user

    class Meta:
        model = Membership
        fields = ['user', 'role', 'project', 'created_at']


# Crew Requirements Serializer
class CrewRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewRequirements
        fields = '__all__'


# Equipment Requirements Serializer
class EquipmentRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentRequirements
        fields = '__all__'


# Project Serializer
class ProjectDetailsSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()  # Show the username or other identifier for the owner
    members = MembershipSerializer(source='memberships', many=True, read_only=True)
    
    class Meta:
        model = ProjectDetails
        fields = ['project_id', 'owner', 'members', 'name', 'content_type', 'brief', 'additional_details', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        create_project_permission = AccountPermission.objects.get(name='create_project')
        user_type = user.user_type
        
        if user_type is None or not user_type.permissions.filter(id=create_project_permission.id).exists():
            raise PermissionDenied("You don't have permission to create a project.")
        
        validated_data['owner'] = self.context['request'].user
        return ProjectDetails.objects.create(**validated_data)

# Project Requirements Serializer
class ProjectRequirementsSerializer(serializers.ModelSerializer):
    crew_requirements = CrewRequirementsSerializer(many=True, read_only=True)
    equipment_requirements = EquipmentRequirementsSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectRequirements
        fields = ['project', 'budget_currency', 'budget', 'crew_requirements', 'equipment_requirements', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        if validated_data['project'].owner == self.context['request'].user:
            validated_data['created_by'] = self.context['request'].user
            validated_data['updated_by'] = self.context['request'].user
            return ProjectRequirements.objects.create(**validated_data)
        
        if Membership.objects.filter(project=validated_data['project'], user=self.context['request'].user).exists() == False:
            raise PermissionDenied("Membership doesnt have required permission.")
        
        if self.context['request'].user is None or validated_data['project'].owner != self.context['request'].user:
            raise PermissionDenied("You don't have permission to create a project requirement.")
        
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return ProjectRequirements.objects.create(**validated_data)


# Shooting Details Serializer
class ShootingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShootingDetails
        fields = '__all__'


# Project Crew Requirement Serializer
class ProjectCrewRequirementSerializer(serializers.ModelSerializer):
    crew = CrewRequirementsSerializer()

    class Meta:
        model = ProjectCrewRequirement
        fields = ['project', 'crew', 'quantity']


# Project Equipment Requirement Serializer
class ProjectEquipmentRequirementSerializer(serializers.ModelSerializer):
    equipment = EquipmentRequirementsSerializer()

    class Meta:
        model = ProjectEquipmentRequirement
        fields = ['project', 'equipment', 'quantity']
