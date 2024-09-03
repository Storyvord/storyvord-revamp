import json
from channels.generic.websocket import AsyncWebsocketConsumer
from inbox.models import DialogsModel, MessageModel
from accounts.models import User
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract access token from the query string
        query_string = self.scope.get('query_string').decode("utf-8")
        access_token = self._get_query_param(query_string, 'access_token')
        
        print(access_token)

        # Authenticate user using the access token
        self.user = await self.get_user_from_token(access_token)

        if self.user is None:
            # If the user is not authenticated, close the connection
            await self.close()
        else:
            self.recipient_id = self.scope["url_route"]["kwargs"]["user_id"]
            self.room_group_name = f'chat_{self.user.id}_{self.recipient_id}'

            # Join the room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        if self.user.is_authenticated:
            # Save the message to the database
            recipient = await database_sync_to_async(User.objects.get)(id=self.recipient_id)
            new_message = await database_sync_to_async(MessageModel.objects.create)(
                sender=self.user,
                recipient=recipient,
                text=message
            )

            # Send the message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': str(self.user.id)  # Use the user's ID
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    def _get_query_param(self, query_string, param):
        params = dict(p.split('=') for p in query_string.split('&'))
        return params.get(param, None)

    @database_sync_to_async
    def get_user_from_token(self, access_token):
        # Implement your token validation and user retrieval logic here
        try:
            token = AccessToken(access_token)
            user_id = token.payload['user_id']
            return User.objects.get(id=user_id)
        except (User.DoesNotExist, KeyError):
            return None