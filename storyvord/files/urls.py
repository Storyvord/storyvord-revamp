from django.urls import path
from .views import * 

urlpatterns = [
    # Path for getting the list of files and creating a new file
    path('', FileListCreateView.as_view(), name='file-list-create'),
    # Path for deleting a file by its primary key (pk)
    path('<int:pk>/', FileDetailView.as_view(), name='file-delete'),
]