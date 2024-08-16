from django.urls import path

# client/urls.py
from .views import *

urlpatterns = [
    # path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/detail/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('switch-profile/', SwitchProfileView.as_view(), name='switch-profile'),
    path('folders/', ClientCompanyFolderView.as_view(), name='client_company_folder_list_create'),
    path('folders/<int:pk>/', ClientCompanyFolderUpdateView.as_view(), name='client-company-folder-update'),
    path('folders/<int:folder_id>/files/', ClientCompanyFileView.as_view(), name='client_company_file_list_create'),
    path('folders/files/<int:pk>/', ClientCompanyFileUpdateView.as_view(), name='client-company-file-update'),
    
    # calendars
    path('company-calendar/events/', ClientCompanyEventAPIView.as_view(), name='event-list-create'),
    path('company-calendar/events/<int:event_id>/', ClientCompanyEventAPIView.as_view(), name='event-detail'),
]
