from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404

class CrewProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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