from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai_assistant.models import ChatMessage
from ai_assistant.serializers import ChatMessageSerializer
import requests
import os
from openai import OpenAI
client = OpenAI()

OPENAI_API_KEY=os.environ['OPENAI_API_KEY'] 

class ChatAPIView(APIView):
    def post(self, request):
        user_message = request.data.get('message')
        print(user_message)
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 50
        }
        print(data)
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "I need you to act as a line producer with expertise in local locations, compliance issues, and cultural nuances. You have a strong understanding of the risks involved in film production, especially related to location-specific factors. You are also skilled in budgeting for films, including compliance costs, and creating detailed itineraries to ensure compliance. Your knowledge covers locations worldwide, from big cities to small towns in every country. Given this expertise, provide advice using critical thinking based on further details I will provide, such as crew size, equipment (like cameras), and the type of shoot (indoor, outdoor, corporate, or blog). Offer two options when appropriate. Your response should include a comprehensive overview, and feel free to ask questions to better understand my production needs."},
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            
            ai_response = completion.choices[0].message
            
        except requests.Timeout:
            return Response({'error': 'Timed out when calling the OpenAI API'}, status=status.HTTP_408_REQUEST_TIMEOUT)
        except requests.HTTPError as e:
            if e.response.status_code >= 400:
                return Response({'error': 'You have exceeded your daily quota for the day'}, status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response({'error': 'Something went wrong when calling the OpenAI API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save the chat message
        chat_message = ChatMessage.objects.create(user_message=user_message, ai_response=ai_response.content)
        serializer = ChatMessageSerializer(chat_message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
