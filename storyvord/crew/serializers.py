from rest_framework import serializers

from project.models import Project
from .models import *

class CrewProfileSerializer(serializers.ModelSerializer):
    class Meta:
        # Base 64 image
        model = CrewProfile
        fields = '__all__'
        read_only_fields = ('user',)

class CrewCreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewCredits
        fields = '__all__'
        
class CrewEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewEducation
        fields = '__all__'
        
class EndorsementfromPeersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndorsementfromPeers
        fields = '__all__'

class SocialLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = '__all__'
        

# Crew Porfolio and its verification

class ClientReferenceVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientReferenceVerification
        fields = ['fname', 'lname', 'email', 'company_name']

class ImbdLinkVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImbdLinkVerification
        fields = ['link']

class WorkSampleVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSampleVerification
        fields = ['minutes', 'seconds']
        
class EmailAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAgreement
        fields = ['document']

class CrewPortfolioSerializer(serializers.ModelSerializer):
    verification_details = serializers.SerializerMethodField()

    class Meta:
        model = CrewPortfolio
        fields = [
            'id', 'title', 'link', 'image', 'contentTag', 'description', 'providedService',
            'verification_type', 'verified', 'verification_details'
        ]

    def get_verification_details(self, obj):
        if obj.verification_type == 'client_reference':
            serializer = ClientReferenceVerificationSerializer(obj.client_reference_verification)
        elif obj.verification_type == 'imbd_link':
            serializer = ImbdLinkVerificationSerializer(obj.imbd_link_verification)
        elif obj.verification_type == 'work_sample':
            serializer = WorkSampleVerificationSerializer(obj.work_sample_verification)
        elif obj.verification_type == 'email_agreement':
            serializer = EmailAgreementSerializer(obj.email_agreement_verification)
        else:
            return None
        return serializer.data
    
class CrewPortfolioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewPortfolio
        fields = [
            'title', 'link', 'image', 'contentTag', 'description', 'providedService',
            'verification_type'
        ]
        
        
# Crew Projects

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'project_id', 'name', 'brief', 'additional_details',
            'budget_currency', 'budget_amount', 'content_type',
            'selected_crew', 'equipment', 'uploaded_document',
            'location_details', 'status', 'created_at', 'updated_at'
        ]
        
class CompanyProjectsResponseSerializer(serializers.Serializer):
    company_name = serializers.CharField()
    projects = ProjectSerializer(many=True)