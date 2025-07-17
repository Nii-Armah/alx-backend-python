"""
URL configuration for chats application.
"""

from chats.views import MessageViewSet, ConversationViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')