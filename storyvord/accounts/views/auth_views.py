from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.utils import send_verification_email, get_tokens_for_user
from accounts.serializers import RegisterSerializer, RegisterNewSerializer, LoginSerializer
from accounts.models import User

class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            token = get_tokens_for_user(user)['access']
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            user.steps = '1'
            user.save()

            # Send email
            send_verification_email(user, token)

            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "User created successfully",
                "data": serializer.data,
                "access_token": token,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Something went wrong",
                "data": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class RegisterNewView(APIView):
    serializer_class = RegisterNewSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        user.steps = '1'
        user.verified = True
        user.save()

        absurl = settings.SITE_URL + f"/api/accounts/email-verify/?token={tokens['access']}"
        send_verification_email(user, tokens['access'], absurl)

        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user_obj = serializer.data
        user = User.objects.get(email=user_obj['email'])

        if not user.verified:
            token = get_tokens_for_user(user)['access']
            send_verification_email(user, token)
            return Response({
                "detail": "Email is not verified. A verification email has been sent."
            }, status=status.HTTP_400_BAD_REQUEST)

       
