from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

class CrewProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewProfileSerializer
    def get(self, request, format=None):
        profile = get_object_or_404(CrewProfile, user=request.user)
        serializer = CrewProfileSerializer(profile)
        return Response(serializer.data)
     
    def put(self, request, format=None):
        profile = get_object_or_404(CrewProfile, user=request.user)
        serializer = CrewProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrewCreditsListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewCreditsSerializer
    def get(self, request, format=None):
        credits = CrewCredits.objects.filter(crew__user=request.user)
        serializer = CrewCreditsSerializer(credits, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CrewCreditsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrewCreditsDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewCreditsSerializer
    def get_object(self, pk, user):
        return get_object_or_404(CrewCredits, pk=pk, crew__user=user)

    def get(self, request, pk, format=None):
        credit = self.get_object(pk, request.user)
        serializer = CrewCreditsSerializer(credit)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        credit = self.get_object(pk, request.user)
        serializer = CrewCreditsSerializer(credit, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        credit = self.get_object(pk, request.user)
        credit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CrewEducationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewEducationSerializer
    def get(self, request, format=None):
        educations = CrewEducation.objects.filter(crew__user=request.user)
        serializer = CrewEducationSerializer(educations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CrewEducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrewEducationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewEducationSerializer
    def get_object(self, pk, user):
        return get_object_or_404(CrewEducation, pk=pk, crew__user=user)

    def get(self, request, pk, format=None):
        education = self.get_object(pk, request.user)
        serializer = CrewEducationSerializer(education)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        education = self.get_object(pk, request.user)
        serializer = CrewEducationSerializer(education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        education = self.get_object(pk, request.user)
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CrewRateListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewRateSerializer
    def get(self, request, format=None):
        rates = CrewRate.objects.filter(crew__user=request.user)
        serializer = CrewRateSerializer(rates, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CrewRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CrewRateDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewRateSerializer
    def get_object(self, pk, user):
        return get_object_or_404(CrewRate, pk=pk, crew__user=user)

    def get(self, request, pk, format=None):
        rate = self.get_object(pk, request.user)
        serializer = CrewRateSerializer(rate)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        rate = self.get_object(pk, request.user)
        serializer = CrewRateSerializer(rate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        rate = self.get_object(pk, request.user)
        rate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# EndorsementfromPeers Views
class EndorsementfromPeersListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EndorsementfromPeersSerializer
    def get(self, request, format=None):
        endorsements = EndorsementfromPeers.objects.filter(crew__user=request.user)
        serializer = EndorsementfromPeersSerializer(endorsements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EndorsementfromPeersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EndorsementfromPeersDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EndorsementfromPeersSerializer
    def get_object(self, pk, user):
        return get_object_or_404(EndorsementfromPeers, pk=pk, crew__user=user)

    def get(self, request, pk, format=None):
        endorsement = self.get_object(pk, request.user)
        serializer = EndorsementfromPeersSerializer(endorsement)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        endorsement = self.get_object(pk, request.user)
        serializer = EndorsementfromPeersSerializer(endorsement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        endorsement = self.get_object(pk, request.user)
        endorsement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# SocialLinks Views
class SocialLinksListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialLinksSerializer
    def get(self, request, format=None):
        links = SocialLinks.objects.filter(crew__user=request.user)
        serializer = SocialLinksSerializer(links, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SocialLinksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SocialLinksDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SocialLinksSerializer
    def get_object(self, pk, user):
        return get_object_or_404(SocialLinks, pk=pk, crew__user=user)

    def get(self, request, pk, format=None):
        link = self.get_object(pk, request.user)
        serializer = SocialLinksSerializer(link)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        link = self.get_object(pk, request.user)
        serializer = SocialLinksSerializer(link, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        link = self.get_object(pk, request.user)
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        

class CrewListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        crew_profiles = CrewProfile.objects.all()
        response_data = []

        for crew_profile in crew_profiles:
            crew_credits = CrewCredits.objects.filter(crew=crew_profile)
            crew_education = CrewEducation.objects.filter(crew=crew_profile)
            crew_rate = CrewRate.objects.filter(crew=crew_profile)
            endorsement_from_peers = EndorsementfromPeers.objects.filter(crew=crew_profile)
            social_links = SocialLinks.objects.filter(crew=crew_profile)


            # Serialize the data
            crew_profile_data = CrewProfileSerializer(crew_profile).data
            crew_credits_data = CrewCreditsSerializer(crew_credits, many=True).data
            crew_education_data = CrewEducationSerializer(crew_education, many=True).data
            crew_rate_data = CrewRateSerializer(crew_rate, many=True).data
            endorsement_from_peers_data = EndorsementfromPeersSerializer(endorsement_from_peers, many=True).data
            social_links_data = SocialLinksSerializer(social_links, many=True).data

            # Construct the response data for this crew profile
            profile_response_data = {
                'crew_profile': crew_profile_data,
                'crew_credits': crew_credits_data,
                'crew_education': crew_education_data,
                'crew_rate': crew_rate_data,
                'endorsement_from_peers_data': endorsement_from_peers_data,
                'social_links': social_links_data,
            }

            response_data.append(profile_response_data)

        return Response(response_data)