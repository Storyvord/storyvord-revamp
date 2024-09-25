from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('old-register/', RegisterNewView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/user/me/', AuthUserDetailView.as_view(), name='auth-user-detail'),
    
    # password reset
    path('request-reset-password/', RequestPasswordResetEmailAPIView.as_view(), name="request-reset-password"),
    path('reset-password/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('reset-password-complete/', NewPasswordSetAPIView.as_view(), name='password-reset-complete'),
    path('password-change/', UserChangePasswordAPIView.as_view(),name='change-password'),
    
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

    path('register/onboard/', SelectUserType.as_view(), name='user-usertype-onboard'),

    path('google/', google_custom_login_redirect, name='google-login'),
]
