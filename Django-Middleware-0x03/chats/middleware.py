"""
Middlewares specific to chats application.

RequestLoggingMiddleware:
    Logs each request including the timestamp, user and request path.

RestrictAccessByTimeMiddleware:
    Restricts access to the application between 6pm and 9pm (inclusive) each day.
"""

from django.http import HttpResponse
from django.utils import timezone

from rest_framework import status

import datetime


class RequestLoggingMiddleware:
    """Logs each request including the timestamp, user and request path."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with open('requests.log', 'a') as log_file:
            log_file.write(f'{datetime.datetime.now()} - User: {request.user} - Path: {request.path}\n')

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """Restricts access to the application between 6pm and 9pm (inclusive) each day."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 18 <= timezone.now().hour <= 21:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        return self.get_response(request)
