from django.urls import path
from .views import *


urlpatterns = [
    # Projects
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    
    # Onbaord
    # path('projects/<uuid:project_id>/onboard-request/<int:crew_id>/', SendOnboardRequestAPIView.as_view(), name='send-onboard-request'),
    # path('onboard-requests/', ListOnboardRequestsAPIView.as_view(), name='list-onboard-requests'),
    # path('onboard-requests/<int:request_id>/accept/', AcceptOnboardRequestAPIView.as_view(), name='accept-onboard-request'),
    
    path('onboard-requests/send/', SendOnboardRequestView.as_view(), name='send-onboard-request'),
    path('onboard-requests/<int:pk>/update/', UpdateOnboardRequestView.as_view(), name='update-onboard-request'),
]
