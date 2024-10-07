from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email,  password=None, user_type=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user_type_instance = UserType.objects.get(name=user_type) if user_type else None
        user = self.model(email=email, user_type=user_type_instance, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_new_user(self, email,  password=None, user_type=None, verified=True, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        user_type_instance = UserType.objects.get(name=user_type) if user_type else None
        
        user = self.model(email=email, user_type=user_type_instance, verified=True, **extra_fields)
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

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class UserType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name='user_types', blank=True)

    def __str__(self):
        return self.name
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True, blank=True)
    user_stage = models.CharField(max_length=10, blank=True, null=True)
    verified = models.BooleanField(default=False)
    steps = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    objects = UserManager() 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256, null=True, blank=True)
    contact_number = models.CharField(max_length=256, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    languages = models.CharField(max_length=256, null=True, blank=True)
    job_title = models.CharField(max_length=256, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name