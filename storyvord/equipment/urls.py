# equipment/urls.py
from django.urls import path
from .views import (
    EquipmentCategoryListAPIView,
    EquipmentModelListAPIView,
    EquipmentInstanceListAPIView,
    EquipmentInstanceDetailAPIView,
    EquipmentLogListAPIView,
    EquipmentLogDetailAPIView,
)

urlpatterns = [
    path('categories/', EquipmentCategoryListAPIView.as_view(), name='equipment-category-list'),
    path('models/', EquipmentModelListAPIView.as_view(), name='equipment-model-list'),
    path('instances/', EquipmentInstanceListAPIView.as_view(), name='equipment-instance-list'),
    path('instances/<int:pk>/', EquipmentInstanceDetailAPIView.as_view(), name='equipment-instance-detail'),
    path('logs/', EquipmentLogListAPIView.as_view(), name='equipment-log-list'),
    path('logs/<int:pk>/', EquipmentLogDetailAPIView.as_view(), name='equipment-log-detail'),
]
