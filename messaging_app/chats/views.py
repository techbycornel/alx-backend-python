from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")
        if conversation_id:
            return Message.objects.filter(
                conversation_id=conversation_id,
                conversation__participants=self.request.user
            )
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = Conversation.objects.filter(id=conversation_id).first()

        if not conversation or self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not allowed to send messages in this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer.save(sender=self.request.user, conversation=conversation)
