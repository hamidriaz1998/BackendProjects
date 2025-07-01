import secrets


def generate_random_string(length: int = 8) -> str:
    return secrets.token_urlsafe(length)
