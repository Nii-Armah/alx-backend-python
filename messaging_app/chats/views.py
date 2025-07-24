"""
API endpoints for chats application.

ConversationViewSet:
    Handles management of conversations.

MessageViewSet:
    Handles management of messages.
"""

from .models import Conversation, Message
from .permissions import  IsParticipantOfConversation
from .serializers import ConversationSerializer, MessageSerializer

from rest_framework import viewsets, status, filters, permissions


class ConversationViewSet(viewsets.ModelViewSet):
    """Handles management of conversations."""
    queryset = Conversation.objects.select_related('participants', 'messages').all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation, ]


class MessageViewSet(viewsets.ModelViewSet):
    """Handles management of messages."""
    queryset = Message.objects.select_related('conversation').all()
    serializer_class = MessageSerializer