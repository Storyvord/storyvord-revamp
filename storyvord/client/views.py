# client/views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ClientProfile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated  # Ensure this import is present
from rest_framework.parsers import MultiPartParser

# class ProfileAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Apply IsAuthenticated permission globally

#     def get(self, request):
#         # Fetch the profile of the logged-in user
#         profile = get_object_or_404(Profile, user=request.user)  # Modified to fetch profile by user
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)

#     def post(self, request):
#         # Ensure the logged-in user doesn't already have a profile
#         if Profile.objects.filter(user=request.user).exists():
#             return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)

#         # Create a new profile for the logged-in user
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import IsAuthenticated  # Ensure this import is present
from accounts.models import User  # Adjust the import path as per your User model location

# class ProfileAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Apply IsAuthenticated permission globally

#     def put(self, request):
#         # Ensure the logged-in user has an associated account
#         try:
#             user = User.objects.get(id=request.user.id)  # Change: Ensure user exists
#         except User.DoesNotExist:
#             return Response({"detail": "User account does not exist."}, status=status.HTTP_404_NOT_FOUND)  # Comment: Handle if user not found

#         # Ensure the logged-in user doesn't already have a profile
#         if ClientProfile.objects.filter(user=request.user).exists():  # Change: Check if profile exists for user
#             return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)  # Comment: Handle if profile already exists

#         # Create a new profile for the logged-in user
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             # serializer.save(user=request.user)
#             serializer.save(user=request.user, user_type=request.user.user_type)  # Change: Ensure user_type is saved

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Comment: Handle serializer errors




class ProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Apply IsAuthenticated permission globally

    parser_classes = [MultiPartParser]  # Enable MultiPartParser to handle file uploads
    
    def get_object(self):
        # Fetch profile based on logged-in user
        profile = get_object_or_404(ClientProfile, user=self.request.user)  # Modified to fetch profile by user
        return profile

    def get(self, request):
        # Retrieve profile based on logged-in user
        profile = self.get_object()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # def put(self, request):
    #     # Update profile based on logged-in user
    #     profile = self.get_object()
    #     serializer = ProfileSerializer(profile, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    

    # Other methods (get, delete) remain unchanged

    def put(self, request):
        try:
            profile = ClientProfile.objects.get(user=request.user)
        except ClientProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            # Handle image upload/update
            # if 'image' in request.data:
            #     # Delete previous image if updating
            #     if profile.image:
            #         profile.image.delete()

            #     # Save new image and update URL
            #     image = request.data.get('image')
            #     profile.image = image
            #     profile.image = f'https://storage.googleapis.com/storyvord-profile/{profile.image.name}'  # Update the image URL

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Delete profile based on logged-in user
        profile = self.get_object()
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
