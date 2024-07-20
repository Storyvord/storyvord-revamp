# urls.py
from django.urls import path
from .views import AnnouncementListCreateAPIView

urlpatterns = [
    path('announcements/', AnnouncementListCreateAPIView.as_view(), name='announcement-list-create')
]
