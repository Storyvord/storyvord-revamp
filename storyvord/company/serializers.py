from rest_framework import serializers
from .models import AddressBook, ClientCompanyProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class AddressBookSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AddressBook
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value

    def validate_positions(self, value):
        if value and len(value) < 5:
            raise serializers.ValidationError("Positions must be at least 5 characters long.")
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        # Fetch the user's company profile
        company_profile = ClientCompanyProfile.objects.get(user=user)

        # Associate the company and the user who created this address
        validated_data['company'] = company_profile
        validated_data['created_by'] = user

        # Create and return the AddressBook instance
        address_book_entry = AddressBook.objects.create(**validated_data)
        return address_book_entry

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        # Ensure the user is updating their own company's address book entry
        if instance.company.user != user:
            raise serializers.ValidationError("You do not have permission to update this address book entry.")

        # Update the AddressBook instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
