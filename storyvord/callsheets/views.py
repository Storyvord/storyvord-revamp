

# Create your views here.
# callsheets/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.models import CallSheet
from.serializers import CallSheetSerializer
from django.shortcuts import render

class CallSheetListView(APIView):
    def get(self, request):
        callsheets = CallSheet.objects.all()
        serializer = CallSheetSerializer(callsheets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CallSheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CallSheetDetailView(APIView):
    def get_object(self, pk):
        try:
            return CallSheet.objects.get(pk=pk)
        except CallSheet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        callsheet = self.get_object(pk)
        serializer = CallSheetSerializer(callsheet)
        return Response(serializer.data)

    def put(self, request, pk):
        callsheet = self.get_object(pk)
        serializer = CallSheetSerializer(callsheet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        callsheet = self.get_object(pk)
        callsheet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)