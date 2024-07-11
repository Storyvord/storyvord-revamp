from django.shortcuts import render

# Create your views here.


# accounts/views.py
from rest_framework import generics
from .models import User
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
