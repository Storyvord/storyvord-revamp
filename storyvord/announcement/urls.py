# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('announcements/', AnnouncementListCreateAPIView.as_view(), name='announcement-list-create'),
    path('announcements/<int:pk>/', AnnouncementRetrieveUpdateDestroyAPIView.as_view(), name='announcement-detail'),
    
    path('recipients/announcements/', RecipientAnnouncementListAPIView.as_view(), name='recipient-announcement-list'),
    path('recipients/announcements/<int:pk>/', RecipientAnnouncementDetailAPIView.as_view(), name='recipient-announcement-detail'),
]
