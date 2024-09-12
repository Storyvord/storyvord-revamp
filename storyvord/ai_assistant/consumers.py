import json
import httpx
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatMessage, UserContext  # Add models for storing chat and context data
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async  # Import this for async DB operations

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract token from the query string
        token = self.scope['query_string'].decode().split('=')[-1]
        print(f"Received token: {token}")
        
        # Validate and authenticate user
        try:
            access_token = AccessToken(token)
            user = await self.get_user(access_token['user_id'])  # Use the async wrapper
            self.scope['user'] = user  # Set the authenticated user in the scope
        except Exception as e:
            self.scope['user'] = AnonymousUser()  # Set as AnonymousUser if authentication fails
            print(f"Authentication error: {e}")
        
        # Check if the user is authenticated
        if not self.scope['user'].is_authenticated:
            await self.close()
        else:
            await self.accept()  # Accept the connection if authenticated
            
            
    async def get_user(self, user_id):
        """
        Asynchronously fetch the user from the database.
        """
        return await database_sync_to_async(User.objects.get)(id=user_id)
            
            
    async def disconnect(self, close_code):
        # Handle user disconnect if necessary
        pass

    async def receive(self, text_data):
        if self.scope['user'].is_anonymous:
            await self.send(json.dumps({'error': 'Authentication required'}))
            return
        
        data = json.loads(text_data)
        user_message = data.get('message', '')

        if not user_message:
            await self.send(text_data=json.dumps({
                'error': 'Message is required'
            }))
            return

        # Fetch or initialize user-specific context
        user_context = await self.get_user_context(self.scope['user'].id)

        # Call the AI model API with the user context
        try:
            ai_response = await self.get_ai_response(user_message, user_context)
        except httpx.RequestError as e:
            await self.send(json.dumps({'error': str(e)}))
            return

        # Save the chat message
        await ChatMessage.objects.acreate(user=self.scope['user'], user_message=user_message, ai_response=ai_response)

        # Update user context with the latest interaction
        await self.update_user_context(self.scope['user'].id, user_message, ai_response)

        # Send the AI response back to the client
        await self.send(text_data=json.dumps({
            'user_message': user_message,
            'ai_response': ai_response
        }))
    async def get_ai_response(self, user_message, user_context):
        headers = {'Authorization': f'Bearer {OPENAI_API_KEY}'}
        data = {
            "model": "gpt-3.5-turbo",
            "messages": user_context + [{"role": "user", "content": user_message}],
            "max_tokens": 100,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

        if response.status_code != 200:
            raise httpx.RequestError(f'API error {response.status_code}: {response.text}')

        response_json = response.json()
        ai_response = response_json.get('choices', [])[0].get('message', {}).get('content', '')
        return ai_response

    # Modify the get_user_context method
    async def get_user_context(self, user_id):
        """
        Retrieve user context from the database or cache.
        """
        # Fetch context entries asynchronously
        context_entries = await database_sync_to_async(list)(
            UserContext.objects.filter(user_id=user_id).order_by('-timestamp')[:10]
        )

        # Build the context list from the retrieved entries
        context = [{"role": "user", "content": entry.user_message} for entry in context_entries]
        context += [{"role": "assistant", "content": entry.ai_response} for entry in context_entries]
        context.reverse()  # Reverse to maintain the correct order of messages
        return context

    async def update_user_context(self, user_id, user_message, ai_response):
        """
        Update the user's context in the database or cache.
        """
        await UserContext.objects.acreate(
            user_id=user_id,
            user_message=user_message,
            ai_response=ai_response
        )
