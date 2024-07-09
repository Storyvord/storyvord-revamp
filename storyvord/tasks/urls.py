# urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('projects/<int:project_pk>/tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    
    # complete approval apis
    path('tasks/<int:pk>/request-completion/', TaskCompletionRequestView.as_view(), name='task-request-completion'),
    path('tasks/<int:pk>/approve-completion/', TaskCompletionApprovalView.as_view(), name='task-approve-completion'),
]
