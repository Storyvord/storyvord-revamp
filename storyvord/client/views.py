# client/views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


from crew.models import CrewProfile
from .models import *
from .serializers import *
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

    # parser_classes = [MultiPartParser]  # Enable MultiPartParser to handle file uploads
    serializer_class = ProfileSerializer
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
    
    def put(self, request):
        # Update profile based on logged-in user
        profile = self.get_object()
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    

    # Other methods (get, delete) remain unchanged

    # def put(self, request):
    #     try:
    #         profile = ClientProfile.objects.get(user=request.user)
    #     except ClientProfile.DoesNotExist:
    #         return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = ProfileSerializer(profile, data=request.data)
    #     if serializer.is_valid():
    #         # Handle image upload/update
    #         # if 'image' in request.data:
    #         #     # Delete previous image if updating
    #         #     if profile.image:
    #         #         profile.image.delete()

    #         #     # Save new image and update URL
    #         #     image = request.data.get('image')
    #         #     profile.image = image
    #         #     profile.image = f'https://storage.googleapis.com/storyvord-profile/{profile.image.name}'  # Update the image URL

    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Delete profile based on logged-in user
        profile = self.get_object()
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SwitchProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        data = request.data
        switch_to_client = data.get('switch_to_client', False)
        switch_to_crew = data.get('switch_to_crew', False)

        if not (switch_to_client or switch_to_crew):
            return Response({'detail': 'Specify a role to switch to.'}, status=status.HTTP_400_BAD_REQUEST)

        if switch_to_client:
            # Activate Client profile and deactivate Crew profile
            client_profile, created = ClientProfile.objects.get_or_create(user=user)
            client_profile.active = True
            client_profile.save()

            CrewProfile.objects.filter(user=user).update(active=False)

            user.is_client = True
            user.is_crew = False
            user.save()

        if switch_to_crew:
            # Activate Crew profile and deactivate Client profile
            crew_profile, created = CrewProfile.objects.get_or_create(user=user)
            crew_profile.active = True
            crew_profile.save()

            ClientProfile.objects.filter(user=user).update(active=False)

            user.is_client = False
            user.is_crew = True
            user.save()

        return Response({'detail': 'Profile updated successfully.'}, status=status.HTTP_200_OK)



class ClientCompanyFolderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        folders = ClientCompanyFolder.objects.filter(allowed_users=user).distinct()
        serializer = ClientCompanyFolderSerializer(folders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClientCompanyFolderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete folders?

class ClientCompanyFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, folder_id, format=None):
        folder = get_object_or_404(ClientCompanyFolder, pk=folder_id, allowed_users=request.user)
        files = folder.files.all()
        serializer = ClientCompanyFileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, folder_id, format=None):
        folder = get_object_or_404(ClientCompanyFolder, pk=folder_id, allowed_users=request.user)
        data = request.data.copy()
        data['folder'] = folder.id
        serializer = ClientCompanyFileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Delete files?

class ClientCompanyFileUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return ClientCompanyFile.objects.get(pk=pk)
        except ClientCompanyFile.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        if file is None:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCompanyFileUpdateSerializer(file, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        if file is None:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCompanyFileUpdateSerializer(file, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        file = self.get_object(pk)
        if file is None:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCompanyFileUpdateSerializer(file, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        if file is None:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        if file.folder.created_by != request.user:
            return Response({'detail': 'You do not have permission to delete this file.'}, status=status.HTTP_403_FORBIDDEN)

        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class ClientCompanyFolderUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return ClientCompanyFolder.objects.get(pk=pk)
        except ClientCompanyFolder.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        folder = self.get_object(pk)
        if folder is None:
            return Response({'detail': 'Folder not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCompanyFolderUpdateSerializer(folder)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        folder = self.get_object(pk)
        if folder is None:
            return Response({'detail': 'Folder not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCompanyFolderUpdateSerializer(folder, data=request.data, context={'request': request})
        if serializer.is_valid():
            self.check_object_permissions(request, folder)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        folder = self.get_object(pk)
        if folder is None:
            return Response({'detail': 'Folder not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCompanyFolderUpdateSerializer(folder, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            self.check_object_permissions(request, folder)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def check_object_permissions(self, request, obj):
        # Custom permission check
        if obj.created_by != request.user:
            self.permission_denied(request, message="You do not have permission to edit this folder.")
            
# Calendar


class ClientCompanyEventAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientCompanyEventSerializer
    def get(self, request, event_id=None):
        if event_id:
            try:
                event = ClientCompanyEvent.objects.get(id=event_id, calendar__company__user=request.user)
                serializer = ClientCompanyEventSerializer(event)
                return Response(serializer.data)
            except ClientCompanyEvent.DoesNotExist:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            company_profile = ClientCompanyProfile.objects.get(user=request.user)
            print("Company prodile", company_profile)
            events = ClientCompanyEvent.objects.filter(calendar__company=company_profile)
            serializer = ClientCompanyEventSerializer(events, many=True)
            return Response(serializer.data)
        except ClientCompanyProfile.DoesNotExist:
            return Response({"error": "Company profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ClientCompanyEventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, event_id):
        try:
            event = ClientCompanyEvent.objects.get(id=event_id, calendar__company__user=request.user)
        except ClientCompanyEvent.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientCompanyEventSerializer(event, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id):
        try:
            event = ClientCompanyEvent.objects.get(id=event_id, calendar__company__user=request.user)
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClientCompanyEvent.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)