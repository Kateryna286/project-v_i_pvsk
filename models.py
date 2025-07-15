from collections import UserDict
from datetime import datetime, date  # додано date

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value) 

class Name(Field):
    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())

class Phone(Field):
    def __init__(self, value):
        clean_value = ''.join(filter(str.isdigit, value))
        if len(clean_value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(clean_value)

class Email(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Email cannot be empty.")
        email = value.strip()
        if email.count("@") != 1 or email.startswith("@") or email.endswith("@"):
            raise ValueError("Email must contain exactly one '@' and cannot start or end with '@'.")
        local, domain = email.split("@")
        if not local or not domain or '.' not in domain:
            raise ValueError("Email must contain a valid domain.")
        if " " in email or "\t" in email:
            raise ValueError("Email cannot contain spaces or tabs.")
        super().__init__(email)

class Birthday(Field):
    def __init__(self, value):
        if isinstance(value, str):
            try:
                birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("Birthday must be in the format DD.MM.YYYY")
        elif isinstance(value, date):
            birthday_date = value
        else:
            raise TypeError("Birthday must be a string in format DD.MM.YYYY or a datetime.date object.")
        if birthday_date > date.today():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(birthday_date)

class Address(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value.strip())

class Record:
    pass

class AddressBook(UserDict):
    pass

class Note:
    pass

class NoteBook(UserDict):
    pass
