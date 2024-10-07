from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers.v2.serializers import SelectUserTypeSerializer , PersonalInfoSerializer , UnifiedProfileSerializer, ClientProfileSerializer, CrewProfileSerializer
from accounts.models import UserType
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
        
        if user.user_stage != '1':
            return Response({'message': 'User type cannot be updated'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Use the serializer to handle validation and updating the user_type
        serializer = SelectUserTypeSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User type updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class SavePersonalInfoView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         # Get the current user from the token
#         """
#         Save personal info and profile data for client or crew.

#         The endpoint returns a 200 response with the message "Profile information saved successfully." if the request is valid.
#         Otherwise, it returns a 400 response with the corresponding error message.
#         """
#         user = request.user
#         user_type = user.user_type

#         # Common personal info saving
#         personal_info_data = request.data.get('personal_info')
#         if not personal_info_data:
#             return Response({"error": "Personal info is required."}, status=status.HTTP_400_BAD_REQUEST)

#         personal_info_serializer = PersonalInfoSerializer(data=personal_info_data)
#         if personal_info_serializer.is_valid():
#             personal_info_serializer.save(user=user)
#         else:
#             return Response(personal_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Handle client or crew specific profile using the unified serializer
#         profile_data = request.data.get('profile_data')  # Use a unified key like 'profile_data'
#         if not profile_data:
#             return Response({"error": f"{user_type.capitalize()} profile info is required."}, status=status.HTTP_400_BAD_REQUEST)

#         profile_serializer = UnifiedProfileSerializer(data=profile_data, user_type=user_type)
#         if profile_serializer.is_valid():
#             profile_serializer.save(user=user, personal_info=personal_info_serializer.instance)
#         else:
#             return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"message": "Profile information saved successfully."}, status=status.HTTP_200_OK)


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
