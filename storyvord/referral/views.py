from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from client.models import ClientProfile
from .serializers import ClientInvitationSerializer, EmployeeRegisterWithReferralSerializer, InvitationRequestSerializer, ListProjectInvitationSerializer, RegisterWithReferralSerializer
from .models import ClientInvitation, ProjectInvitation
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from project.models import Project

class AddCrewToProjectView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvitationRequestSerializer
    def post(self, request, *args, **kwargs):
        serializer = InvitationRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Invitation sent.'}, status=status.HTTP_201_CREATED)

class AcceptInvitationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        referral_code = request.query_params.get('referral_code')
        print(referral_code, "ref")
        if not referral_code:
            return Response({'detail': 'Referral code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = ProjectInvitation.objects.get(referral_code=referral_code, status='pending')
            invitation.status = 'accepted'
            invitation.save()

            # Add the user to the project 
            user = User.objects.get(email=invitation.crew_email)
            project = invitation.project
            print(project, "project")
            project.crew_profiles.add(user)
            project.save()

            return Response({'detail': 'Invitation accepted.'}, status=status.HTTP_200_OK)
        except ProjectInvitation.DoesNotExist:
            return Response({'detail': 'Invitation not found or already processed.'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class RejectInvitationView(APIView):
    permission_classes = [IsAuthenticated]
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

class RegisterWithReferralCrewView(APIView):
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

class CrewInvitationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_email = request.user.email
        invitations = ProjectInvitation.objects.filter(crew_email=user_email)
        
        # Segregate the invitations by status
        pending_invitations = invitations.filter(status='pending')
        accepted_invitations = invitations.filter(status='accepted')
        rejected_invitations = invitations.filter(status='rejected')

        # Serialize the data
        pending_serializer = ListProjectInvitationSerializer(pending_invitations, many=True)
        accepted_serializer = ListProjectInvitationSerializer(accepted_invitations, many=True)
        rejected_serializer = ListProjectInvitationSerializer(rejected_invitations, many=True)

        # Structure the response data
        response_data = {
            'pending': pending_serializer.data,
            'accepted': accepted_serializer.data,
            'rejected': rejected_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

class ClientCrewInvitationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, *args, **kwargs):
        user = request.user
        invitations = ProjectInvitation.objects.filter(project__user=user, project__project_id=project_id)
        
        # Segregate the invitations by status
        pending_invitations = invitations.filter(status='pending')
        accepted_invitations = invitations.filter(status='accepted')
        rejected_invitations = invitations.filter(status='rejected')

        # Serialize the data
        pending_serializer = ListProjectInvitationSerializer(pending_invitations, many=True)
        accepted_serializer = ListProjectInvitationSerializer(accepted_invitations, many=True)
        rejected_serializer = ListProjectInvitationSerializer(rejected_invitations, many=True)

        # Structure the response data
        response_data = {
            'pending': pending_serializer.data,
            'accepted': accepted_serializer.data,
            'rejected': rejected_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    
class AddEmployeeToClientProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Fetch the client profile for the authenticated user
        try:
            client_profile = ClientProfile.objects.get(user=request.user)
        except ClientProfile.DoesNotExist:
            return Response({'detail': 'Client profile not found for the authenticated user.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Prepare new data dictionary with client_profile ID
        data = request.data.copy()  # Make a copy of the original data
        data['client_profile'] = client_profile.pk
        print(data)
        
        
        # Check if the employee is already working as an employee
        if ClientInvitation.objects.filter(employee_email=data['employee_email'], status='accepted').exists():
            return Response({'detail': 'Employee already working as an employee.'}, status=status.HTTP_400_BAD_REQUEST)


        # Create and validate serializer
        serializer = ClientInvitationSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Invitation sent.'}, status=status.HTTP_201_CREATED)


class AcceptClientInvitationView(APIView):
    def get(self, request, *args, **kwargs):
        referral_code = request.query_params.get('referral_code')
        try:
            invitation = ClientInvitation.objects.get(referral_code=referral_code, status='pending')
            invitation.status = 'accepted'
            invitation.save()

            # Add the employee to the client profile
            user = User.objects.get(email=invitation.employee_email)
            invitation.client_profile.employee_profile.add(user)

            return Response({'detail': 'Invitation accepted and you have been added to the client profile.'}, status=status.HTTP_200_OK)
        except ClientInvitation.DoesNotExist:
            return Response({'detail': 'Invitation not found or already processed.'}, status=status.HTTP_400_BAD_REQUEST)


class RejectClientInvitationView(APIView):
    def get(self, request, *args, **kwargs):
        referral_code = request.query_params.get('referral_code')
        try:
            invitation = ClientInvitation.objects.get(referral_code=referral_code, status='pending')
            invitation.status = 'rejected'
            invitation.save()
            return Response({'detail': 'Invitation rejected.'}, status=status.HTTP_200_OK)
        except ClientInvitation.DoesNotExist:
            return Response({'detail': 'Invitation not found or already processed.'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterWithReferralView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmployeeRegisterWithReferralSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Registration complete and added to client profile.'}, status=status.HTTP_201_CREATED)
    
class EmployeeInvitationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_email = request.user.email
        invitations = ClientInvitation.objects.filter(employee_email=user_email)
        
        # Segregate the invitations by status
        pending_invitations = invitations.filter(status='pending')
        accepted_invitations = invitations.filter(status='accepted')
        rejected_invitations = invitations.filter(status='rejected')

        # Serialize the data
        pending_serializer = ClientInvitationSerializer(pending_invitations, many=True)
        accepted_serializer = ClientInvitationSerializer(accepted_invitations, many=True)
        rejected_serializer = ClientInvitationSerializer(rejected_invitations, many=True)

        # Structure the response data
        response_data = {
            'pending': pending_serializer.data,
            'accepted': accepted_serializer.data,
            'rejected': rejected_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ClientEmployeeInvitationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        invitations = ClientInvitation.objects.filter(client_profile__user=user)
        
        # Segregate the invitations by status
        pending_invitations = invitations.filter(status='pending')
        accepted_invitations = invitations.filter(status='accepted')
        rejected_invitations = invitations.filter(status='rejected')

        # Serialize the data
        pending_serializer = ClientInvitationSerializer(pending_invitations, many=True)
        accepted_serializer = ClientInvitationSerializer(accepted_invitations, many=True)
        rejected_serializer = ClientInvitationSerializer(rejected_invitations, many=True)

        # Structure the response data
        response_data = {
            'pending': pending_serializer.data,
            'accepted': accepted_serializer.data,
            'rejected': rejected_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class ReferralCodeDetailView(APIView):
    def get(self, request, *args, **kwargs):
        referral_code = request.query_params.get('referral_code')

        if not referral_code:
            return Response({'detail': 'Referral code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = ClientInvitation.objects.get(referral_code=referral_code)
            serializer = ClientInvitationSerializer(invitation)
            return Response(serializer.data)

        except ClientInvitation.DoesNotExist:
            return Response({'detail': 'Invitation not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        
class ReferralCodeCrewDetailView(APIView):
    def get(self, request, *args, **kwargs):
        referral_code = request.query_params.get('referral_code')

        if not referral_code:
            return Response({'detail': 'Referral code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = ProjectInvitation.objects.get(referral_code=referral_code)
            serializer = ListProjectInvitationSerializer(invitation)
            return Response(serializer.data)

        except ProjectInvitation.DoesNotExist:
            return Response({'detail': 'Invitation not found.'}, status=status.HTTP_404_NOT_FOUND)