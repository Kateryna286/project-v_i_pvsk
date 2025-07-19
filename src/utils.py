from validators import normalize_phone

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

def autosave(func):
    def wrapper(book_or_notebook, *args, **kwargs):
        from storage import save_data
        result = func(book_or_notebook, *args, **kwargs)
        save_data(book_or_notebook)
        return result
    return wrapper
