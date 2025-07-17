"""
URL configuration for chats application.
"""

from django.urls import include, path

from messaging_app.chats.views import MessageViewSet, ConversationViewSet

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
