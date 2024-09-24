import json
import httpx
import os
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatMessage, ChatSession  # Add models for storing chat and context data
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async  # Import this for async DB operations
import uuid
from openai import OpenAI
import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = OpenAI()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
User = get_user_model()

class AIChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract query string parameters (token and session_id)
        query_params = dict(qc.split("=") for qc in self.scope['query_string'].decode().split("&"))
        token = query_params.get('token')
        session_id = query_params.get('session_id')
        
        # Validate and authenticate user
        try:
            access_token = AccessToken(token)
            user = await self.get_user(access_token['user_id'])  # Use the async wrapper
            self.scope['user'] = user  # Set the authenticated user in the scope
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            self.scope['user'] = AnonymousUser()  # Set as AnonymousUser if authentication fails            
        
        # Check if the user is authenticated
        if not self.scope['user'].is_authenticated:
            await self.close()
        else:
            # Use provided session ID if it exists, otherwise generate a new one
            self.session_id = session_id if session_id else str(uuid.uuid4())

            # Check for existing session or create a new one
            try:
                await self.create_chat_session(self.scope['user'], self.session_id)
            except ValueError as e:
                await self.close()  # Close the connection if there's a session conflict
                return

            await self.accept()  # Accept the connection if authenticated and session created successfully
     
    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with code: {close_code}")    

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

        # Generate the embedding for the user message
        user_message_embedding,embedding_cost = await self.generate_embedding(user_message)
        
         # Retrieve relevant messages based on embeddings
        relevant_context = await self.get_relevant_messages(self.session_id, user_message_embedding)

        # Call the AI model API with the relevant context
        try:
            ai_response,input_tokens,output_tokens,response_cost = await self.get_ai_response(user_message, relevant_context)
            total_cost = embedding_cost + response_cost
            logger.info(f"Tokens used - Input: {input_tokens}, Output: {output_tokens}, Total Cost: ${total_cost:.4f}")
        except Exception as e:
            await self.send(json.dumps({'error': str(e)}))
            return

        # Save the chat message
        await self.save_chat_message(self.session_id, user_message, ai_response, user_message_embedding)

        await self.send(text_data=json.dumps({
            'user_message': user_message,
            'ai_response': ai_response,
            'cost': total_cost
        }))
        
    async def get_ai_response(self,user_message,context):
        # Include the context in the prompt
        messages = [{"role": "system", "content": "I need you to act as a line producer with expertise in local locations, compliance issues, and cultural nuances. You have a strong understanding of the risks involved in film production, especially related to location-specific factors. You are also skilled in budgeting for films, including compliance costs, and creating detailed itineraries to ensure compliance. Your knowledge covers locations worldwide, from big cities to small towns in every country. Given this expertise, provide advice using critical thinking based on further details I will provide, such as crew size, equipment (like cameras), and the type of shoot (indoor, outdoor, corporate, or blog). Offer two options when appropriate. Your response should include a comprehensive overview, and feel free to ask questions to better understand my production needs."}] + context
        messages.append({"role": "user", "content": user_message})
        
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        ai_response = completion.choices[0].message
        input_tokens = completion.usage.total_tokens
        output_tokens = completion.usage.total_tokens
        response_cost = (input_tokens * 0.00000015) + (output_tokens * 0.00000060)

        logger.info(f"AI response: {ai_response.content}")
        return ai_response.content, input_tokens, output_tokens, response_cost
    
    async def generate_embedding(self, text):
        # Call OpenAI's embeddings API to get the embedding for the text
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        
        cost_per_token = 0.00000002  # Replace with actual cost per token for embeddings
        tokens_used = response.usage.total_tokens
        cost = tokens_used * cost_per_token

        # Log the cost
        logger.info(f"Tokens used for embedding: {tokens_used}, Cost: ${cost:.4f}")
        
         # Extract the embedding based on the actual structure of the response
        if len(response.data) > 0 and hasattr(response.data[0], 'embedding'):
            return response.data[0].embedding , cost
        else:
            # Handle cases where the structure might be different
            raise ValueError("Response object does not contain 'embedding' attribute or is empty.")
    
    @database_sync_to_async
    def get_relevant_messages(self, session_id, embedding):
        # Retrieve the last 10 messages for this session
        session = ChatSession.objects.get(session_id=session_id)
        messages = ChatMessage.objects.filter(session=session)

        # Calculate similarity scores between the new message embedding and the stored embeddings
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # Convert JSONField embedding to a list of floats
        messages_with_similarity = [
            (msg, cosine_similarity(embedding, json.loads(msg.embedding)))
            for msg in messages
        ]

        # Sort messages by similarity score
        relevant_messages = sorted(messages_with_similarity, key=lambda x: x[1], reverse=True)[:10]

        # Build context
        context = []
        for msg, _ in relevant_messages:
            context.append({"role": "user", "content": msg.user_message})
            context.append({"role": "assistant", "content": msg.ai_response})

        return context


    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def create_chat_session(self, user, session_id):
         # Check if the session already exists
        session, created = ChatSession.objects.get_or_create(
            session_id=session_id,
            defaults={'user': user}  # Only set user if a new session is created
        )
            # If the session already exists and belongs to a different user, handle this case
        if not created and session.user != user:
            raise ValueError("Session ID is already in use by a different user.")

    @database_sync_to_async
    def save_chat_message(self, session_id, user_message, ai_response, embedding):
        session = ChatSession.objects.get(session_id=session_id)
        ChatMessage.objects.create(
            user=self.scope['user'],
            session=session, 
            user_message=user_message, 
            ai_response=ai_response,
            embedding=json.dumps(embedding)  # Store embedding as JSON
        )