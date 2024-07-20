from django.shortcuts import render

# Create your views here.
# accounts/views.py
# from .utils import send_welcome_email

from rest_framework import generics
from .models import User
from .serializers import UserRegistrationSerializer
# from djoser import email

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     email.ActivationEmail(self.request, user).send()
    #     send_welcome_email(user)  # Send welcome email
