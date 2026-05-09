# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await sync_to_async(list)(
            ChatMessage.objects.filter(room_name=self.room_name).order_by('timestamp').all()[:50]
        )
        for msg in messages:
            await self.send(text_data=json.dumps({
                "type": "chat_message",
                "message": msg.message,
                "username": msg.username,
                "timestamp": msg.timestamp.strftime("%I:%M %p")
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type', 'chat_message')
        
        # Add sender's channel name to the data for targeting later
        data['sender_channel'] = self.channel_name
        
        # Forward the entire payload to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'broadcast_message', # A single handler for broadcasting
                'data': data
            }
        )

    async def broadcast_message(self, event):
        message_data = event['data']
        sender_channel = message_data.get('sender_channel')
        message_type = message_data.get('type')
        
        # Don't send initiation signals back to the sender
        if self.channel_name != sender_channel or message_type in ['offer', 'answer', 'candidate', 'end_call']:
            # Special logic for call initiation signals to avoid self-ringing
            if message_type in ['make_call', 'cancel_call', 'decline_call']:
                 if self.channel_name == sender_channel:
                    return # Don't send these to the original sender
            
            await self.send(text_data=json.dumps(message_data))
        
        # Always save chat messages
        if message_type == 'chat_message':
             await sync_to_async(ChatMessage.objects.create)(
                room_name=self.room_name,
                username=message_data['username'],
                message=message_data['message']
            )