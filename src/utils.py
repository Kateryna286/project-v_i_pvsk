from validators import normalize_phone


def parse_input(user_input):
    """Parses only the command from user's input, ignoring arguments."""
    return user_input.strip().lower(), []


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
