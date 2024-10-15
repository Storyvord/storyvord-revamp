from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models import ProjectTask
from project.models import Membership
from django.db.models import Q
from ..serializers.serializers_v2 import ProjectTaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from storyvord.exception_handlers import custom_exception_handler
import logging

logger = logging.getLogger(__name__)

class ProjectTaskViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed
        
    # Override the initial method to add token validation
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if 'HTTP_AUTHORIZATION' not in request.META:
            logger.error("Authorization token missing")
            raise AuthenticationFailed("Authorization token is missing. Please provide a valid token.")
    
    # Create Task
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            task_instance = serializer.save()
            assigned_users = list(task_instance.assigned_to.all())
            data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Task Created successfully',
                'data': {
                    'task_id': task_instance.id,
                    'title': task_instance.title,
                    'description': task_instance.description,
                    'assigned_to': [
                        {
                            'id': membership.user.id,
                            'email': membership.user.email,
                        } for membership in assigned_users
                    ],
                    'due_date': task_instance.due_date,
                    'status': task_instance.status,
                    'is_completed': task_instance.is_completed
                }
            }
            return Response(data)
        except Exception as exc:
            logger.error(f"Error creating task: {exc}")
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response    
    # Update Task
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # List Tasks
    def list(self, request, *args, **kwargs):
        try:
            user = request.user
            tasks = self.queryset.filter(Q(assigned_to__user=user))
            data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Task Fetched successfully',
                'data': {
                    'tasks': [
                        {
                            'id': task.id,
                            'title': task.title,
                            'description': task.description,
                            'assigned_to': [
                                {
                                    'id': membership.user.id,
                                    'email': membership.user.email,
                                } for membership in task.assigned_to.all()
                            ],
                            'due_date': task.due_date,
                            'status': task.status,
                            'is_completed': task.is_completed
                        } for task in tasks
                    ]
                }
            }
            return Response(data)
        except Exception as exc:
            logger.error(f"Error getting tasks: {exc}")
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response  
        
    # Retrieve a single task
    def retrieve(self, request, *args, **kwargs):
        try:
            user = request.user
            task = self.queryset.filter(assigned_to__user=user).get(pk=kwargs['pk'])
            data = {
                'status': status.HTTP_200_OK,
                'message': 'Task Fetched successfully',
                'data': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'assigned_to': [
                        {
                            'id': membership.user.id,
                            'email': membership.user.email,
                        } for membership in task.assigned_to.all()
                    ],
                    'due_date': task.due_date,
                    'status': task.status,
                    'is_completed': task.is_completed
                }
            }
            return Response(data)
        except Exception as exc:
            logger.error(f"Error retierving task: {exc}")
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response
    
    # Delete a task
    def destroy(self, request, *args, **kwargs):
        try:
            user = request.user
            tasks = self.queryset.filter(assigned_to__user=user)
            if tasks.count() == 0:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            task = tasks.get(pk=kwargs['pk'])
            if task.assigned_by != user:
                raise Exception("You are not authorized to delete this task.")
            task.delete()
            data = {
                'status': status.HTTP_200_OK,
                'message': 'Tasks Fetched successfully',
                'data': {
                    'tasks': [
                        {
                            'id': task.id,
                            'title': task.title,
                            'description': task.description,
                            'assigned_to': [
                                {
                                    'id': membership.user.id,
                                    'email': membership.user.email,
                                } for membership in task.assigned_to.all()
                            ],
                            'due_date': task.due_date,
                            'status': task.status,
                            'is_completed': task.is_completed
                        } for task in tasks
                    ]
                }
            }
            return Response(data)
        except Exception as exc:
            logger.error(f"Error getting all tasks: {exc}")
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response