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
    
    path('endorsement-from-peers/', EndorsementfromPeersListCreateView.as_view(), name='endorsement-from-peers-list-create'),
    path('endorsement-from-peers/<int:pk>/', EndorsementfromPeersDetailView.as_view(), name='endorsement-from-peers-detail'),
    
    path('social-links/', SocialLinksListCreateView.as_view(), name='social-links-list-create'),
    path('social-links/<int:pk>/', SocialLinksDetailView.as_view(), name='social-links-detail'),

    path('crew-list/', CrewListView.as_view(), name='crew-list'),
    
    # Crew Portfolio and its verification Urls
    path('portfolios/', CrewPortfolioListCreate.as_view(), name='crew-portfolio-list-create'),
    path('portfolios/<int:pk>/', CrewPortfolioDetail.as_view(), name='crew-portfolio-detail'),
    
    path('verify/client_reference/<int:pk>/', VerifyClientReference.as_view(), name='verify-client-reference'),
    path('verify/imbd_link/<int:pk>/', VerifyImbdLink.as_view(), name='verify-imbd-link'),
    path('verify/work_sample/<int:pk>/', VerifyWorkSample.as_view(), name='verify-work-sample'),
    path('verify/email_agreement/<int:pk>/', VerifyEmailAgreement.as_view(), name='verify-email-agreement'),
    
    # All projects
    path('my-projects/', UserProjectsView.as_view(), name='user_projects'),
    path('company-projects/', CompanyProjectsView.as_view(), name='company_projects'),

    
    # skills/services and location
    path('crew-profile/search/', CrewProfileSearchView.as_view(), name='crew-profile-search'),
]
