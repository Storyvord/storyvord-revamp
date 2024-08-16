from django.urls import path
from .views import AddressBookAPIView

urlpatterns = [
    path('address-book/', AddressBookAPIView.as_view(), name='addressbook-list-create'),
    path('address-book/<int:pk>/', AddressBookAPIView.as_view(), name='addressbook-detail'),
]
