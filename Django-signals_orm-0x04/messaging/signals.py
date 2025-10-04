from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Task 0: Create notification when a new message is sent"""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Task 1: Log old content before a message is updated"""
    if instance.pk:  # only if message already exists (update, not create)
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        if old_message.content != instance.content:
            # Save old content in MessageHistory
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content,
                edited_by=instance.edited_by  # who made the edit
            )
            # Mark message as edited
            instance.edited = True
            instance.edited_at = timezone.now()

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """Task 2: Clean up related data when a user is deleted"""
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories associated with this user
    MessageHistory.objects.filter(edited_by=instance).delete()
