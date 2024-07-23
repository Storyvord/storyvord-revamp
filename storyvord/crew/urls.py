from django.urls import path
from .views import *

urlpatterns = [
    path('crew-profile/', CrewProfileView.as_view(), name='crew-profile'),
    
    # Crew Credits CRUD api
    path('crew-credits/', CrewCreditsListCreateView.as_view(), name='crew-credits-list-create'),
    path('crew-credits/<int:pk>/', CrewCreditsDetailView.as_view(), name='crew-credits-detail'),
    
    # Crew Education CRUD api
    path('crew-education/', CrewEducationListCreateView.as_view(), name='crew-education-list-create'),
    path('crew-education/<int:pk>/', CrewEducationDetailView.as_view(), name='crew-education-detail'),
    
    # Crew rate
    path('crew-rate/', CrewRateListCreateView.as_view(), name='crew-rate-list-create'),
    path('crew-rate/<int:pk>/', CrewRateDetailView.as_view(), name='crew-rate-detail'),
    
    path('endorsement-from-peers/', EndorsementfromPeersListCreateView.as_view(), name='endorsement-from-peers-list-create'),
    path('endorsement-from-peers/<int:pk>/', EndorsementfromPeersDetailView.as_view(), name='endorsement-from-peers-detail'),
    
    path('social-links/', SocialLinksListCreateView.as_view(), name='social-links-list-create'),
    path('social-links/<int:pk>/', SocialLinksDetailView.as_view(), name='social-links-detail'),

    path('crew-list/', CrewListView.as_view(), name='crew-list'),
]
