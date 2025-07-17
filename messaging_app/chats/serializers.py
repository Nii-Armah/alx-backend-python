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


class ConversationSerializer:
    """Processes and validates Conversation model data."""
    class Meta:
        model = Conversation
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    """Processes and validates Message model data."""
    class Meta:
        model = Message
        fields = '__all__'


class UserSerializer:
    """Processes and validates User model data."""
    class Meta:
        model = User
        fields = '__all__'
