from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializers.serializers_v2 import SelectUserTypeSerializer , PersonalInfoSerializer , UnifiedProfileSerializer, ClientProfileSerializer, CrewProfileSerializer, ProfileSerializer, CountrySerializer
from accounts.models import UserType ,PersonalInfo , Country
from client.models import ClientProfile 
from crew.models import CrewProfile
from drf_spectacular.utils import extend_schema
import logging
logger = logging.getLogger(__name__)

class UpdateUserTypeView(APIView):
    serializer_class = SelectUserTypeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        if user.user_stage == '2':
            return Response(
                {   'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'User type cannot be updated',
                    'data': 'User type cannot be updated'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use the serializer to handle validation and updating the user_type
        serializer = SelectUserTypeSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'User type updated successfully',
                    'data': 'User type updated successfully'
                 }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SavePersonalInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UnifiedProfileSerializer

    def post(self, request):
        """
        Save personal info and profile data for client or crew.

        The endpoint returns a 200 response with the message "Profile information saved successfully." if the request is valid.
        Otherwise, it returns a 400 response with the corresponding error message.
        """
        user = request.user
        user_type_id = user.user_type_id
        
        try:
            # Use the unified serializer
            unified_serializer = UnifiedProfileSerializer(data=request.data, context={'user_type_id': user_type_id})

            if unified_serializer.is_valid():
                personal_info_data = unified_serializer.validated_data['personal_info']
                personal_info_serializer = PersonalInfoSerializer(data=personal_info_data, context={'user': user})
                
                if not personal_info_serializer.is_valid():
                    return Response(personal_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                personal_info_instance = personal_info_serializer.save(user=user)
                
                # Save client or crew profile
                try:
                    if user_type_id == 1:
                        client_profile_data = unified_serializer.validated_data['client_profile']
                        if client_profile_data:
                            client_profile_serializer = ClientProfileSerializer(data=client_profile_data)
                            if client_profile_serializer.is_valid():
                                client_profile_serializer.save(user=user, personal_info=personal_info_instance)
                            else:
                                return Response(client_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    elif user_type_id == 2:
                        crew_profile_data = unified_serializer.validated_data['crew_profile']
                        if crew_profile_data:
                            crew_profile_serializer = CrewProfileSerializer(data=crew_profile_data)
                            if crew_profile_serializer.is_valid():
                                crew_profile_serializer.save(user=user, personal_info=personal_info_instance)
                            else:
                                return Response(crew_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)              
                        
                except Exception as e:
                    logger.error(f"Error in SavePersonalInfoView: {e}")
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                return Response({"message": "Profile information saved successfully."}, status=status.HTTP_200_OK)

            return Response(unified_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error in SavePersonalInfoView: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetPersonalInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_type = user.user_type_id
        
        if user.user_stage != '2':
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Profile information retrieved successfully.",
                "data": {"user": {
                    "email": user.email,
                    "user_type": user.user_type_id,
                    "user_stage": user.user_stage,
                    },
                         }
            }, status=status.HTTP_200_OK)
        
        try:
            personal_info = PersonalInfo.objects.get(user=user)
        except PersonalInfo.DoesNotExist:
            personal_info = None
        
        
        if user_type == 1:
            try:
                client_profile = ClientProfile.objects.get(user=user)
            except ClientProfile.DoesNotExist:
                return Response({"error": "Client profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
            data = {
                "user": {
                    "email": user.email,
                    "user_type": user.user_type_id,
                    "user_stage": user.user_stage,
                },
                "personal_info": personal_info,
                "client_profile": client_profile
            }
            serializer = ProfileSerializer(data)
            # Return a successful response
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Profile information retrieved successfully.",
                "data": {
                    **serializer.data,
                    },
            }, status=status.HTTP_200_OK)
        
        elif user_type == 2:
            try:
                crew_profile = CrewProfile.objects.get(user=user)
            except CrewProfile.DoesNotExist:
                return Response({"error": "Crew profile not found."}, status=status.HTTP_404_NOT_FOUND)

            data = {
                "user": {
                    "email": user.email,
                    "user_type": user.user_type_id,
                    "user_stage": user.user_stage,
                },
                "personal_info": personal_info,
                "crew_profile": crew_profile
            }
            serializer = ProfileSerializer(data)
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Profile information retrieved successfully.",
                "data": {
                    **serializer.data,
                    },
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "User type not found."}, status=status.HTTP_404_NOT_FOUND)
    
    
class getDropdownsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        param = request.GET.get('param')
        if param == 'country':
            countries = Country.objects.all()
            print(countries)
            serializer = CountrySerializer(countries, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    #TODO: add more dropdowns and error handling
    