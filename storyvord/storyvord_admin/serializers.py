from rest_framework import serializers

from project.models import Project
from crew.models import *
from storyvord.utils import Base64FileField

# Individual Nested Serializers for related fields
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

class CrewPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrewPortfolio
        fields = '__all__'

# Main Serializer that includes nested fields and handles custom logic
class CrewProfileSerializer(serializers.ModelSerializer):
    image = Base64FileField(required=False, allow_null=True)
    crew_credits = serializers.SerializerMethodField()
    crew_education = serializers.SerializerMethodField()
    endorsement_from_peers = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()
    crew_portfolio = serializers.SerializerMethodField()

    class Meta:
        model = CrewProfile
        fields = '__all__'
        read_only_fields = ('user',)

    # Methods to handle related field serialization
    def get_crew_credits(self, obj):
        credits = CrewCredits.objects.filter(crew=obj)
        return CrewCreditsSerializer(credits, many=True).data

    def get_crew_education(self, obj):
        education = CrewEducation.objects.filter(crew=obj)
        return CrewEducationSerializer(education, many=True).data

    def get_endorsement_from_peers(self, obj):
        endorsements = EndorsementfromPeers.objects.filter(crew=obj)
        return EndorsementfromPeersSerializer(endorsements, many=True).data

    def get_social_links(self, obj):
        links = SocialLinks.objects.filter(crew=obj)
        return SocialLinksSerializer(links, many=True).data

    def get_crew_portfolio(self, obj):
        portfolios = CrewPortfolio.objects.filter(crew=obj)
        return CrewPortfolioSerializer(portfolios, many=True).data