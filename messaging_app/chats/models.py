"""
Data models for chats application.

User:
    A user of the system.

Conversation:
    A conversation between users.

Message:
    A user's message.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid


class User(AbstractUser):
    """A user of the system."""
    class Meta:
        db_table = 'users'

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identification of user'
    )

    email = models.EmailField(help_text='Email address of the user')
    password = models.CharField(max_length=128, help_text='Password of user')
    first_name = models.CharField(max_length=100, help_text='First name of user')
    last_name = models.CharField(max_length=100, help_text='Last name of user')
    phone_number = models.CharField(max_length=20, help_text='Phone number of user')


class Conversation(models.Model):
    """A conversation between users."""
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identification of conversation'
    )

    participants = models.ManyToManyField(User, related_name='conversations')


class Message(models.Model):
    """A user's message."""
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identification of message'
    )

    message_body = models.TextField(help_text='Body of message')
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(auto_now=True)
