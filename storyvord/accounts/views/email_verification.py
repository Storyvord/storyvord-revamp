from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from accounts.utils import verify_email_token, send_welcome_email
from ..serializers.serializers_v2 import V2EmailVerificationSerializer
from utils.env_utils import get_bool_env_var
from django.http import HttpResponseRedirect

PROD = get_bool_env_var('PROD')

class VerifyEmail(APIView):
    serializer_class = V2EmailVerificationSerializer
    def get(self, request):
        try:
            token = request.GET.get('token')
            if user := verify_email_token(token):
                if user.verified:
                    return Response({"message": "Email already verified"}, status=status.HTTP_400_BAD_REQUEST)
                user.verified = True
                user.save()
                send_welcome_email(user)
                if PROD:
                    return HttpResponseRedirect(redirect_to="https://www.storyvord.com/auth/sign-in")
                else:
                    return HttpResponseRedirect(redirect_to="https://dev.storyvord.com/auth/sign-in")
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
