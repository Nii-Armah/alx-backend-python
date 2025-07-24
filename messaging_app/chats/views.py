"""
API endpoints for chats application.

ConversationViewSet:
    Handles management of conversations.

MessageViewSet:
    Handles management of messages.
"""

from django.db.models import QuerySet

from .filters import MessageFilter
from .models import Conversation, Message
from .pagination import PageNumberPagination
from .permissions import  IsParticipantOfConversation
from .serializers import ConversationSerializer, MessageSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions


class ConversationViewSet(viewsets.ModelViewSet):
    """Handles management of conversations."""
    queryset = Conversation.objects.select_related('participants', 'messages').all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation, ]

    def get_object(self):
        conversation = super().get_object()

        if self.request.user not in conversation.participants.all():
            raise status.HTTP_403_FORBIDDEN

        return conversation

    def get_queryset(self):
        user_conversations = self.request.user.conversations.all()
        return Conversation.objects.select_related('participants', 'messages').filter(conversation_id_in=user_conversations).all()


class MessageViewSet(viewsets.ModelViewSet):
    """Handles management of messages."""
    serializer_class = MessageSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self) -> QuerySet:
        return Message.objects.filter(conversation__participants=self.request.user.pk).select_related('conversation')
