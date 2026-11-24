"""
Time utilities for SafeTriage configured for Indian Standard Time (IST, UTC+05:30).
"""

from datetime import datetime, timezone, timedelta

# Indian Standard Time (UTC+05:30)
IST = timezone(timedelta(hours=5, minutes=30), name="IST")


def get_ist_now() -> datetime:
    """Return the current local datetime in Indian Standard Time (IST)."""
    return datetime.now(IST).replace(tzinfo=None)


def get_ist_now_aware() -> datetime:
    """Return timezone-aware current datetime in Indian Standard Time."""
    return datetime.now(IST)


def to_ist_iso(dt: datetime | None = None) -> str:
    """Return an ISO formatted timestamp in IST."""
    if dt is None:
        dt = datetime.now(IST)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=IST)
    else:
        dt = dt.astimezone(IST)
    return dt.isoformat()
