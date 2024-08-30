# urls.py file ->

from django.urls import path
from .views import *

urlpatterns = [
    path('<str:project_id>/', CallSheetListAPIView.as_view(), name='callsheet-create'),
    path('details/<int:pk>/', CallSheetDetailAPIView.as_view(), name='callsheet-detail'),
]