from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email,  password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_new_user(self, email,  password=None, user_type=None, verified=True, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(email=email, user_type=user_type, verified=True, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


AUTH_PROVIDERS = {'email': 'email',
                #   'facebook': 'facebook',
                  'google': 'google'}

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [ 
        ('client', 'Client'),
        ('crew', 'Crew'),
        ('vendor', 'Vendor'),
        ('internal', 'Internal Team'),
        ('superuser', 'Super User'),
    ]
    email = models.EmailField(max_length=255,unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    verified = models.BooleanField(default=False)
    steps = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    objects = UserManager() 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def get_full_name(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
