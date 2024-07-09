from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import FileSerializer
from .models import File
from django.shortcuts import get_object_or_404

# Create your views here.

class FileListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        if(File.is_crew_user_allowed(request.user)):
            files = File.objects.filter(allowed_users=request.user)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if not File.is_crew_user_allowed(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = get_object_or_404(File, pk=pk)

        # Who can delete a file?
        if not File.is_crew_user_allowed(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)

        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        file = get_object_or_404(File, pk=pk)

        # Who can update a file?
        if not File.is_crew_user_allowed(request.user):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = FileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)