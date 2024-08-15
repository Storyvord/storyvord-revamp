from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import InvitationRequestSerializer, RegisterWithReferralSerializer
from .models import ProjectInvitation
from rest_framework.permissions import IsAuthenticated
from accounts.models import User

class AddCrewToProjectView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationRequestSerializer
    def post(self, request, *args, **kwargs):
        serializer = InvitationRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Invitation sent.'}, status=status.HTTP_201_CREATED)

class AcceptInvitationView(APIView):
    def post(self, request, *args, **kwargs):
        referral_code = request.query_params.get('referral_code')
        print(referral_code, "ref")
        if not referral_code:
            return Response({'detail': 'Referral code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = ProjectInvitation.objects.get(referral_code=referral_code, status='pending')
            invitation.save()

            user = User.objects.get(email=invitation.crew_email)
            project = invitation.project
            project.crew_profiles.add(user)

            return Response({'detail': 'Invitation accepted.'}, status=status.HTTP_200_OK)
        except ProjectInvitation.DoesNotExist:
            return Response({'detail': 'Invitation not found or already processed.'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class RejectInvitationView(APIView):
    def post(self, request, *args, **kwargs):
        referral_code = request.query_params.get('referral_code')
        if not referral_code:
            return Response({'detail': 'Referral code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = ProjectInvitation.objects.get(referral_code=referral_code, status='pending')
            invitation.status = 'rejected'
            invitation.save()

            return Response({'detail': 'Invitation rejected.'}, status=status.HTTP_200_OK)
        except ProjectInvitation.DoesNotExist:
            return Response({'detail': 'Invitation not found or already processed.'}, status=status.HTTP_404_NOT_FOUND)

class RegisterWithReferralView(APIView):
    serializer_class = RegisterWithReferralSerializer

    def post(self, request, *args, **kwargs):
        data = {
            'project_id': request.query_params.get('project_id', request.data.get('project_id')),
            'referral_code': request.query_params.get('referral_code', request.data.get('referral_code')),
            'email': request.data.get('email'),
            'password': request.data.get('password')
        }

        serializer = RegisterWithReferralSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Registration complete and added to project.'}, status=status.HTTP_201_CREATED)
