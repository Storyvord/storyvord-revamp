from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers import UserProfileSerializer
from accounts.models import User
from client.models import ClientProfile 
from crew.models import CrewProfile

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        user_data = {
            'user': user,
            'profile': self.get_profile(user)
        }
        serializer = UserProfileSerializer(user_data)
        return Response(serializer.data)

    def get_profile(self, user):
        if user.user_type == 'client':
            return ClientProfile.objects.filter(user=user).first()
        elif user.user_type == 'crew':
            return CrewProfile.objects.filter(user=user).first()
        return None
