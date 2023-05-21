from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.utils import timezone

from .models import Conversation, Message, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['id']
        self.conversation_group_name = f'conversation_{self.conversation_id}'

        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        if action == 'message':
            message = data['message']
            user = data.get('user')
            await self.send_message(message, user)


    async def send_message(self, message,user):
        conversation = await self.get_conversation()
        if conversation:
            sender = await self.get_user(user['user_id'])
            await self.create_message(conversation, sender, message)
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    'type': 'chat_message',
                    'sender': {
                    'user_id': sender.user_id,
                    'user_name': sender.user_name,
                    'user_image': sender.user_image,
                    },
                    'message': message,
                    'created_at': timezone.now().isoformat(),
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender': event['sender'],
            'message': event['message'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def get_conversation(self):
        try:
            return Conversation.objects.get(id=self.conversation_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, conversation, sender, message):
        Message.objects.create(
            conversation=conversation,
            sender=sender,
            message=message
        )
