# urls.py file ->

from django.urls import path
from .views import *

urlpatterns = [
    path('<str:project_id>/', CallSheetListAPIView.as_view(), name='callsheet-create'),
    path('details/<int:pk>/', CallSheetDetailAPIView.as_view(), name='callsheet-detail'),

    path('geolocation/address/', GeoapifyGeocodeView.as_view(), name='weather-list'),
    path('geolocation/nearest-places/', GeoapifyNearestPlaceView.as_view(), name='nearest-list'),
    path('weather/current/', WeatherCurrentInfoView.as_view(), name='weather-info'),
    path('weather/future/', WeatherFutureInfoView.as_view(), name='weather-info'),
    
    path('crew-details/<int:pk>/', CallSheetCrewDetails.as_view(), name='crew-details'),
]