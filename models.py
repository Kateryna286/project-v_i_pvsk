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
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())

class Phone(Field):
    def __init__(self, value):
        clean_value = ''.join(filter(str.isdigit, value))
        if len(clean_value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(clean_value)

    @staticmethod
    def validate(value):
        return len(value) == 10 and value.isdigit()

class Email(Field):
    def __init__(self, value):
        email = value.strip()
        if (
            not email
            or email.count("@") != 1
            or email.startswith("@")
            or email.endswith("@")
            or '.' not in email.split("@")[1]
            or " " in email
        ):
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
class Record:
    def __init__(self, name, phone=None, email=None, birthday=None, address=None):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = Birthday(birthday) if birthday else None
        self.address = Address(address) if address else None

        if phone:
            self.add_phone(phone)
        if email:
            self.add_email(email)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_email(self, email):
        self.emails.append(Email(email))

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def set_address(self, address):
        self.address = Address(address)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def remove_email(self, email):
        for e in self.emails:
            if e.value == email:
                self.emails.remove(e)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        if not Phone.validate(new_phone):
            raise ValueError("New phone number must be 10 digits.")
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def get_info(self):
        info = f"Name: {self.name.value}\n"
        if self.phones:
            info += "Phones: " + ", ".join(str(p) for p in self.phones) + "\n"
        if self.emails:
            info += "Emails: " + ", ".join(str(e) for e in self.emails) + "\n"
        if self.address:
            info += f"Address: {self.address.value}\n"
        if self.birthday:
            info += f"Birthday: {self.birthday.value.strftime('%d.%m.%Y')}\n"
        return info.strip()

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "no phones"
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

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                self.data = pickle.load(f)
        else:
            self.data = {}

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

    def add_note(self, note_text):
        note = Note(note_text)
        self.data[len(self.data) + 1] = note
        self.save()

    def search(self, keyword):
        return {k: v for k, v in self.data.items() if keyword.lower() in v.text.lower()}

    def delete_note(self, note_id):
        if note_id in self.data:
            del self.data[note_id]
            self.save()
        else:
            raise KeyError(f"No note with ID {note_id}")

    def edit_note(self, note_id, new_text):
        if note_id not in self.data:
            raise KeyError(f"No note with ID {note_id}")
        self.data[note_id] = Note(new_text)
        self.save()

    def save(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self.data, f)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, "rb") as f:
                self.data = pickle.load(f)
        else:
            self.data = {}