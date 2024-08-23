from django.urls import path
from .views import *

urlpatterns = [
    path('address-book/', AddressBookAPIView.as_view(), name='addressbook-list-create'),
    path('address-book/<int:pk>/', AddressBookAPIView.as_view(), name='addressbook-detail'),

    # Company Task
    path('employees/', EmployeeListView.as_view(), name='employee-list'),

    path('tasks/', CompanyTaskListCreateAPIView.as_view(), name='company-task-list-create'),
    path('tasks/<int:pk>/', CompanyTaskDetailAPIView.as_view(), name='company-task-detail'),
    
    path('tasks/<int:pk>/request-completion/', TaskCompletionRequestView.as_view(), name='company-task-request-completion'),
    path('tasks/<int:pk>/approve-completion/', TaskCompletionApprovalView.as_view(), name='company-task-approve-completion'),
    path('tasks/pending-approvals/', TaskPendingToApprovalView.as_view(), name='pending-company-task-approvals'),
    
    path('employee/tasks/', EmployeeTaskListView.as_view(), name='employee-task-list'),
    path('employee/tasks/<int:pk>/', EmployeeTaskDetailView.as_view(), name='employee-task-detail'),
    
]
