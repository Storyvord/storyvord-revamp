from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import AddressBook
from .serializers import AddressBookSerializer

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
