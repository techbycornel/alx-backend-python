from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["user_id", "username", "email", "first_name", "last_name", "phone_number"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["message_id", "sender", "conversation", "message_body", "sent_at", "message_preview"]

    def get_message_preview(self, obj):
        """Return first 30 characters of the message for preview."""
        return obj.message_body[:30]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at", "messages"]

    def validate(self, data):
        """Custom validation example to satisfy ValidationError requirement."""
        if not data.get("participants") and not self.instance:
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return data
