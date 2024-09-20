import json
from channels.generic.websocket import AsyncWebsocketConsumer
from inbox.models import DialogsModel, InboxGroup, InboxMessage, MessageModel
from accounts.models import User
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.core.cache import cache
import json
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract access token from the query string
        query_string = self.scope.get('query_string').decode("utf-8")
        access_token = self._get_query_param(query_string, 'access_token')
        
        # Authenticate user using the access token
        self.user = await self.get_user_from_token(access_token)

        if self.user is None:
            # If the user is not authenticated, close the connection
            await self.close()
        else:
            # Get the recipient's user ID from the URL
            self.recipient_id = self.scope["url_route"]["kwargs"]["user_id"]

            # Create a consistent room name regardless of the sender-recipient order
            self.room_group_name = f'chat_{min(self.user.id, self.recipient_id)}_{max(self.user.id, self.recipient_id)}'

            # Mark user as online in in-memory cache
            await self.set_user_online(self.user.id)

            # Notify other users in the group that this user is online
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_status',
                    'user_id': str(self.user.id),
                    'status': 'online'
                }
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Mark user as offline in in-memory cache
        await self.set_user_offline(self.user.id)

        # Notify other users that this user is offline
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_status',
                'user_id': str(self.user.id),
                'status': 'offline'
            }
        )

        # Leave the room group when the WebSocket is disconnected
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Check the type of message received (either 'chat', 'typing', or 'status')
        if 'message' in data:
            message = data['message']

            if self.user.is_authenticated:
                # Save the message to the database
                recipient = await database_sync_to_async(User.objects.get)(id=self.recipient_id)
                new_message = await database_sync_to_async(MessageModel.objects.create)(
                    sender=self.user,
                    recipient=recipient,
                    text=message
                )

                # Send the message to the room group with detailed user info
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender': await self.get_user_info(self.user.id),
                        'recipient': await self.get_user_info(self.recipient_id),
                        'you': True
                    }
                )
        elif 'typing' in data:
            # Handle typing event
            typing_status = data['typing']

            # Send typing event to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_status',
                    'typing': typing_status,
                    'sender': await self.get_user_info(self.user.id),
                    'you': True
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        recipient = event['recipient']
        you = event['you']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recipient': recipient,
            # 'you': you
        }))

    async def typing_status(self, event):
        typing = event['typing']
        sender = event['sender']
        you = event['you']

        # Send the typing status to the WebSocket
        await self.send(text_data=json.dumps({
            'typing': typing,
            'sender': sender,
            'you': you
        }))

    async def online_status(self, event):
        user_id = event['user_id']
        status = event['status']

        # Send the online/offline status to the WebSocket
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': status
        }))

    def _get_query_param(self, query_string, param):
        params = dict(p.split('=') for p in query_string.split('&'))
        return params.get(param, None)

    @database_sync_to_async
    def get_user_from_token(self, access_token):
        # Implement token validation and user retrieval logic here
        try:
            token = AccessToken(access_token)
            user_id = token.payload['user_id']
            return User.objects.get(id=user_id)
        except (User.DoesNotExist, KeyError):
            return None

    @database_sync_to_async
    def set_user_online(self, user_id):
        # Set user as online in in-memory cache
        cache.set(f'user_{user_id}_online', True)

    @database_sync_to_async
    def set_user_offline(self, user_id):
        # Set user as offline in in-memory cache
        cache.set(f'user_{user_id}_online', False)

    @database_sync_to_async
    def is_user_online(self, user_id):
        # Check if a user is online from in-memory cache
        return cache.get(f'user_{user_id}_online', False)

    @database_sync_to_async
    def get_user_info(self, user_id):
        """
        Fetch user details and format as needed for WebSocket messages.
        """
        try:
            user = User.objects.get(id=user_id)
            return {
                'id': user.id,
                'email': user.email,
                'user_type': user.user_type,
                'name': self.get_user_name(user),
                'you': user_id == self.user.id
            }
        except User.DoesNotExist:
            return None

    def get_user_name(self, user):
        """
        Get the name of the user based on their profile.
        """
        if user.user_type == 'client':
            profile = getattr(user, 'clientprofile', None)
            return f"{profile.firstName} {profile.lastName}" if profile else None
        elif user.user_type == 'crew':
            profile = getattr(user, 'crewprofile', None)
            return profile.name if profile else None
        return None


