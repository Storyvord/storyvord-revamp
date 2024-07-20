from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .utils import send_welcome_email  # Import from utils# from .utils import send_welcome_email  # Import from utils

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    # def create_user(self, email, password, **extra_fields):
    def create_user(self, email, password, user_type, **extra_fields):  # Change: Added user_type parameter

        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)

        extra_fields.setdefault('is_active', True)

        # user = self.model(email=email, **extra_fields)
        user = self.model(email=email, user_type=user_type, **extra_fields)  # Change: Pass user_type to user model

        user.set_password(password)
        user.save(using=self._db)

        # send_welcome_email(user)  # Send welcome email
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        # return self.create_user(email, password, **extra_fields)
        return self.create_user(email, password, **extra_fields)  # Change: Ensure user_type for superuser

    

class User(AbstractUser):
    USER_TYPE_CHOICES = [  # Change: Added USER_TYPE_CHOICES
        ('client', 'Client'),
        ('crew', 'Crew'),
        ('vendor', 'Vendor'),
        ('internal', 'Internal Team'),
    ]

    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)  # Change: Added user_type field


    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
    REQUIRED_FIELDS = ['user_type']  # Change: Added user_type to required fields


    objects = CustomUserManager()

    def __str__(self):
        return self.email
        