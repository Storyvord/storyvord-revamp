from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import * 
from .serializers import *
from storyvord.exception_handlers import custom_exception_handler

class AddressBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressBookSerializer
    def get(self, request, pk=None):
        try:
            if pk:
                address = AddressBook.objects.get(pk=pk, company__user=request.user)
                serializer = AddressBookSerializer(address)
                data = {
                    "message": "Success",
                    "data": serializer.data
                }
                return Response(data)
            # except AddressBook.DoesNotExist:
                # return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)

            # Get all addresses for the user's company
            addresses = AddressBook.objects.filter(company__user=request.user)
            serializer = AddressBookSerializer(addresses, many=True)
            data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(data)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def post(self, request):
        try:
            serializer = AddressBookSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    "message": "Success",
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)
            data = {
                "message": "Error",
                "data": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def put(self, request, pk):
        try:
            address = AddressBook.objects.get(pk=pk, company__user=request.user)

            serializer = AddressBookSerializer(address, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    "message": "Success",
                    "data": serializer.data
                }
                return Response(data)
            data = {
                "message": "Error",
                "data": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def delete(self, request, pk):
        try:
            address = AddressBook.objects.get(pk=pk, company__user=request.user)
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

class CompanyTaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def get(self, request):
        try:
            tasks = ClientCompanyTask.objects.filter(created_by=request.user)
            serializer = CompanyTaskSerializer(tasks, many=True)
            return Response(serializer.data)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def post(self, request):
        try:
            serializer = CompanyTaskSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                task = serializer.save()
                data = {
                    "message": "Success",
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)
            data = {
                "message": "Error",
                "data": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

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
        try:
            task = self.get_object(pk)
            serializer = CompanyTaskSerializer(task)
            return Response(serializer.data)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def put(self, request, pk):
        try:
            task = self.get_object(pk)
            serializer = CompanyTaskSerializer(task, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    "message": "Success",
                    "data": serializer.data
                }
                return Response(data)
            data = {
                "message": "Error",
                "data": serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

    def delete(self, request, pk):
        try:
            task = self.get_object(pk)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response


class TaskCompletionRequestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskCompletionRequestSerializer

    def post(self, request, pk, format=None):
        try:
            task = ClientCompanyTask.objects.get(pk=pk, assigned_to=request.user)

            task.completion_requested = True
            task.requester = request.user
            task.save()

            serializer = TaskCompletionRequestSerializer(task)
            data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response


class TaskCompletionApprovalView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def post(self, request, pk, format=None):
        try:
            task = ClientCompanyTask.objects.get(pk=pk, created_by=request.user)
            task.completed = True
            task.completion_requested = False
            task.requester = None
            task.save()

            serializer = CompanyTaskSerializer(task)
            data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response


class TaskPendingToApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = ClientCompanyTask.objects.filter(created_by=request.user, completion_requested=True)
            serializer = CompanyTaskSerializer(tasks, many=True)
            data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response 


class EmployeeTaskListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def get(self, request, format=None):
        try:
            tasks = ClientCompanyTask.objects.filter(assigned_to=request.user)
            serializer = CompanyTaskSerializer(tasks, many=True)
            data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response


class EmployeeTaskDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanyTaskSerializer

    def get(self, request, pk, format=None):
        try:
            task = ClientCompanyTask.objects.get(pk=pk, assigned_to=request.user)

            serializer = CompanyTaskSerializer(task)
            data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response

class EmployeeListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            client_profile = ClientProfile.objects.get(user=request.user)
            employees = client_profile.employee_profile.all()
            serializer = UserSerializer(employees, many=True)
            data = {
                "message": "Success",
                "data": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response
        

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            file_serializer = UploadedFileSerializer(data=request.data)
            print(file_serializer)
            if file_serializer.is_valid():
                file_serializer.save()
                data = {
                    "message": "Success",
                    "data": file_serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)
            data = {
                "message": "Error",
                "data": file_serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            response = custom_exception_handler(exc, self.get_renderer_context())
            return response