# chat/consumers.py


User = get_user_model()  # Get the custom user model

class InboxChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get group_id from URL route
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'chat_{self.group_id}'

        # Extract access token from query string (ws://localhost:8000/ws/chat/<group_id>/?token=<JWT_TOKEN>)
        query_string = self.scope['query_string'].decode('utf8')
        access_token = self._get_query_param(query_string, 'token')

        # Authenticate user using the token
        self.user = await self.get_user_from_token(access_token)

        if self.user is None:
            # If token is invalid or user not authenticated, close the connection
            await self.close()
        else:
            # Mark user as online in in-memory cache
            await self.set_user_online(self.user.id)

            # Notify group that this user is online
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'online_status',
                    'user_id': str(self.user.id),
                    'status': 'online'
                }
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Mark user as offline in in-memory cache
        await self.set_user_offline(self.user.id)

        # Notify other users that this user is offline
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'online_status',
                'user_id': str(self.user.id),
                'status': 'offline'
            }
        )

        # Leave the group on disconnect
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Handle different message types: chat message, typing status
        if 'message' in data:
            message = data['message']

            if self.user.is_authenticated:
                # Save the message to the database asynchronously
                await self.save_message(self.user, self.group_id, message)

                # Send the message to the group
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender': await self.get_user_info(self.user.id),
                        'recipient_group': self.group_id,
                    }
                )
        elif 'typing' in data:
            typing_status = data['typing']

            # Send typing event to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'typing_status',
                    'typing': typing_status,
                    'sender': await self.get_user_info(self.user.id),
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        recipient_group = event['recipient_group']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'recipient_group': recipient_group,
        }))

    async def typing_status(self, event):
        typing = event['typing']
        sender = event['sender']

        # Send the typing status to the WebSocket
        await self.send(text_data=json.dumps({
            'typing': typing,
            'sender': sender,
        }))

    async def online_status(self, event):
        user_id = event['user_id']
        status = event['status']

        # Send the online/offline status to the WebSocket
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': status
        }))

    @sync_to_async
    def save_message(self, user, group_id, message):
        group, _ = InboxGroup.objects.get_or_create(id=group_id)
        InboxMessage.objects.create(group=group, sender=user, message=message)

    @database_sync_to_async
    def get_user_from_token(self, access_token):
        # Token validation and user retrieval logic
        try:
            token = UntypedToken(access_token)
            user_id = token.payload.get('user_id')
            return User.objects.get(id=user_id)
        except (User.DoesNotExist, KeyError):
            return None

    @database_sync_to_async
    def set_user_online(self, user_id):
        # Set user as online in in-memory cache
        cache.set(f'user_{user_id}_online', True)

    @database_sync_to_async
    def set_user_offline(self, user_id):
        # Set user as offline in in-memory cache
        cache.set(f'user_{user_id}_online', False)

    @database_sync_to_async
    def get_user_info(self, user_id):
        """
        Fetch user details and format as needed for WebSocket messages.
        """
        try:
            user = User.objects.get(id=user_id)
            return {
                'id': user.id,
                'email': user.email,
                'user_type': user.user_type,
                'name': self.get_user_name(user),
            }
        except User.DoesNotExist:
            return None

    def get_user_name(self, user):
        """
        Get the name of the user based on their profile.
        """
        if user.user_type == 'client':
            profile = getattr(user, 'clientprofile', None)
            return f"{profile.firstName} {profile.lastName}" if profile else None
        elif user.user_type == 'crew':
            profile = getattr(user, 'crewprofile', None)
            return profile.name if profile else None
        return None

    def _get_query_param(self, query_string, param):
        # Parse query string and return the value of the provided parameter
        params = dict(p.split('=') for p in query_string.split('&'))
        return params.get(param, None)