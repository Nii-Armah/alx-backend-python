"""
Data models for chats application.

User:
    A user of the system.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid


class User(AbstractUser):
    """A user of the system."""
    class Meta:
        db_table = 'users'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique identification of user'
    )
