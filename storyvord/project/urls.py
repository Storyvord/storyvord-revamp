from django.urls import path
from .views import *


urlpatterns = [
    # Projects
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    
    path('onboard-requests/send/', SendOnboardRequestView.as_view(), name='send-onboard-request'),
    path('onboard-requests/<int:pk>/update/', UpdateOnboardRequestView.as_view(), name='update-onboard-request'),
    path('onboard-requests/pending/', PendingOnboardRequestsView.as_view(), name='pending_onboard_requests'),
    
    path('<str:project_id>/onboard-requests/', OnboardRequestsByProjectView.as_view(), name='onboard_requests_by_project'),
]
