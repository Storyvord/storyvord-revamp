from django.urls import path

# client/urls.py
from .views import ProfileAPIView, ProfileDetailAPIView

urlpatterns = [
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/detail/', ProfileDetailAPIView.as_view(), name='profile-detail'),
]
