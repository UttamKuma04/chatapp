# chat/admin.py
from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("room_name", "username", "message", "timestamp")
    list_filter = ("room_name", "username", "timestamp")
    search_fields = ("room_name", "username", "message")
    ordering = ("-timestamp",)
