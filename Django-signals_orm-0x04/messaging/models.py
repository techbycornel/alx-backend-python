from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # New fields for Task 1
    edited = models.BooleanField(default=False)  # track if a message has been edited
    edited_at = models.DateTimeField(null=True, blank=True)  # when the edit happened
    edited_by = models.ForeignKey(
        User, related_name="edited_messages", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID {self.message.id}"


class MessageHistory(models.Model):
    """Stores the old content of a message before edit."""
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User, related_name="message_history", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"History of Message {self.message.id} edited at {self.edited_at}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        User, related_name="edited_messages", null=True, blank=True, on_delete=models.SET_NULL
    )

    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"
