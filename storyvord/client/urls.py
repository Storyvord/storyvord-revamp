from django.urls import path

# client/urls.py
from .views import *

urlpatterns = [
    # path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/detail/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('switch-profile/', SwitchProfileView.as_view(), name='switch-profile'),
]
