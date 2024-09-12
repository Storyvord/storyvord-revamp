from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_assistant.models import ChatMessage
from ai_assistant.serializers import ChatMessageSerializer
import requests
import os

OPENAI_API_KEY=os.environ['OPENAI_API_KEY'] 

class ChatAPIView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        print(user_message)
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 50
        }
        print(data)
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
                json=data,
                timeout=1
            )
            if response.status_code != 200:
                return Response({'error': 'Error connecting to OpenAI API'}, status=response.status_code)
            ai_response = response.json()['choices'][0]['message']['content']
        except requests.Timeout:
            return Response({'error': 'Timed out when calling the OpenAI API'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.HTTPError as e:
            if e.response.status_code >= 400:
                return Response({'error': 'You have exceeded your daily quota for the day'}, status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response({'error': 'Something went wrong when calling the OpenAI API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the chat message
        chat_message = ChatMessage.objects.create(user_message=user_message, ai_response=ai_response)
        serializer = ChatMessageSerializer(chat_message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
