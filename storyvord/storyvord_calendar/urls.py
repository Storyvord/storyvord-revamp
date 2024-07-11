from django.urls import path
from .views import CalendarView, EventView

urlpatterns = [
    path('calendars/', CalendarView.as_view(), name='calendar-list'),
    path('calendars/<int:pk>/', CalendarView.as_view(), name='calendar-detail'),
    path('calendars/<int:calendar_id>/events/', EventView.as_view(), name='event-list-create'),
    path('calendars/<int:calendar_id>/events/<int:pk>/', EventView.as_view(), name='event-detail'),
]
