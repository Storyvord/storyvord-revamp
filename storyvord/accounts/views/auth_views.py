from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from accounts.utils import send_verification_email, get_tokens_for_user
from ..serializers.serializers_v2 import V2RegisterSerializer, V2LoginSerializer, V2UserDataSerializer
from accounts.models import User
import datetime

class RegisterViewV2(APIView):
    serializer_class = V2RegisterSerializer

    def post(self, request, *args, **kwargs):
        """
        Creates a new user instance and sends verification email.

        Args:
            request (object): The request object.

        Returns:
            Response (object): A response object with the status code and message.
        """
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            # Save the user instance to the database
            user = serializer.save()
            # Generate a token for the user
            token = get_tokens_for_user(user)['access']
            # Get the user data from the serializer
            user_data = serializer.data

            # Set the user's steps to 1
            user.steps = '1'
            # Save the user instance again to update the steps
            user.save()

            # Send the verification email
            send_verification_email(user, token)

            # Return a successful response
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "User created successfully",
                "data": {
                    **user_data,
                    "access_token": token,
                    },
            }, status=status.HTTP_201_CREATED)
            
        except serializers.ValidationError as e:
            error_messages = e.detail
            if 'non_field_errors' in error_messages:
                message = error_messages['non_field_errors'][0]
            else:
                message = next(iter(error_messages.values()))[0] 
            return Response({
                "status": status.HTTP_409_CONFLICT,
                "message": e.detail,
                "data": None
            }, status=status.HTTP_409_CONFLICT)
            
        except Exception as e:
            # Return an error response if something goes wrong
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Registration failed",
                "data": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
class LoginViewV2(APIView):
    serializer_class = V2LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Logs in a user and returns user data and tokens.

        Args:
            request (object): The request object.

        Returns:
            Response (object): A response object with the status code and message.

        Raises:
            Exception (object): Any unexpected exceptions.
        """
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.context['user']
            
            # Check if the user's email is verified
            if not user.verified:
                # Send verification email if not verified
                token = get_tokens_for_user(user)['access']
                send_verification_email(user, token)
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Email is not verified. A verification email has been sent."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Successful login, return user data and tokens
            user.last_login = datetime.datetime.now()
            user.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "User logged in successfully",
                "data": {
                    **V2UserDataSerializer(user).data,
                    "access_token": get_tokens_for_user(user)['access'],
                    "refresh_token": get_tokens_for_user(user)['refresh'],
                }
            }, status=status.HTTP_200_OK)

        except serializers.ValidationError as e:
            error_messages = e.detail
            if 'non_field_errors' in error_messages:
                message = error_messages['non_field_errors'][0]
            else:
                message = str(e)
            return Response({
                "status": status.HTTP_409_CONFLICT,
                "message": message,
                "data": None
            }, status=status.HTTP_409_CONFLICT)

        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Login failed",
                "data": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)