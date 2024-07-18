# callsheets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CallSheetListView.as_view(), name='callsheet_list'),
    path('<int:pk>/', views.CallSheetDetailView.as_view(), name='callsheet_detail'),
]