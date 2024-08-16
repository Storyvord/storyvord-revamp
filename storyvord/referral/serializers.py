from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, ProjectInvitation
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
import uuid

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInvitation
        fields = '__all__'

    def create(self, validated_data):
        project = validated_data.get('project')
        crew_email = validated_data.get('crew_email')
        referral_code = validated_data.get('referral_code', str(uuid.uuid4()))
        invitation, created = ProjectInvitation.objects.get_or_create(
            project=project,
            crew_email=crew_email,
            defaults={'status': 'pending', 'referral_code': referral_code}
        )

        if created:
            request = self.context.get('request')  # Access the request from context
            user_exists = User.objects.filter(email=crew_email).exists()
            if user_exists:
                self.send_existing_user_invitation_email(crew_email, project, invitation, request)
            else:
                self.send_new_user_registration_email(crew_email, project, referral_code, request)
        return invitation

    def get_site_info(self, request):
        if request:
            current_site = get_current_site(request)
            domain = current_site.domain
            scheme = 'https' if request.is_secure() else 'http'
        else:
            # Fallback if request is None or not provided
            domain = Site.objects.get_current().domain
            scheme = 'https'  # Default to https, or use 'http' if your environment is not secure
        return scheme, domain
    
   
    def send_existing_user_invitation_email(self, crew_email, project, invitation, request):
        scheme, domain = self.get_site_info(request)
        
        subject = 'Project Invitation'
        if settings.PROD == False:
            accept_url = f'http://127.0.0.1:8000/api/referral/invitations/accept/?referral_code={invitation.referral_code}'
            reject_url = f'http://127.0.0.1:8000/api/referral/invitations/reject/?referral_code={invitation.referral_code}'
        else:
            accept_url = f'https://storyvord-back-end-d432tn3msq-uc.a.run.app/api/referral/invitations/accept/?referral_code={invitation.referral_code}'
            reject_url = f'https://storyvord-back-end-d432tn3msq-uc.a.run.app/api/referral/invitations/reject/?referral_code={invitation.referral_code}'
        
        print(accept_url)
        
        message = (
            f'Hi,\n\n'
            f'You have been invited to join the project "{project.name}".\n\n'
            f'Please choose to approve or reject the invitation by clicking the links below:\n'
            f'Approve: {accept_url}\n'
            f'Reject: {reject_url}\n\n'
            f'Best regards,\nThe Team'
        )
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [crew_email],
            fail_silently=False,
        )

    def send_new_user_registration_email(self, crew_email, project, referral_code, request):
        scheme, domain = self.get_site_info(request)
        print("Site", scheme, domain)

        if settings.PROD == False:
            registration_url = f'http://127.0.0.1:8000/api/referral/register-with-referral/?project_id={project.project_id}&referral_code={referral_code}'
        else:
            registration_url = f'https://storyvord-back-end-d432tn3msq-uc.a.run.app/api/referral/register-with-referral/?project_id={project.project_id}&referral_code={referral_code}'
        subject = 'Register to Join a Project'
        
        print(registration_url)
        
        message = (
            f'Hi,\n\n'
            f'You have been invited to register for the project "{project.name}".\n'
            f'Please complete your registration using the following link:\n'
            f'{registration_url}\n\n'
            f'Best regards,\nThe Team'
        )
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [crew_email],
            fail_silently=False,
        )


class InvitationRequestSerializer(serializers.Serializer):
    crew_email = serializers.EmailField()
    project_id = serializers.CharField()

    def create(self, validated_data):
        crew_email = validated_data['crew_email']
        project_id = validated_data['project_id']
        print(crew_email, project_id)
        try:
            project = Project.objects.get(project_id=project_id)
            print(project)
            invitation_data = {
                'project': project.project_id,
                'crew_email': crew_email,
            }
            print(invitation_data)
            serializer = ProjectInvitationSerializer(data=invitation_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except Project.DoesNotExist:
            raise serializers.ValidationError('Project does not exist.')

class RegisterWithReferralSerializer(serializers.Serializer):
    project_id = serializers.CharField()
    referral_code = serializers.CharField()

    def validate(self, data):
        project_id = data.get('project_id')
        referral_code = data.get('referral_code')

        try:
            project = Project.objects.get(project_id=project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError('Project does not exist.')

        try:
            invitation = ProjectInvitation.objects.get(referral_code=referral_code, project=project)
        except ProjectInvitation.DoesNotExist:
            raise serializers.ValidationError('Invalid referral code.')

        return data

    def create(self, validated_data):
        project_id = validated_data['project_id']
        referral_code = validated_data['referral_code']
        
        # Proceed with user registration
        user_data = {
            'email': self.context['request'].data.get('email'),
            'password': self.context['request'].data.get('password'),
            'user_type': 'crew',
        }
        user_serializer = UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Add user to the project
        project = Project.objects.get(project_id=project_id)
        project.crew_profiles.add(user)

        return user

class UserCreateSerializer(serializers.ModelSerializer):
    user_type = 'crew'
    class Meta:
        model = User
        fields = ('email', 'password', 'user_type')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
