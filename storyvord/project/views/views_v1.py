
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..models import *
from ..serializers.serializers_v1 import *
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from rest_framework.generics import GenericAPIView 
from django.db.models import Q
from storyvord.exception_handlers import custom_exception_handler


class ProjectOnboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def post(self, request):
        try:
            user = request.user
        
            if user.user_type != 'client':
                return Response({'status': False,
                                 'code': status.HTTP_400_BAD_REQUEST,
                                 'message': 'Only clients can create projects'}, status=status.HTTP_400_BAD_REQUEST)
        
            if user.steps:
                return Response({'status': False,
                                 'code': status.HTTP_400_BAD_REQUEST,
                                 'message': 'User has already completed the onboarding process'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ProjectSerializer(data=request.data)
            serializer.is_valid(exception=True)
            serializer.save(user=user)
            user.steps = True
            user.save()
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response


class ProjectListCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer

    def get(self, request):
        try:
            projects = Project.objects.filter(
                Q(user=request.user) | Q(crew_profiles=request.user)
            ).distinct()
            serializer = ProjectSerializer(projects, many=True)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def post(self, request):
        try:
            serializer = ProjectSerializer(data=request.data)
            serializer.is_valid(exception=True)
            serializer.save(user=request.user)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

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
        try:
            project = self.get_object(pk, request.user)
            serializer = ProjectSerializer(project)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def put(self, request, pk):
        try:
            project = self.get_object(pk, request.user)
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            serializer.is_valid(exception=True)
            serializer.save()
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def delete(self, request, pk):
        try:
            project = self.get_object(pk, request.user)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response
    

class SendOnboardRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnboardRequestSerializer

    def post(self, request):
        try:
            project_id = request.data.get('project_id')
            user_id = request.data.get('user_id')

            # Check if the project and user exist
            project = Project.objects.get(project_id=project_id)
            user = User.objects.get(id=user_id)

            # Create an onboarding request
            onboard_request = OnboardRequest.objects.create(project=project, user=user)

            serializer = OnboardRequestSerializer(onboard_request)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response
    
    
class UpdateOnboardRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnboardRequestSerializer

    def patch(self, request, pk):
        try:
            onboard_request = OnboardRequest.objects.get(pk=pk)

            status2 = request.data.get('status')
            if status2 not in ['accepted', 'declined']:
                return Response({'status': False,
                                 'code': status.HTTP_400_BAD_REQUEST,
                                 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
            print(onboard_request.status)

            onboard_request.status = status2
            onboard_request.save()

            if status2 == 'accepted':
                onboard_request.project.crew_profiles.add(onboard_request.user)

            serializer = OnboardRequestSerializer(onboard_request)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

class PendingOnboardRequestsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnboardRequestSerializer

    def get(self, request):
        try:
            user = request.user
            onboard_requests = OnboardRequest.objects.filter(user=user, status='pending')
            serializer = OnboardRequestSerializer(onboard_requests, many=True)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response
    
class OnboardRequestsByProjectView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OnboardRequestsByProjectSerializer

    def get(self, request, project_id):
        try:
            project = Project.objects.get(project_id=project_id)
            serializer = OnboardRequestsByProjectSerializer(project)
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

        
class CrewListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer 

    def get(self, request, project_id):
        try:
            project = Project.objects.get(project_id=project_id)
            crew_profiles = project.crew_profiles.all()
        
            serializer = UserSerializer(crew_profiles, many=True)
        
            data = {
                'message': 'Success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response
    