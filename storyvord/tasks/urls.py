# urls.py

from django.urls import path
from .views import *

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
