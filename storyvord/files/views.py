from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from project.serializers.v1.serializers import UserSerializer
from .models import File, Folder
from accounts.models import User
from project.models import Project
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

class FolderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderSerializer
    # parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk, format=None):
        user = request.user
        folders = Folder.objects.filter(
            Q(project=pk) & (Q(allowed_users=user) | Q(default=True))
        ).distinct()
        serializer = FolderSerializer(folders, many=True, context={'exclude_files': True})
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        data = request.data.copy()
        data['project'] = pk

        serializer = FolderSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FolderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderUpdateSerializer
    
    def put(self, request, pk, format=None):
        folder = get_object_or_404(Folder, pk=pk)
        serializer = self.serializer_class(folder, data=request.data, context={'request': request}, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer

    # Get the list of files in a folder
    def get(self, request, pk, format=None):
        folder = get_object_or_404(Folder, pk=pk)
        if not folder.allowed_users.filter(id=request.user.id).exists() and folder.default == False:
            return Response(status=status.HTTP_403_FORBIDDEN)

        files = folder.files

        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        user = request.user

        folder = get_object_or_404(Folder, pk=pk)
        
        if user != folder.project.user and user != folder.created_by:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Check if the file with same name exists
        if File.objects.filter(folder=pk, name=request.data.get('name')).exists():
            return Response({"detail": "File with the same name already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Make a mutable copy of request.data
        data = request.data.copy()
        data['folder'] = pk

        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer

    # Get the details of a file
    def get(self, request, pk, format=None):
        file = get_object_or_404(File, pk=pk)

        # Who can view a file?
        if not file.folder.allowed_users.filter(id=request.user.id).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = FileSerializer(file)
        return Response(serializer.data)
    
    def delete(self, request, pk, format=None):
        file = get_object_or_404(File, pk=pk)

        # Who can delete a file?
        if not file.folder.project.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        file = get_object_or_404(File, pk=pk)

        # Who can update a file?
        if not file.folder.project.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # Ensure the folder id doesnot change
        if 'folder' in request.data:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'You cannot change the folder of a file.'})

        serializer = FileSerializer(file, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

class FolderCrewListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        folder = get_object_or_404(Folder, pk=pk)
        if not folder.project.user == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        crew = folder.project.crew_profiles.all()
        serializer = UserSerializer(crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Crew side file view 

class AccessibleFileListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        files = File.objects.filter(allowed_users=user)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AccessibleFileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            file = File.objects.get(pk=pk)
        except File.DoesNotExist:
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

        if not file.allowed_users.filter(id=request.user.id).exists():
            return Response({"error": "You do not have permission to access this file."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FileSerializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)