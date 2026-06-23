import re
import html

MAX_NAME_LENGTH = 100
MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 128

def sanitize_string(value: str, max_length: int = MAX_NAME_LENGTH) -> str:
    if not isinstance(value, str):
        raise ValueError("Must be text")

    value = value.strip()

    if len(value) == 0:
        raise ValueError("This field can't be empty")
    if len(value) > max_length:
        raise ValueError(f"Max length {max_length} charachters")

    value = html.escape(value)

    sql_patterns = r"(--|;|/\*|\*/|xp_|union|select|insert|drop|delete|update|exec|execute)"
    if re.search(sql_patterns, value, re.IGNORECASE):
        raise ValueError("Invalid context")

    return value

def sanitize_username(value: str) -> str:
    value = sanitize_string(value, max_length=MAX_USERNAME_LENGTH)

    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise ValueError("Username must contain only numbers, letters, _ and -")

    return value

def sanitize_password(value: str) -> str:

    value = value.strip()

    if len(value) < 8:
        raise ValueError("Password must be at least 8 charachters")
    if len(value) > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Max length {MAX_PASSWORD_LENGTH} charachters")

    return value
