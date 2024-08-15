from django.urls import path
from .views import AddCrewToProjectView, AcceptInvitationView, RejectInvitationView, RegisterWithReferralView

urlpatterns = [
    path('projects/add-crew/', AddCrewToProjectView.as_view(), name='add-crew-to-project'),
    path('invitations/accept/', AcceptInvitationView.as_view(), name='accept-invitation'),
    path('invitations/reject/', RejectInvitationView.as_view(), name='reject-invitation'),
    path('register-with-referral/', RegisterWithReferralView.as_view(), name='register-with-referral'),
]
