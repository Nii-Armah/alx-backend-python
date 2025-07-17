"""
URL configuration for chats application.
"""

from django.urls import include, path

from messaging_app.chats.views import MessageViewSet, ConversationViewSet

from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversations', ConversationViewSet)


nested_router = NestedDefaultRouter(router, r'api')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
