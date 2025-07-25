from django.http import HttpRequest

import datetime


def get_ip_address(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()    # It may contain multiple IPs if there are proxies
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def within_same_minute(t1: datetime.datetime, t2: datetime.datetime) -> bool:
    if t1 <= t2:
        timedelta = t2 - t1
    else:
        timedelta = t1 - t2

    return timedelta.seconds < 60
