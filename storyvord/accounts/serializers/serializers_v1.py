# # # accounts/serializers.py
from rest_framework import serializers

from client.models import ClientProfile
from crew.models import CrewProfile
from accounts.models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class RegisterNewSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'user_type')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data['password'],
            user_type = validated_data.get('user_type')
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'user_type')

class LoginSerializer(serializers.Serializer):
    
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return user


# Change, reset password

from django.core.mail import EmailMessage
from django.conf import settings
from rest_framework import serializers

from accounts.models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string, get_template
import threading



class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# Done

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']          

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      #print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      #print('Password Reset Token', token)
      link = 'http://127.0.0.1:8000/api/auth/reset-password/'+uid+'/'+token
      #print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      email_body = render_to_string('new/reset-password.html',{
            'user': user.email,
            'absurl': link,
        })
      # data = {
      #   'email_subject':'Reset Your Password',
      #   'email_body':body,
      #   'to_email':user.email
      # }
      # Util.send_email(data)
      email = EmailMessage(
          subject="Reset Your Password",
          body=email_body,
          from_email=settings.DEFAULT_FROM_EMAIL,
          to=[user.email],
      )
      email.content_subtype = "html"
      EmailThread(email).start()
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']

# Done

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            email = User.objects.filter(id=id).values_list("email", flat=True)[0]
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match"
            )
        user.set_password(password)
        user.save()
        return attrs
    
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'user_type']

class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = '__all__'

class CrewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewProfile
        fields = '__all__'

class UserProfileSerializer(serializers.Serializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        user = obj  # 'obj' is the User instance
        if user.user_type == 'client':
            profile = ClientProfile.objects.filter(user=user).first()
            serializer = ClientProfileSerializer(profile)
        elif user.user_type == 'crew':
            profile = CrewProfile.objects.filter(user=user).first()
            serializer = CrewProfileSerializer(profile)
        else:
            return None
        return serializer.data
    
class MeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_type', 'id', 'email']