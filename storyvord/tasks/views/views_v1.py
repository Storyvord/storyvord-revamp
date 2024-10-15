# views.py

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Project, Task
from ..serializers.serializers_v1 import *
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request, project_pk):
        tasks = Task.objects.filter(project_id=project_pk)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_pk):
        data = request.data.copy()
        
        # Pass the project_pk to the serializer context
        serializer = TaskSerializer(data=data, context={'request': request, 'project_pk': project_pk})
        if serializer.is_valid():
            try:
                task = serializer.save()
                return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                # Handle validation error from the serializer
                custom_errors = self.format_validation_errors(e.detail)
                return Response({'errors': custom_errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def format_validation_errors(self, errors):
        """
        Custom method to format validation errors.
        """
        formatted_errors = {}
        for field, messages in errors.items():
            if isinstance(messages, list):
                formatted_errors[field] = ' '.join(messages)
            else:
                formatted_errors[field] = messages
        return formatted_errors



class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCompletionRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCompletionRequestSerializer

    def post(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != task.assigned_to:
            return Response({"error": "You are not assigned to this task."}, status=status.HTTP_403_FORBIDDEN)

        if request.user.user_type != '2':
            return Response({"error": "Only crew members can request task completion."}, status=status.HTTP_403_FORBIDDEN)

        task.completion_requested = True
        task.requester = request.user
        task.save()

        serializer = TaskCompletionRequestSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskCompletionApprovalView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def post(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != task.created_by:
            return Response({"error": "You are not authorized to approve this task completion."}, status=status.HTTP_403_FORBIDDEN)

        if not task.completion_requested:
            return Response({"error": "No completion request found for this task."}, status=status.HTTP_400_BAD_REQUEST)

        task.completed = True
        task.completion_requested = False
        task.requester = None
        task.save()

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

        
class TaskPendingToApprovalView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, project_pk):
        tasks = Task.objects.filter(project=project_pk ,created_by=request.user, completion_requested=True)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CrewTaskListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request, format=None):
        # Ensure the user is a crew member
        if request.user.user_type != '2':
            return Response({"error": "Only crew members can view their tasks."}, status=status.HTTP_403_FORBIDDEN)
        
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CrewTaskDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the task is assigned to the requesting user
        if task.assigned_to != request.user:
            return Response({"error": "You are not assigned to this task."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)