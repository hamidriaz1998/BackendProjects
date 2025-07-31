import secrets
from datetime import datetime, timedelta, timezone


def generate_random_string(length: int = 8) -> str:
    return secrets.token_urlsafe(length)


def get_time():
    return datetime.now(timezone.utc)


def get_expiration_time(after_minutes: float) -> datetime:
    return get_time() + timedelta(minutes=after_minutes)
