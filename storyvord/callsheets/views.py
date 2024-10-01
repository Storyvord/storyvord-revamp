from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CallSheet
from .serializers import *
from project.models import Project
import requests
from django.http import JsonResponse
from django.conf import settings
from client.models import ClientProfile
from crew.models import CrewProfile

class CallSheetListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, project_id):
        callsheets = CallSheet.objects.filter(project=project_id, allowed_users=request.user)
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
        if request.user not in call_sheet.allowed_users.all():
            return Response({'error': 'You do not have permission to view this call sheet.'}, status=status.HTTP_403_FORBIDDEN)
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

        
class CallSheetCrewDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        crew_profile = get_object_or_404(CrewProfile, pk=pk)
        serializer = CrewProfileSerializer(crew_profile)
        return Response(serializer.data)

        
# https://www.geoapify.com/tutorial/geocoding-python/
class GeoapifyGeocodeView(APIView):
    def get(self, request):
        api_key = getattr(settings, 'GEOAPIFY_API_KEY')
        address = request.GET.get('text')

        url = f"https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={api_key}"

        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            return JsonResponse(response.json())
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

class GeoapifyNearestPlaceView(APIView):
    def get(self, request):
        api_key = getattr(settings, 'GEOAPIFY_API_KEY')
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')


        url = f"https://api.geoapify.com/v1/places?categories=city&filter=circle:{longitude},{latitude},1000&limit=1&apiKey={api_key}"

        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            return JsonResponse(response.json())
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

            
# https://www.weatherapi.com/docs/
class WeatherCurrentInfoView(APIView):
    def get(self, request):
        # Extract the latitude and longitude from the query parameters
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')
        
        if not latitude or not longitude:
            return JsonResponse({'error': 'Latitude and Longitude are required.'}, status=400)
        
        api_key = getattr(settings, 'WEATHERAPI_API_KEY')
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}"

        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            return JsonResponse(response.json())
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

class WeatherFutureInfoView(APIView):
    def get(self, request):
        # Extract the latitude and longitude from the query parameters
        latitude = request.GET.get('lat')
        longitude = request.GET.get('lon')
        dt = request.GET.get('dt')
        
        if not latitude or not longitude:
            return JsonResponse({'error': 'Latitude and Longitude are required.'}, status=400)
        
        api_key = getattr(settings, 'WEATHERAPI_API_KEY')
        url = f"http://api.weatherapi.com/v1/future.json?key={api_key}&q={latitude},{longitude}&dt={dt}"

        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
            return JsonResponse(response.json())
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)