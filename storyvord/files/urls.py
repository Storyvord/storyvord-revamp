from django.urls import path
from .views import * 

urlpatterns = [
    # Path for getting the list of files and creating a new file in a folder
    path('folders/files/<int:pk>/', FileListCreateView.as_view(), name='file-list-create'),
    # Path for deleting a file by its primary key (pk)
    path('<int:pk>/', FileDetailView.as_view(), name='file-delete'),
    
    # crew side list and detail
    
    path('crew/files/', AccessibleFileListView.as_view(), name='file-list'),
    path('crew/files/<int:pk>/', AccessibleFileDetailView.as_view(), name='file-detail'),

    path('crew/folders/<str:pk>/', FolderListView.as_view(), name='folder-list-create'),
]