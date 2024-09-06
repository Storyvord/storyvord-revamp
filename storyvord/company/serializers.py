from rest_framework import serializers
from .models import *
from client.models import ClientCompanyProfile, ClientProfile  
from accounts.models import User

class AddressBookSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBookSkills
        fields = '__all__'

class AddressBookCateringInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBookCateringInformation
        fields = '__all__'

class AddressBookHomeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBookHomeAddress
        fields = '__all__'

class AddressBookFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressBookFiles
        fields = '__all__'

class AddressBookSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.ReadOnlyField(source='created_by.id')
    
    # Nested serializers
    skills = AddressBookSkillsSerializer(many=True, read_only=True)
    catering_information = AddressBookCateringInformationSerializer(many=True, read_only=True)
    home_address = AddressBookHomeAddressSerializer(many=True, read_only=True)
    files = AddressBookFilesSerializer(many=True, read_only=True)

    class Meta:
        model = AddressBook
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        company_profile = ClientCompanyProfile.objects.get(user=user)

        validated_data['company'] = company_profile
        validated_data['created_by'] = user
        address_book_entry = AddressBook.objects.create(**validated_data)

        # Handling related models (skills, catering, home address, files)
        skills_data = request.data.get('skills', [])
        for skill_data in skills_data:
            AddressBookSkills.objects.create(address_book=address_book_entry, **skill_data)

        catering_info_data = request.data.get('catering_information', [])
        for catering_data in catering_info_data:
            AddressBookCateringInformation.objects.create(address_book=address_book_entry, **catering_data)

        home_address_data = request.data.get('home_address', [])
        for address_data in home_address_data:
            AddressBookHomeAddress.objects.create(address_book=address_book_entry, **address_data)

        files_data = request.data.get('files', [])
        for file_data in files_data:
            AddressBookFiles.objects.create(address_book=address_book_entry, **file_data)

        return address_book_entry

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        if instance.company.user != user:
            raise serializers.ValidationError("You do not have permission to update this address book entry.")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        AddressBookSkills.objects.filter(address_book=instance).delete()
        skills_data = request.data.get('skills', [])
        for skill_data in skills_data:
            AddressBookSkills.objects.create(address_book=instance, **skill_data)

        AddressBookCateringInformation.objects.filter(address_book=instance).delete()
        catering_info_data = request.data.get('catering_information', [])
        for catering_data in catering_info_data:
            AddressBookCateringInformation.objects.create(address_book=instance, **catering_data)

        AddressBookHomeAddress.objects.filter(address_book=instance).delete()
        home_address_data = request.data.get('home_address', [])
        for address_data in home_address_data:
            AddressBookHomeAddress.objects.create(address_book=instance, **address_data)

        AddressBookFiles.objects.filter(address_book=instance).delete()
        files_data = request.data.get('files', [])
        for file_data in files_data:
            AddressBookFiles.objects.create(address_book=instance, **file_data)

        return instance

    def to_representation(self, instance):
        """Customize the representation to include related objects"""
        representation = super().to_representation(instance)
        representation['skills'] = AddressBookSkillsSerializer(instance.addressbookskills_set.all(), many=True).data
        representation['catering_information'] = AddressBookCateringInformationSerializer(instance.addressbookcateringinformation_set.all(), many=True).data
        representation['home_address'] = AddressBookHomeAddressSerializer(instance.addressbookhomeaddress_set.all(), many=True).data
        representation['files'] = AddressBookFilesSerializer(instance.addressbookfiles_set.all(), many=True).data
        return representation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

        
class CompanyTaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    completed = serializers.BooleanField(read_only=True)
    completion_requested = serializers.BooleanField(read_only=True)

    class Meta:
        model = ClientCompanyTask
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'completed', 'completion_requested', 'assigned_to')

    def validate_assigned_to(self, value):
        user = self.context['request'].user

        try:
            # Check if the assigned user is an employee of the client’s company
            clientProfile = ClientProfile.objects.get(user=user)
        except ClientProfile.DoesNotExist:
            raise serializers.ValidationError("Client profile does not exist for the current user.")

        if not clientProfile.employee_profile.filter(id=value.id).exists():
            raise serializers.ValidationError("The user is not an employee of the client’s company.")

        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user

        # Extract assigned_to from the initial data
        assigned_to_id = self.initial_data.get('assigned_to')
        if assigned_to_id:
            try:
                assigned_to_user = User.objects.get(id=assigned_to_id)
                validated_data['assigned_to'] = assigned_to_user
            except User.DoesNotExist:
                raise serializers.ValidationError("Assigned user does not exist.")

        return super().create(validated_data)


class TaskCompletionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCompanyTask
        fields = ('completion_requested', 'requester')
        read_only_fields = ('requester',)

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at']