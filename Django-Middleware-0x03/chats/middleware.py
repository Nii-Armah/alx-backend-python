"""
Middlewares specific to chats application.

RequestLoggingMiddleware:
    Logs each request including the timestamp, user and request path.
"""

import datetime


class RequestLoggingMiddleware:
    """Logs each request including the timestamp, user and request path."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with open('requests.log', 'a') as log_file:
            log_file.write(f'{datetime.datetime.now()} - User: {request.user} - Path: {request.path}\n')

        return self.get_response(request)
