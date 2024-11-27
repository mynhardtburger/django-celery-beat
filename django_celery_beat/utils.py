"""Utilities."""
from __future__ import annotations
# -- XXX This module must not use translation as that causes
# -- a recursive loader import!
from datetime import timezone as datetime_timezone

from django.conf import settings
from django.utils import timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime, time


is_aware = timezone.is_aware
# celery schedstate return None will make it not work
NEVER_CHECK_TIMEOUT = 100000000

# see Issue #222
now_localtime = getattr(timezone, 'template_localtime', timezone.localtime)


def make_aware(value: time | datetime) -> datetime | time:
    """Force datatime to have timezone information."""
    if getattr(settings, 'USE_TZ', False):
        # naive datetimes are assumed to be in UTC.
        if timezone.is_naive(value):
            value = timezone.make_aware(value, datetime_timezone.utc)
        # then convert to the Django configured timezone.
        default_tz = timezone.get_default_timezone()
        value = timezone.localtime(value, default_tz)
    elif timezone.is_naive(value):
        # naive datetimes are assumed to be in local timezone.
        value = timezone.make_aware(value, timezone.get_default_timezone())
    return value


def now() -> datetime:
    """Return the current date and time."""
    if getattr(settings, 'USE_TZ', False):
        return now_localtime(timezone.now())
    else:
        return timezone.now()


def is_database_scheduler(scheduler: str) -> bool:
    """Return true if Celery is configured to use the db scheduler."""
    if not scheduler:
        return False
    from kombu.utils import symbol_by_name

    from .schedulers import DatabaseScheduler
    return (
        scheduler == 'django'
        or issubclass(symbol_by_name(scheduler), DatabaseScheduler)
    )
