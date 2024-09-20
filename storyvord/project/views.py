
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from rest_framework.generics import GenericAPIView 
from django.db.models import Q


class ProjectOnboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        
        if user.user_type != 'client':
            return Response({'error': 'Only clients can create projects'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.steps:
            return Response({'error': 'User has already completed the onboarding process'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            user.steps = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get(self, request):
        projects = Project.objects.filter(
            Q(user=request.user) | Q(crew_profiles=request.user)
        ).distinct()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_object(self, pk, user):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise NotFound("Project not found")
        if project.user != user:
            raise PermissionDenied("You do not have permission to access this project")
        return project

    def get(self, request, pk):
        project = self.get_object(pk, request.user)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = self.get_object(pk, request.user)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk, request.user)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SendOnboardRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnboardRequestSerializer
    def post(self, request):
        project_id = request.data.get('project_id')
        user_id = request.data.get('user_id')

        # Check if the project and user exist
        try:
            project = Project.objects.get(project_id=project_id)
            user = User.objects.get(id=user_id)
        except (Project.DoesNotExist, User.DoesNotExist):
            return Response({'error': 'Invalid project or user ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an onboarding request
        onboard_request = OnboardRequest.objects.create(project=project, user=user)

        serializer = OnboardRequestSerializer(onboard_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class UpdateOnboardRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnboardRequestSerializer
    def patch(self, request, pk):
        try:
            onboard_request = OnboardRequest.objects.get(pk=pk)
        except OnboardRequest.DoesNotExist:
            return Response({'error': 'Onboarding request not found'}, status=status.HTTP_404_NOT_FOUND)

        status2 = request.data.get('status')
        if status2 not in ['accepted', 'declined']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(onboard_request.status)

        onboard_request.status = status2
        onboard_request.save()

        if status2 == 'accepted':
            onboard_request.project.crew_profiles.add(onboard_request.user)

        serializer = OnboardRequestSerializer(onboard_request)
        return Response(serializer.data)

class PendingOnboardRequestsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnboardRequestSerializer
    def get(self, request):
        user = request.user
        onboard_requests = OnboardRequest.objects.filter(user=user, status='pending')
        serializer = OnboardRequestSerializer(onboard_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OnboardRequestsByProjectView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnboardRequestsByProjectSerializer
    def get(self, request, project_id):
        try:
            project = Project.objects.get(project_id=project_id)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OnboardRequestsByProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
class CrewListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer 

    def get(self, request, project_id):
        project = Project.objects.get(project_id=project_id)
        crew_profiles = project.crew_profiles.all()
        
        serializer = UserSerializer(crew_profiles, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    