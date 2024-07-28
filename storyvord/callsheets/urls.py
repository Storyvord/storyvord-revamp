# urls.py file ->

from django.urls import path
from .views import CallSheetCreateView, CallSheetRetrieveUpdateDeleteView

urlpatterns = [
    path('callsheets/', CallSheetCreateView.as_view(), name='callsheet-create'),
    path('callsheets/<int:pk>/', CallSheetRetrieveUpdateDeleteView.as_view(), name='callsheet-detail'),
]