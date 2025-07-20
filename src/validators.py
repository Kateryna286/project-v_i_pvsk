import re


PHONE_REGEX = r"^\+\d{1,3}\d{6,9}$"
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


def normalize_phone(value: str) -> str:
    value = value.strip()
    if value.startswith("+"):
        return "+" + "".join(filter(str.isdigit, value[1:]))
    return "".join(filter(str.isdigit, value))


def is_valid_phone(value: str) -> bool:
    """Validates normalized phone number format"""
    normalized = normalize_phone(value)
    return re.fullmatch(PHONE_REGEX, normalized)


def is_valid_email(value):
    return re.fullmatch(EMAIL_REGEX, value)
