"""
Custom permissions for chats application.

IsParticipantOfConversation:
    User is a participant of Conversation.
"""

from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """User is a participant of Conversation."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(user_id=request.user.id).exists()
