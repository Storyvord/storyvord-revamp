from django.urls import path
from .views.v1.views import *
from .views.v2.auth_views import RegisterViewV2
from .views.v2.auth_views import LoginViewV2
from .views.v2.email_verification import VerifyEmail as VerifyEmailV2
from .views.v2.profile_views import *


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('old-register/', RegisterNewView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # password reset
    path('request-reset-password/', RequestPasswordResetEmailAPIView.as_view(), name="request-reset-password"),
    path('reset-password/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('reset-password-complete/', NewPasswordSetAPIView.as_view(), name='password-reset-complete'),
    path('password-change/', UserChangePasswordAPIView.as_view(),name='change-password'),
    
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

    path('register/onboard/', SelectUserType.as_view(), name='user-usertype-onboard'),

    path('google/', google_custom_login_redirect, name='google-login'),
]

urlpatterns += [
    path('v2/register/', RegisterViewV2.as_view(), name='register-v2'),
    path('v2/email-verify/', VerifyEmailV2.as_view(), name="email-verify-v2"),
    path('v2/login/', LoginViewV2.as_view(), name='login-v2'),
    path('v2/usertype/', UpdateUserTypeView.as_view(), name='user-usertype-v2'),
    path('v2/saveprofile/', SavePersonalInfoView.as_view(), name='user-profile-v2'),
    path('v2/getprofile/', GetPersonalInfoView.as_view(), name='user-profile-v2'),
    path('v2/getdropdowns/', getDropdownsView.as_view(), name='get-dropdowns-v2'),
]
