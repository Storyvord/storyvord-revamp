# views.py

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project, Task
from .serializers import *
from rest_framework.permissions import IsAuthenticated

class TaskListCreateAPIView(APIView):
    def get(self, request, project_pk):
        tasks = Task.objects.filter(project_id=project_pk)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_pk):
        data = request.data.copy()
        data['project'] = project_pk
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailAPIView(APIView):
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

    def post(self, request, pk, format=None):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != task.assigned_to:
            return Response({"error": "You are not assigned to this task."}, status=status.HTTP_403_FORBIDDEN)

        if request.user.user_type != 'crew':
            return Response({"error": "Only crew members can request task completion."}, status=status.HTTP_403_FORBIDDEN)

        task.completion_requested = True
        task.requester = request.user
        task.save()

        serializer = TaskCompletionRequestSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TaskCompletionApprovalView(APIView):
    permission_classes = [IsAuthenticated]

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
    
class CrewTaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Ensure the user is a crew member
        if request.user.user_type != 'crew':
            return Response({"error": "Only crew members can view their tasks."}, status=status.HTTP_403_FORBIDDEN)
        
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CrewTaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

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