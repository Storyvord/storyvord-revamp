from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from project.serializers.serializers_v1 import UserSerializer
from .models import File, Folder
from accounts.models import User
from project.models import Project
from django.shortcuts import get_object_or_404
from django.db.models import Q
from storyvord.exception_handlers import custom_exception_handler

# Create your views here.

class FolderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderSerializer
    # parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk, format=None):
        try:
            user = request.user
            folders = Folder.objects.filter(
                Q(project=pk) & (Q(allowed_users=user) | Q(default=True))
            ).distinct()
            serializer = FolderSerializer(folders, many=True, context={'exclude_files': True})
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def post(self, request, pk, format=None):
        try:
            data = request.data.copy()
            data['project'] = pk

            serializer = FolderSerializer(data=data, context={'request': request})
            serializer.is_valid(exception=True)
            serializer.save()
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

class FolderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FolderUpdateSerializer
    
    def put(self, request, pk, format=None):
        try:
            folder = get_object_or_404(Folder, pk=pk)
            serializer = self.serializer_class(folder, data=request.data, context={'request': request}, partial=True)
        
            serializer.is_valid(exception=True)
            serializer.save()
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data)
        
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response


class FileListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer

    # Get the list of files in a folder
    def get(self, request, pk, format=None):
        try:
            folder = get_object_or_404(Folder, pk=pk)
            if not folder.allowed_users.filter(id=request.user.id).exists() and folder.default == False:
                return Response(status=status.HTTP_403_FORBIDDEN)

            files = folder.files

            serializer = FileSerializer(files, many=True)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def post(self, request, pk, format=None):
        try:
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
            serializer.is_valid(exception=True)
            serializer.save()
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

class FileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer

    # Get the details of a file
    def get(self, request, pk, format=None):
        try:
            file = get_object_or_404(File, pk=pk)

            # Who can view a file?
            if not file.folder.allowed_users.filter(id=request.user.id).exists():
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = FileSerializer(file)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response
    
    def delete(self, request, pk, format=None):
        try:
            file = get_object_or_404(File, pk=pk)

            # Who can delete a file?
            if not file.folder.project.user == request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response


    def put(self, request, pk, format=None):
        try:
            file = get_object_or_404(File, pk=pk)

            # Who can update a file?
            if not file.folder.project.user == request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Ensure the folder id doesnot change
            if 'folder' in request.data:
                return Response(status=status.HTTP_403_FORBIDDEN, data={'status': False,
                                                                        'code': status.HTTP_403_FORBIDDEN,
                                                                        'message': 'You cannot change the folder of a file.'})

            serializer = FileSerializer(file, data=request.data, partial=True)
            serializer.is_valid(exception=True)
            serializer.save()
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

class FolderCrewListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            folder = get_object_or_404(Folder, pk=pk)
            if not folder.project.user == request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            crew = folder.project.crew_profiles.all()
            serializer = UserSerializer(crew, many=True)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response


# Crew side file view 

class AccessibleFileListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer

    def get(self, request, format=None):
        try:
            user = request.user
            files = File.objects.filter(allowed_users=user)
            serializer = FileSerializer(files, many=True)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

class AccessibleFileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FileSerializer

    def get(self, request, pk, format=None):
        try:
            file = File.objects.get(pk=pk)

            if not file.allowed_users.filter(id=request.user.id).exists():
                return Response({'status': False,
                                 'code': status.HTTP_403_FORBIDDEN,
                                 "message": "You do not have permission to access this file."}, status=status.HTTP_403_FORBIDDEN)

            serializer = FileSerializer(file)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response