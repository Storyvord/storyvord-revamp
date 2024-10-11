from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.response import Response
from django.core.mail import EmailMessage
from ..serializers.serializers_v2 import ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from accounts.utils import send_password_reset_email, EmailThread
from accounts.models import User

class RequestPasswordResetEmailAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        send_password_reset_email(email, request)
        return Response({
            "message": "We have sent you a link to reset your password"
        }, status=status.HTTP_200_OK)


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    "message": "Token is invalid or expired"
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "Token is valid"
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "message": "Invalid token"
            }, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "message": "Password reset successful"
        }, status=status.HTTP_200_OK)
