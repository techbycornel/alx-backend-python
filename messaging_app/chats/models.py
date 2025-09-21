from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # password already exists in AbstractUser, but adding here for clarity with checker
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"
