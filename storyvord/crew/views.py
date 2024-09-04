from collections import defaultdict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from client.models import ClientCompanyProfile
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

    def get(self, request, format=None, pk=None):
        if pk:
            crew_profiles = CrewProfile.objects.filter(pk=pk)
        else:
            crew_profiles = CrewProfile.objects.all()
        response_data = []

        for crew_profile in crew_profiles:
            crew_credits = CrewCredits.objects.filter(crew=crew_profile)
            crew_education = CrewEducation.objects.filter(crew=crew_profile)
            endorsement_from_peers = EndorsementfromPeers.objects.filter(crew=crew_profile)
            social_links = SocialLinks.objects.filter(crew=crew_profile)


            # Serialize the data
            crew_profile_data = CrewProfileSerializer(crew_profile).data
            crew_credits_data = CrewCreditsSerializer(crew_credits, many=True).data
            crew_education_data = CrewEducationSerializer(crew_education, many=True).data
            endorsement_from_peers_data = EndorsementfromPeersSerializer(endorsement_from_peers, many=True).data
            social_links_data = SocialLinksSerializer(social_links, many=True).data

            # Construct the response data for this crew profile
            profile_response_data = {
                'crew_profile': crew_profile_data,
                'crew_credits': crew_credits_data,
                'crew_education': crew_education_data,
                'endorsement_from_peers_data': endorsement_from_peers_data,
                'social_links': social_links_data,
            }

            response_data.append(profile_response_data)

        return Response(response_data)
    

# Crew Porfolio and its verification APIS

class CrewPortfolioListCreate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewPortfolioCreateSerializer
    def get(self, request):
        try:
            crew_profile = CrewProfile.objects.get(user=request.user)
        except CrewProfile.DoesNotExist:
            return Response({"detail": "CrewProfile not found."}, status=status.HTTP_404_NOT_FOUND)

        # List CrewPortfolios associated with the CrewProfile
        portfolios = CrewPortfolio.objects.filter(crew=crew_profile)
        serializer = CrewPortfolioSerializer(portfolios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            crew_profile = CrewProfile.objects.get(user=request.user)
        except CrewProfile.DoesNotExist:
            return Response({"detail": "CrewProfile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CrewPortfolioCreateSerializer(data=request.data)
        if serializer.is_valid():
            portfolio = serializer.save(crew=crew_profile)
            return Response(CrewPortfolioSerializer(portfolio).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CrewPortfolioDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CrewPortfolioSerializer
    def get_object(self, pk):
        try:
            return CrewPortfolio.objects.get(pk=pk)
        except CrewPortfolio.DoesNotExist:
            return None

    def get(self, request, pk):
        portfolio = self.get_object(pk)
        if portfolio is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the portfolio belongs to the authenticated user's CrewProfile
        if portfolio.crew.user != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CrewPortfolioSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        portfolio = self.get_object(pk)
        if portfolio is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the portfolio belongs to the authenticated user's CrewProfile
        if portfolio.crew.user != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CrewPortfolioSerializer(portfolio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        portfolio = self.get_object(pk)
        if portfolio is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the portfolio belongs to the authenticated user's CrewProfile
        if portfolio.crew.user != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyClientReference(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientReferenceVerificationSerializer
    def post(self, request, pk):
        portfolio = CrewPortfolio.objects.filter(id=pk).first()
        if not portfolio:
            return Response({"detail": "Crew Portfolio not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if portfolio.crew.user != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ClientReferenceVerificationSerializer(data=request.data)
        if serializer.is_valid():
            verification, created = ClientReferenceVerification.objects.get_or_create(crew_portfolio=portfolio, defaults=serializer.validated_data)
            if not created:
                for attr, value in serializer.validated_data.items():
                    setattr(verification, attr, value)
                verification.save()
            portfolio.verification_type = 'client_reference'
            portfolio.client_reference_verification = verification
            portfolio.verified = True
            portfolio.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyImbdLink(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ImbdLinkVerificationSerializer
    def post(self, request, pk):
        portfolio = CrewPortfolio.objects.filter(id=pk).first()
        if not portfolio:
            return Response({"detail": "Crew Portfolio not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if portfolio.crew.user != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ImbdLinkVerificationSerializer(data=request.data)
        if serializer.is_valid():
            verification, created = ImbdLinkVerification.objects.get_or_create(crew_portfolio=portfolio, defaults=serializer.validated_data)
            if not created:
                for attr, value in serializer.validated_data.items():
                    setattr(verification, attr, value)
                verification.save()
            portfolio.verification_type = 'imbd_link'
            portfolio.imbd_link_verification = verification
            portfolio.verified = True
            portfolio.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyWorkSample(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WorkSampleVerificationSerializer
    def post(self, request, pk):
        portfolio = CrewPortfolio.objects.filter(id=pk).first()
        if not portfolio:
            return Response({"detail": "Crew Portfolio not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if portfolio.crew.user != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        serializer = WorkSampleVerificationSerializer(data=request.data)
        if serializer.is_valid():
            verification, created = WorkSampleVerification.objects.get_or_create(crew_portfolio=portfolio, defaults=serializer.validated_data)
            if not created:
                for attr, value in serializer.validated_data.items():
                    setattr(verification, attr, value)
                verification.save()
            portfolio.verification_type = 'work_sample'
            portfolio.work_sample_verification = verification
            portfolio.verified = True
            portfolio.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailAgreement(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailAgreementSerializer
    def post(self, request, pk):
        portfolio = CrewPortfolio.objects.filter(id=pk).first()
        if not portfolio:
            return Response({"detail": "Crew Portfolio not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if portfolio.crew.user != request.user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EmailAgreementSerializer(data=request.data)
        if serializer.is_valid():
            verification, created = EmailAgreement.objects.get_or_create(crew_portfolio=portfolio, defaults=serializer.validated_data)
            if not created:
                for attr, value in serializer.validated_data.items():
                    setattr(verification, attr, value)
                verification.save()
            portfolio.verification_type = 'email_agreement'
            portfolio.email_agreement_verification = verification
            portfolio.verified = True
            portfolio.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# All Projects

class UserProjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    def get(self, request):
        user = request.user
        projects = Project.objects.filter(crew_profiles=user)
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CompanyProjectsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        projects = Project.objects.filter(selected_crew=user)
        
        company_projects = defaultdict(list)
        
        for project in projects:
            creator = project.user  
            
            try:
                company_profile = ClientCompanyProfile.objects.get(user=creator)
                company_name = company_profile.company_name
            except ClientCompanyProfile.DoesNotExist:
                company_name = "Unknown"
            
            project_data = ProjectSerializer(project).data
            company_projects[company_name].append(project_data)
        
        response_data = [
            {
                "company_name": company,
                "projects": projects
            }
            for company, projects in company_projects.items()
        ]
        
        return Response(response_data, status=status.HTTP_200_OK)

        
class CrewProfileSearchView(APIView):
    def get(self, request, format=None):
        location_query = request.query_params.get('location', '')
        skills_query = request.query_params.get('skills', '')

        # Filter crew profiles based on partial matches to location and skills
        crews = CrewProfile.objects.filter(
            location__icontains=location_query, 
            skills__icontains=skills_query, 
            active=True
        )
        serializer = CrewProfileSerializer(crews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
