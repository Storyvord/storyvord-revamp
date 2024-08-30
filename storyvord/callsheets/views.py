from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CallSheet
from .serializers import CallSheetSerializer
from project.models import Project

class CallSheetListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        callsheets = CallSheet.objects.filter(project=project_id)
        serializer = CallSheetSerializer(callsheets, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        data = request.data.copy()
        data['project'] = project.project_id

        serializer = CallSheetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CallSheetDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        call_sheet = get_object_or_404(CallSheet, pk=pk)
        serializer = CallSheetSerializer(call_sheet)
        return Response(serializer.data)

    def put(self, request, pk):
        call_sheet = get_object_or_404(CallSheet, pk=pk)
        serializer = CallSheetSerializer(call_sheet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        call_sheet = get_object_or_404(CallSheet, pk=pk)
        call_sheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)