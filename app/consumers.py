# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Import models inside async method
        from .models import ChatMessage

        # Send last 50 messages
        messages = await sync_to_async(list)(
            ChatMessage.objects.filter(room_name=self.room_name)
            .order_by('-timestamp')[:50]
        )
        for msg in reversed(messages):
            await self.send(text_data=json.dumps({
                "message": msg.message,
                "username": msg.username,
                # Format timestamp like "2025-09-26 18:07"
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M")
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
            return

        message = data.get("message")
        username = data.get("username", "Anonymous")

        if not message:
            await self.send(text_data=json.dumps({"error": "No message provided"}))
            return

        from .models import ChatMessage

        # Save message
        msg_obj = await sync_to_async(ChatMessage.objects.create)(
            room_name=self.room_name,
            username=username,
            message=message
        )

        # Broadcast
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "timestamp": msg_obj.timestamp.strftime("%Y-%m-%d %H:%M")
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
            "timestamp": event.get("timestamp")  # already formatted
        }))
