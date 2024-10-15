from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models import ProjectTask
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
        project_id = request.query_params.get('project', None)
        logger.debug(f'Project ID: {project_id}')
        if project_id:
            tasks = self.queryset.filter(project=project_id)
        else:
            tasks = self.queryset.all()  
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    
    # Retrieve a single task
    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    # Delete a task
    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
