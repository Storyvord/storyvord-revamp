# equipment/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import EquipmentCategory, EquipmentModel, EquipmentInstance, EquipmentLog
from .serializers import EquipmentCategorySerializer, EquipmentModelSerializer, EquipmentInstanceSerializer, EquipmentLogSerializer
from django.shortcuts import get_object_or_404

class EquipmentCategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = EquipmentCategory.objects.all()
        serializer = EquipmentCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
         # Check if the data is a list
        if isinstance(request.data, list):
            serializer = EquipmentCategorySerializer(data=request.data, many=True)  # <-- Add this line
        else:
         serializer = EquipmentCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentModelListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        models = EquipmentModel.objects.all()
        serializer = EquipmentModelSerializer(models, many=True)
        return Response(serializer.data)

    def post(self, request):
          # Check if the data is a list
        if isinstance(request.data, list):
            serializer = EquipmentModelSerializer(data=request.data, many=True)  # <-- Add this line
        else:
         serializer = EquipmentModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentInstanceListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        instances = EquipmentInstance.objects.all()
        serializer = EquipmentInstanceSerializer(instances, many=True)
        return Response(serializer.data)

    def post(self, request):
         # Check if the data is a list
        if isinstance(request.data, list):
            serializer = EquipmentInstanceSerializer(data=request.data, many=True)  # <-- Add this line
        else:
         serializer = EquipmentInstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentInstanceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(EquipmentInstance, pk=pk)

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = EquipmentInstanceSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = EquipmentInstanceSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = EquipmentInstanceSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EquipmentLogListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = EquipmentLog.objects.all()
        serializer = EquipmentLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
         # Check if the data is a list
        if isinstance(request.data, list):
            serializer = EquipmentLogSerializer(data=request.data, many=True)  # <-- Add this line
        else:
         serializer = EquipmentLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EquipmentLogDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(EquipmentLog, pk=pk)

    def get(self, request, pk):
        log = self.get_object(pk)
        serializer = EquipmentLogSerializer(log)
        return Response(serializer.data)

    def put(self, request, pk):
        log = self.get_object(pk)
        serializer = EquipmentLogSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        log = self.get_object(pk)
        serializer = EquipmentLogSerializer(log, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        log = self.get_object(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
