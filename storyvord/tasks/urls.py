# urls.py

from django.urls import path , include
from .views.views_v1 import *
from .views.views_v2 import ProjectTaskViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('projects/<str:project_pk>/tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    
    # complete approval apis
    path('tasks/<int:pk>/request-completion/', TaskCompletionRequestView.as_view(), name='task-request-completion'),
    path('tasks/<int:pk>/approve-completion/', TaskCompletionApprovalView.as_view(), name='task-approve-completion'),
    path('tasks/pending-approvals/<str:project_pk>/', TaskPendingToApprovalView.as_view(), name='pending-task-approvals'),
    
    # Crew side tasks
    path('crew/tasks/', CrewTaskListView.as_view(), name='crew-task-list'),
    path('crew/tasks/<int:pk>/', CrewTaskDetailView.as_view(), name='crew-task-detail'),
]

router = DefaultRouter()

# Register viewsets with the router
router.register(r'tasks', ProjectTaskViewSet, basename='projecttask')

urlpatterns += [
    path('v2/', include(router.urls)),
]
