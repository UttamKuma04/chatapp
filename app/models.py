from django.db import models
from django.contrib.auth.models import AbstractUser

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default="Anonymous")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.room_name}] {self.username}: {self.message}"



    
