"""
Middlewares specific to chats application.

RequestLoggingMiddleware:
    Logs each request including the timestamp, user and request path.

RestrictAccessByTimeMiddleware:
    Restricts access to the application between 6pm and 9pm (inclusive) each day.

OffensiveLanguageMiddleware:
    Restricts IPs to a maximum of 5 POST requests per minute.

RolePermissionMiddleware:
    Restricts access to the endpoint to administrative users.
"""

from django.http import HttpResponse
from django.utils import timezone

from .utils import get_ip_address, within_same_minute

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


TIMESTAMPS_PER_IP = {}


class OffensiveLanguageMiddleware:
    """Restricts IPs to a maximum of 5 POST requests per minute."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = get_ip_address(request)

        if request.method == 'POST':
            # First request from IP address
            timestamps = TIMESTAMPS_PER_IP.get(ip_address, [])
            if len(timestamps) == 0:
                TIMESTAMPS_PER_IP[ip_address] = [timezone.now()]
                return self.get_response(request)

            # Subsequent request from IP address
            now = timezone.now()
            timestamps = list(filter(lambda timestamp: within_same_minute(now, timestamp), timestamps))
            if len(timestamps) >= 5:
                return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

            TIMESTAMPS_PER_IP[ip_address].append(now)

        return self.get_response(request)


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_staff:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        return self.get_response(request)
