from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import * 
from .serializers import *

class AddressBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressBookSerializer
    def get(self, request, pk=None):
        if pk:
            try:
                address = AddressBook.objects.get(pk=pk, company__user=request.user)
                serializer = AddressBookSerializer(address)
                return Response(serializer.data)
            except AddressBook.DoesNotExist:
                return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all addresses for the user's company
        addresses = AddressBook.objects.filter(company__user=request.user)
        serializer = AddressBookSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressBookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            address = AddressBook.objects.get(pk=pk, company__user=request.user)
        except AddressBook.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressBookSerializer(address, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            address = AddressBook.objects.get(pk=pk, company__user=request.user)
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AddressBook.DoesNotExist:
            return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

class CompanyTaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def get(self, request):
        tasks = ClientCompanyTask.objects.filter(created_by=request.user)
        serializer = CompanyTaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CompanyTaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                task = serializer.save()
                return Response(CompanyTaskSerializer(task).data, status=status.HTTP_201_CREATED)
            except serializers.ValidationError as e:
                custom_errors = self.format_validation_errors(e.detail)
                return Response({'errors': custom_errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def format_validation_errors(self, errors):
        formatted_errors = {}
        for field, messages in errors.items():
            if isinstance(messages, list):
                formatted_errors[field] = ' '.join(messages)
            else:
                formatted_errors[field] = messages
        return formatted_errors

class CompanyTaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def get_object(self, pk):
        try:
            return ClientCompanyTask.objects.get(pk=pk, created_by=self.request.user)
        except ClientCompanyTask.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = CompanyTaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = CompanyTaskSerializer(task, data=request.data, context={'request': request})
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
            task = ClientCompanyTask.objects.get(pk=pk, assigned_to=request.user)
        except ClientCompanyTask.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        task.completion_requested = True
        task.requester = request.user
        task.save()

        serializer = TaskCompletionRequestSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskCompletionApprovalView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def post(self, request, pk, format=None):
        try:
            task = ClientCompanyTask.objects.get(pk=pk, created_by=request.user)
        except ClientCompanyTask.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if not task.completion_requested:
            return Response({"error": "No completion request found for this task."}, status=status.HTTP_400_BAD_REQUEST)

        task.completed = True
        task.completion_requested = False
        task.requester = None
        task.save()

        serializer = CompanyTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskPendingToApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = ClientCompanyTask.objects.filter(created_by=request.user, completion_requested=True)
        serializer = CompanyTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeTaskListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def get(self, request, format=None):
        tasks = ClientCompanyTask.objects.filter(assigned_to=request.user)
        serializer = CompanyTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeTaskDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def get(self, request, pk, format=None):
        try:
            task = ClientCompanyTask.objects.get(pk=pk, assigned_to=request.user)
        except ClientCompanyTask.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanyTaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeeListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            client_profile = ClientProfile.objects.get(user=request.user)
            employees = client_profile.employee_profile.all()
            serializer = UserSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientProfile.DoesNotExist:
            return Response({"detail": "Client profile does not exist for the current user."}, status=status.HTTP_404_NOT_FOUND)