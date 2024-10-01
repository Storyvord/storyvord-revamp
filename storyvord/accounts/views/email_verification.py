from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from accounts.models import User
from accounts.utils import verify_email_token

class VerifyEmail(APIView):
    def get(self, request):
        token = request.GET.get('token')
        user = verify_email_token(token)
        if user:
            user.verified = True
            user.save()
            return Response({"message": "Email verified"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
