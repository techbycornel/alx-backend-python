from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to ensure:
    - User is authenticated
    - User is a participant of the conversation to view, send,
      update, or delete messages
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For message objects → check if user is in the conversation participants
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        # For conversation objects → check if user is a participant
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        return False
