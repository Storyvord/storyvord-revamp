from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import FileSerializer
from .models import File
from accounts.models import User
from django.shortcuts import get_object_or_404

# Create your views here.

class FileListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        files = File.objects.filter(allowed_users=request.user)

        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        if user.user_type != 'crew':
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Make sure the user who is creating the file is in the list of allowed
        request.data['allowed_users'] += [user.id]

        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class FileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        file = get_object_or_404(File, pk=pk)

        # Who can view a file?
        if not file.is_crew_user_allowed(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = FileSerializer(file)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        file = get_object_or_404(File, pk=pk)

        # Who can delete a file?
        if not file.is_crew_user_allowed(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)

        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        file = get_object_or_404(File, pk=pk)

        # Who can update a file?
        if not file.is_crew_user_allowed(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if 'allowed_users' in request.data:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'You cannot update allowed_users field. Use "add_users" and "remove_users" fields instead.'})

        # Add additional users if 'add_users' is provided in request
        if 'add_users' in request.data:
            add_users_ids = request.data.pop('add_users')
            for user_id in add_users_ids:
                file.allowed_users.add(user_id)

        # Remove users if 'remove_users' is provided in request
        if 'remove_users' in request.data:
            remove_users_ids = request.data.pop('remove_users')
            for user_id in remove_users_ids:
                file.allowed_users.remove(user_id)
        
        # Make sure the user who is updating the file is in the list of allowed
        if request.user not in file.allowed_users.all():
            file.allowed_users.add(request.user)

        serializer = FileSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)