from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - User must be authenticated
    - Only participants of a conversation can view, send, update, or delete messages
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For message objects → check conversation participants
        if hasattr(obj, "conversation"):
            participants = obj.conversation.participants.all()
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return request.user in participants
            return request.user in participants

        # For conversation objects → check participants
        if hasattr(obj, "participants"):
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return request.user in obj.participants.all()
            return request.user in obj.participants.all()

        return False
