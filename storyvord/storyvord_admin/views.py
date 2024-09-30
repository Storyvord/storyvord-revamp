from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from accounts.serializers import UserSerializer 
from crew.models import CrewProfile, CrewPortfolio, SocialLinks
from .serializers import *


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Check if email and password are provided
        if not email or not password:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is a superuser 
        if not user.user_type == 'superuser':
        # if not user.is_superuser:
            return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)
            
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)

        # Serialize user data and profile
        user_serializer = UserSerializer(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_serializer.data,  # Serialized user data
        }, status=status.HTTP_200_OK)
        

class Pagination(PageNumberPagination):
    page_size = 20 
    page_size_query_param = 'page_size'
    max_page_size = 100

class CrewActiveProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination 

    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     if not user.user_type == 'superuser' and not user.is_superuser:
    #         return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

        
    #     try:
    #         activeCrewProfiles = CrewProfile.objects.filter(active=True)
    #         crew_profiles = CrewProfileSerializer(activeCrewProfiles, many=True)
    #     except CrewProfile.DoesNotExist:
    #         return Response({'error': 'No active crew profiles found'}, status=status.HTTP_404_NOT_FOUND)

    #     return Response(crew_profiles.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.user_type == 'superuser' and not user.is_superuser:
            return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve active crew profiles
        active_crew_profiles = CrewProfile.objects.filter(active=True)

        # Use the paginator to paginate the queryset
        paginator = self.pagination_class()
        paginated_profiles = paginator.paginate_queryset(active_crew_profiles, request)
        crew_profiles_serializer = CrewProfileSerializer(paginated_profiles, many=True)

        return paginator.get_paginated_response(crew_profiles_serializer.data)


class CrewInActiveProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     if not user.user_type == 'superuser' and not user.is_superuser:
    #         return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

        
    #     try:
    #         inActiveCrewProfiles = CrewProfile.objects.filter(active=False)
    #         crew_profiles = CrewProfileSerializer(inActiveCrewProfiles, many=True)
    #     except CrewProfile.DoesNotExist:
    #         return Response({'error': 'No inactive crew profiles found'}, status=status.HTTP_404_NOT_FOUND)

    #     return Response(crew_profiles.data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.user_type == 'superuser' and not user.is_superuser:
            return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve inactive crew profiles
        inactive_crew_profiles = CrewProfile.objects.filter(active=False)

        # Use the paginator to paginate the queryset
        paginator = self.pagination_class()
        paginated_profiles = paginator.paginate_queryset(inactive_crew_profiles, request)
        crew_profiles_serializer = CrewProfileSerializer(paginated_profiles, many=True)

        return paginator.get_paginated_response(crew_profiles_serializer.data)

class CrewUpdateActiveProfileView(APIView):
    permissions_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.user_type == 'superuser' and not user.is_superuser:
            return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

        crew_id = request.data.get('crew_id')
        active = request.data.get('active')
        if crew_id is None or active is None:
            return Response({'error': 'Please provide a crew_id and active'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            crew = CrewProfile.objects.get(pk=crew_id)
        except CrewProfile.DoesNotExist:
            return Response({'error': 'Crew profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

        crew.active = active 
        crew.save()

        return Response({'message': f'Crew profile active state set to {crew.active} successfully'}, status=status.HTTP_200_OK)
     
class CrewVerifiedPortfolioView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.user_type == 'superuser' and not user.is_superuser:
            return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve verified crew portfolios
        verified_crew_portfolios = CrewPortfolio.objects.filter(verified=True)
        # Use the paginator to paginate the queryset
        paginator = self.pagination_class()
        paginated_portfolios = paginator.paginate_queryset(verified_crew_portfolios, request)
        crew_portfolios_serializer = CrewPortfolioSerializer(paginated_portfolios, many=True)

        return paginator.get_paginated_response(crew_portfolios_serializer.data)

class CrewNonVerifiedPortfolioView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.user_type == 'superuser' and not user.is_superuser:
            return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve verified crew portfolios
        nonverified_crew_portfolios = CrewPortfolio.objects.filter(verified=False)
        # Use the paginator to paginate the queryset
        paginator = self.pagination_class()
        paginated_portfolios = paginator.paginate_queryset(nonverified_crew_portfolios, request)
        crew_portfolios_serializer = CrewPortfolioSerializer(paginated_portfolios, many=True)

        return paginator.get_paginated_response(crew_portfolios_serializer.data)

class CrewUpdateVerifiedPortfolioView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.user_type == 'superuser' and not user.is_superuser:
            return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

        portfolio_id = request.data.get('portfolio_id')
        verified = request.data.get('verified')
        if portfolio_id is None or verified is None:
            return Response({'error': 'Please provide a portfolio_id and verified'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            portfolio = CrewPortfolio.objects.get(pk=portfolio_id)
        except CrewPortfolio.DoesNotExist:
            return Response({'error': 'Portfolio does not exist'}, status=status.HTTP_404_NOT_FOUND)

        portfolio.verified = verified 
        portfolio.save()

        return Response({'message': f'Portfolio verified state set to {portfolio.verified} successfully'}, status=status.HTTP_200_OK)


# class CrewSocialLinksView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     pagination_class = Pagination

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         if not user.user_type == 'superuser' and not user.is_superuser:
#             return Response({'error': 'You are not authorized to access this page'}, status=status.HTTP_403_FORBIDDEN)

#         # Retrieve verified crew portfolios
#         social_links = SocialLinks.objects.all()
#         # Use the paginator to paginate the queryset
#         paginator = self.pagination_class()
#         paginated_links = paginator.paginate_queryset(social_links, request)
#         social_links_serializer = SocialLinksSerializer(paginated_links, many=True)

#         return paginator.get_paginated_response(social_links_serializer.data)


class CrewListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    def get(self, request, format=None, pk=None):
        # Get the queryset for crew profiles
        crew_profiles = CrewProfile.objects.filter(pk=pk) if pk else CrewProfile.objects.all()

        # Use the pagination class to paginate the queryset
        paginator = self.pagination_class()
        paginated_profiles = paginator.paginate_queryset(crew_profiles, request)

        # Serialize the paginated profiles
        serializer = CrewProfileSerializer(paginated_profiles, many=True)

        # Return a paginated response using paginator's method
        return paginator.get_paginated_response(serializer.data)