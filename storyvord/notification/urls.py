# urls.py
from django.urls import path
from .views import * 

urlpatterns = [
    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),
    path('notifications/unread-count/', UnreadNotificationCountAPIView.as_view(), name='unread-notification-count'),
]
