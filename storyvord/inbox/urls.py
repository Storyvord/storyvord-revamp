from django.urls import path
from .views import DialogListView, DialogMessagesView, SendMessageView, MarkAsReadView

urlpatterns = [
    path('dialogs/', DialogListView.as_view(), name='dialog-list'),
    path('dialogs/<int:user_id>/messages/', DialogMessagesView.as_view(), name='dialog-messages'),
    path('dialogs/<int:user_id>/messages/send/', SendMessageView.as_view(), name='send-message'),
    path('messages/<int:message_id>/read/', MarkAsReadView.as_view(), name='mark-as-read'),
]
