from django.urls import path
from .views import *

urlpatterns = [
    path('dialogs/', DialogListView.as_view(), name='dialog-list'),
    path('dialogs/<int:user_id>/messages/', DialogMessagesView.as_view(), name='dialog-messages'),
    path('dialogs/<int:user_id>/messages/send/', SendMessageView.as_view(), name='send-message'),
    path('messages/<int:message_id>/read/', MarkAsReadView.as_view(), name='mark-as-read'),
    
    path('groups/', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groups/<int:group_id>/add_member/', GroupAddMemberAPIView.as_view(), name='group-add-member'),
    path('groups/<int:group_id>/remove_member/', GroupRemoveMemberAPIView.as_view(), name='group-remove-member'),
    path('groups/<int:group_id>/messages/', MessageListCreateAPIView.as_view(), name='message-list-create'),
]
