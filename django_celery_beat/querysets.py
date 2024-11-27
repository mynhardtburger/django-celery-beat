"""Model querysets."""
from typing import Self
from django.db import models


class PeriodicTaskQuerySet(models.QuerySet):
    """QuerySet for PeriodicTask."""

    def enabled(self) -> Self:
        return self.filter(enabled=True).prefetch_related(
            "interval", "crontab", "solar", "clocked"
        )
