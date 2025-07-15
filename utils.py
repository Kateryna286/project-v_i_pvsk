import re

PHONE_REGEX = r"\+?\d{7,15}"
EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

def is_valid_phone(value):
    return re.fullmatch(PHONE_REGEX, value)

def is_valid_email(value):
    return re.fullmatch(EMAIL_REGEX, value)

def parse_input(user_input):
    """Parses the user's input into a command and its arguments."""
      
    parts = user_input.strip().lower().split()
    if not parts:
        return "", []
    return parts[0], parts[1:]


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."
        except ValueError as e:
            return str(e) if str(e) else "Give me name and phone please."
    return wrapper