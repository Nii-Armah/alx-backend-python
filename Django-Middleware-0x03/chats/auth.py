"""
Custom authentication logic for chats application.

CustomJWTAuthentication:
    Custom JWT authentication class leveraging default behaviour at the moment.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class leveraging default behaviour at the moment.

    Reserved for future extensions.
    """
    pass
