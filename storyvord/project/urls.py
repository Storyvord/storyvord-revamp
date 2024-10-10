from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views.v1.views import *
from .views.v2.views import *

urlpatterns = [
    # Projects
    path('projects/onboard/', ProjectOnboardView.as_view(), name='project-onboard'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<uuid:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    
    path('onboard-requests/send/', SendOnboardRequestView.as_view(), name='send-onboard-request'),
    path('onboard-requests/<int:pk>/update/', UpdateOnboardRequestView.as_view(), name='update-onboard-request'),
    path('onboard-requests/pending/', PendingOnboardRequestsView.as_view(), name='pending_onboard_requests'),
    
    path('<str:project_id>/onboard-requests/', OnboardRequestsByProjectView.as_view(), name='onboard_requests_by_project'),

    path('crew/<str:project_id>/', CrewListView.as_view(), name='crew-list'),
]

router = DefaultRouter()

# Register viewsets with the router
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-requirements', ProjectRequirementsViewSet, basename='project-requirements')
router.register(r'shooting-details', ShootingDetailsViewSet, basename='shooting-details')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'memberships', MembershipViewSet, basename='memberships')

urlpatterns += [
    path('v2/', include(router.urls)),
]