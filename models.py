from collections import UserDict
from datetime import datetime

class Field:
    def __init__ (self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value) 

class Name(Field):
    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())

class Phone(Field):
    pass

class Email(Field):
    pass

class Birthday(Field):
    pass

class Address(Field):
    pass

class Record:
    pass

class AddressBook(UserDict):
    pass

class Note:
    pass

class NoteBook(UserDict):
    pass
