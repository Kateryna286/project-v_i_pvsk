import pickle
import os
from collections import UserDict
from datetime import datetime, date, timedelta

# ----------- Field Base Class -------------
class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

# ----------- Contact Fields ---------------
class Name(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())

class Phone(Field):
    def __init__(self, value):
        clean_value = ''.join(filter(str.isdigit, value))
        if not is_valid_phone(clean_value):
            raise ValueError("Phone number must be valid (10 digits).")
        super().__init__(clean_value)

class Email(Field):
    def __init__(self, value):
        email = value.strip()
        if not is_valid_email(email):
            raise ValueError("Invalid email format.")
        super().__init__(email)

class Birthday(Field):
    def __init__(self, value):
        if isinstance(value, str):
            try:
                birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError("Birthday must be in format DD.MM.YYYY")
        elif isinstance(value, date):
            birthday_date = value
        else:
            raise TypeError("Birthday must be a string or datetime.date")
        if birthday_date > date.today():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(birthday_date)

class Address(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Address cannot be empty.")
        super().__init__(value.strip())

# ----------- Contact Record ----------------
from datetime import datetime, date

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def set_email(self, email):
        self.email = Email(email)

    def remove_email(self):
        self.email = None

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def set_address(self, address):
        self.address = Address(address)

    def get_info(self):
        info = f"Name: {self.name.value}\n"
        if self.phones:
            info += "Phones: " + ", ".join(str(p) for p in self.phones) + "\n"
        if self.email:
            info += f"Email: {self.email.value}\n"
        if self.address:
            info += f"Address: {self.address.value}\n"
        if self.birthday:
            info += f"Birthday: {self.birthday.value.strftime('%d.%m.%Y')}\n"
        return info.strip()

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = date.today()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "No phones"
        return f"{self.name.value} | Phones: {phones}"


# ----------- AddressBook -------------------
class AddressBook(UserDict):
    def __init__(self, filename="address_book.pkl"):
        super().__init__()
        self.filename = filename
        self.load()

    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Only Record instances can be added.")
        self.data[record.name.value] = record
        self.save()

    def get_record(self, name):
        return self.data.get(name)

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]
            self.save()
        else:
            raise KeyError(f"No record found for name: {name}")

    def search(self, query):
        result = []
        for record in self.data.values():
            if (
                query.lower() in record.name.value.lower()
                or any(query in p.value for p in record.phones)
                or any(query in e.value for e in record.emails)
                or (record.address and query.lower() in record.address.value.lower())
            ):
                result.append(record)
        return result

    def get_upcoming_birthdays(self, days=7):
        today = date.today()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                if 0 <= (bday - today).days <= days:
                    upcoming.append({
                        "name": record.name.value,
                        "birthday": bday.strftime("%d.%m.%Y")
                    })
        return upcoming

# ----------- Note & NotesBook ---------------
class Note:
    def __init__(self, text):
        if not text.strip():
            raise ValueError("Note cannot be empty.")
        self.text = text.strip()

    def __str__(self):
        return self.text

class NotesBook(UserDict):
    def __init__(self, filename="notes_book.pkl"):
        super().__init__()
        self.filename = filename
        self.load()