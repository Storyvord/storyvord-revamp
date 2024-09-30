from django.urls import path
from .views import * 

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    # Crew Profile
    path('crew/active-profile/', CrewActiveProfileView.as_view(), name='crew-active-profile'),
    path('crew/inactive-profile/', CrewInActiveProfileView.as_view(), name='crew-inactive-profile'),
    path('crew/update-active-profile/', CrewUpdateActiveProfileView.as_view(), name='crew-update-active-profile'),

    path('crew/verified-portfolio/', CrewVerifiedPortfolioView.as_view(), name='crew-verified-portfolio'),
    path('crew/nonverified-portfolio/', CrewNonVerifiedPortfolioView.as_view(), name='crew-nonverified-portfolio'),
    path('crew/update-verified-portfolio/', CrewUpdateVerifiedPortfolioView.as_view(), name='crew-update-verified-portfolio'),

    # path('crew/social-links/', CrewSocialLinksView.as_view(), name='crew-social-links'),

    path('crew/list/', CrewListView.as_view(), name='crew-profile'),
    path('crew/list/<int:pk>/', CrewListView.as_view(), name='crew-profile'),
]