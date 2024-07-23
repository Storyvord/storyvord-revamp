# client/serializers.py
from rest_framework import serializers
from .models import ClientProfile

class ProfileSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(source='user.email', read_only=True)  # Include user's email field

    class Meta:
        model = ClientProfile
        # fields = ['email', 'phone_number', 'address', 'image']  # Include 'email' in the fields list
        # fields = ['email', 'phone_number', 'address', 'image']  # Change: Added user_type to fields
        fields = ['firstName', 'lastName', 'formalName', 'role', 'description', 'address', 'countryName', 'locality', 'personalWebsite']  # Change: Added user_type to fields
        # fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        if self.instance:  # Checks if an instance is being updated
            self.fields.pop('user', None)  # Removes 'user' field from serializer if updating an instance
    

# {
#     "firstName": "Kaushik",
#     "lastName": "Shahare",
#     "formalName": "Kaushik Shahare",
#     "role": "producer",
#     "description": "Developer",
#     "address": "Badlapur, Thane, Maharashtra",
#     "countryName": "India",
#     "locality": "Thane",
#     "personalWebsite": "kaushik-shahare.com"
# }