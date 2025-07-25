"""
Serializers for chats application.

ConversationSerializer:
    Processes and validates Conversation model data.

MessageSerializer:
    Processes and validates Message model data.

UserSerializer:
    Processes and validates User model data.
"""

from .models import Conversation, Message, User

from rest_framework import serializers


class ConversationSerializer(serializers.ModelSerializer):
    """Processes and validates Conversation model data."""
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = '__all__'

    def get_messages(self, conversation):
        return MessageSerializer(conversation.messages, many=True).data



class MessageSerializer(serializers.ModelSerializer):
    """Processes and validates Message model data."""
    class Meta:
        model = Message
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Processes and validates User model data."""
    password = serializers.CharField(max_length=128, write_only=True, help_text='Password of user')

    class Meta:
        model = User
        fields = '__all__'

    def validate_email(self, email):
        """Validate uniqueness of user email address."""
        if self.Meta.model.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'User exists with email address: {email}.')

        return email
