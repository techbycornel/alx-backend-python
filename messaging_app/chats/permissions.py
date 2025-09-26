from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to access or modify its messages.
    """

    def has_object_permission(self, request, view, obj):
        # For messages, check if user is sender or in conversation participants
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        # For conversations, check if user is a participant
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        return False
