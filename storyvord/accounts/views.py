from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse


from client.models import ClientProfile
from crew.models import CrewProfile
from .serializers import ClientProfileSerializer, CrewProfileSerializer, EmailVerificationSerializer, RegisterNewSerializer, RegisterSerializer, LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, UserChangePasswordSerializer, UserProfileSerializer, UserSerializer

def get_tokens_for_user(user):
  refresh_token = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh_token),
      'access': str(refresh_token.access_token),
  }

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            # Generate a JSON Web Token to verify the user
            token = get_tokens_for_user(user)['access']
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            # Save the user steps as '1'
            user.steps = '1'
            user.save()
            # Generate the verification email link
            absurl = f"{settings.SITE_URL}/api/accounts/email-verify/?token={token}"
            # Render the verification email template
            email_body = render_to_string(
                'email/verification.html', {'user': user.email, 'absurl': absurl}
            )
            # Create the verification email
            email = EmailMessage(
                subject="Activate your account",
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            # Specify the email content subtype as 'html'
            email.content_subtype = "html"
            # Use the EmailThread to send the email
            EmailThread(email).start()
            print("Email Sended Successfully")
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "User created successfully",
                "data": serializer.data,
                "token": token,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(e)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterNewView(APIView):
    serializer_class = RegisterNewSerializer
    def post(self, request, *args, **kwargs):
        serializer = RegisterNewSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token = RefreshToken.for_user(user).access_token
            tokens = get_tokens_for_user(user)
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            user.steps = '1'
            user.verified=True
            user.save()
            
            absurl = ''
            if settings.PROD:
                absurl = f"http://api-story.storyvord.com/api/accounts/email-verify/?token={str(token)}"
            else:
                absurl = f"http://127.0.0.1:8000/api/accounts/email-verify/?token={str(token)}"
                
            email_body = render_to_string('email/verification.html',{
                'user': user.email,
                'absurl': absurl,
            })
            email = EmailMessage(
                subject="Activate your account",
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.content_subtype = "html"
            EmailThread(email).start()
            print("Email Sended Successfully")
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            user_obj = serializer.data
            user = User.objects.get(email=user_obj['email'])
            if not user.verified:
                token = RefreshToken.for_user(user).access_token
                absurl = ''
                if settings.PROD:
                    absurl = f"http://api-story.storyvord.com/api/accounts/email-verify/?token={str(token)}"
                else:
                    absurl = f"http://127.0.0.1:8000/api/accounts/email-verify/?token={str(token)}"
                    
                email_body = render_to_string('email/verification.html',{
                    'user': user.email,
                    'absurl': absurl,
                })
                email = EmailMessage(
                    subject="Activate your account",
                    body=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                email.content_subtype = "html"
                EmailThread(email).start()
                print("Email Sended Successfully")

                return Response(
                    {"detail": "Email is not verified. A verification email has been sent."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            user_profile_serializer = UserProfileSerializer(user)
            user_serializer = UserSerializer(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data,  # Serialized user data
                'profile': user_profile_serializer.data['profile']  # Serialized profile data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# reset password views


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status, views, permissions
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
import os
from django.http import HttpResponsePermanentRedirect
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
import threading



class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RequestPasswordResetEmailAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email', '')
        user = User.objects.filter(email=email).first()

        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain

            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            if settings.PROD:
                url = f"http://dev.storyvord.com/recover-password-confirm"
            else:
                url = f"http://dev.storyvord.com/recover-password-confirm"

            abs_url = f'http://api-stage.storyvord.com{relative_link}?redirect_url={url}'
            # abs_url = f'http://127.0.0.1:8000{relative_link}?redirect_url={url}'
            email_body = render_to_string('email/password_reset.html', {
                'user': user.email,
                'abs_url': abs_url,
            })

            email = EmailMessage(
                subject='Reset your password',
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            email.content_subtype = 'html'
            EmailThread(email).start()

            resp_data = {
                "message": "Success",
                "data": 'We have sent you a link to reset your password',
                "link": abs_url
            }
            return Response(resp_data, status=status.HTTP_200_OK)
        else:
            resp_data = {
                "message": "Error",
                "data": 'No user found'
            }
            return Response(resp_data, status=status.HTTP_404_NOT_FOUND)
        
class PasswordTokenCheckAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if settings.PROD:
                url = f"http://dev.storyvord.com/recover-password-confirm"
            else:
                url = f"http://dev.storyvord.com/recover-password-confirm"

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(url+'?token_valid=False')
                    
                else:
                    return CustomRedirect(url+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)

        except DjangoUnicodeDecodeError as identifier:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(url+'?token_valid=False')

            

class NewPasswordSetAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if settings.PROD:
            url = f"https://dev.storyvord.com/auth/sign-in"
        else:
            url = f"http://dev.storyvord.com/auth/sign-in"
        return Response({'success': True, 'message': 'Password reset success', 'url': url}, status=status.HTTP_200_OK)
        
class UserChangePasswordAPIView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        resp_data = {
            "message": "Success",
            "data": "Password Changed Successfully"
        }
        return Response(resp_data,status=status.HTTP_200_OK)
       
       
# email verification

class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        try:
            token = request.GET.get('token')

            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            try:
                url = f"http://dev.storyvord.com/auth/sign-in"
                
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

                if User.objects.filter(id=payload['user_id']).exists():
                    user = User.objects.get(id=payload['user_id'])
                    current_site = get_current_site(request).domain
                    redirect = url
                    if not user.verified:
                        user.verified = True
                        user.save()
                        # print(user)
                        link = url
                        email_body = render_to_string('email/user-welcome.html',{
                            'link': link,
                            'email': user.email
                        })

                        email = EmailMessage(subject='Welcome to Somhako ATS', body=email_body, from_email=settings.DEFAULT_FROM_EMAIL, to=[user.email])
                        email.content_subtype = 'html'
                        EmailThread(email).start()

                        redirect = url
                    return HttpResponseRedirect(redirect_to=redirect)
                else:
                    return Response({'email': 'Not Activated'}, status=status.HTTP_200_OK)

            except:
                if settings.PROD == True:
                    return HttpResponseRedirect(redirect_to="http://dev.storyvord.com/auth/sign-in")
                else:
                    return HttpResponseRedirect(redirect_to="http://dev.storyvord.com/auth/sign-in")
        except:
            if settings.PROD == True:
                return HttpResponseRedirect(redirect_to="http://dev.storyvord.com/auth/sign-in")
            else:
                return HttpResponseRedirect(redirect_to="http://dev.storyvord.com/auth/sign-in")

                
class SelectUserType(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.steps == False: 
            user_type = request.data.get('user_type')
            if not user_type:
                return Response({'message': 'User type is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.user_type = user_type
            user.save()
            # self.create_profile(user)
        # elif user.steps == '2':
        #     # CLient profile api PUT /api/client/profile/details 
        #     user.steps = '3'
        #     user.save()
        # elif user.steps == '3':
        #     # Step 3: Onboard project API or any other logic
        #     user.steps = 'F'
        #     user.save()
        #     self.onboard_project(user)
        else:
            return Response({'message': 'User already registered'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Success'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    
    def get(self, request, format=None):
        user = request.user

        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = {
            'user': user
        }
        user_data['profile'] = self.get_profile(user)

        serializer = UserProfileSerializer(user_data)
        return Response(serializer.data)

    def get_profile(self, user):
        if user.user_type == 'client':
            return ClientProfile.objects.filter(user=user).first()
        elif user.user_type == 'crew':
            return CrewProfile.objects.filter(user=user).first()
        return None



def google_custom_login_redirect(request):
    if request.user.is_authenticated:
        if request.user.auth_provider != 'google':
            user = request.user
            user.auth_provider = 'google'
            user.save()
        refresh = RefreshToken.for_user(request.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Authentication failed'}, status=401)