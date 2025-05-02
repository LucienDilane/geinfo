# messaging/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from Etudiants.models import Etudiant
from .models import Echange

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        self.room_group_name = f"chat_{self.scope['user'].id}_{self.receiver_id}"

        # Rejoindre un groupe de canal spécifique à la conversation
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Quitter le groupe de canal
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recevoir un message du WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_id = text_data_json['receiver_id']

        # Enregistrer le message dans la base de données
        receiver = await self.get_user(receiver_id)
        await self.save_message(self.scope['user'], receiver, message)

        # Envoyer le message au groupe de canal
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.scope['user'].id,
                'timestamp': str(await self.get_current_timestamp()),
            }
        )

    # Recevoir un message du groupe de canal
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        timestamp = event['timestamp']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'timestamp': timestamp,
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return Etudiant.objects.get(id=user_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        Echange.objects.create(sender=sender, receiver=receiver, content=content)

    @database_sync_to_async
    def get_current_timestamp(self):
        from django.utils import timezone
        return timezone.now()