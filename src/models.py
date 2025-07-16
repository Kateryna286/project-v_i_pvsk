from collections import UserDict
from datetime import datetime, date, timedelta
from utils import is_valid_phone, is_valid_email

# ----------- Field Base Class -------------

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

# ----------- Contact Fields ---------------

class Name(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value.strip())

class Phone(Field):
    def __init__(self, value):
        if not is_valid_phone(value):
            raise ValueError("Invalid phone number format.")
        super().__init__(value)

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

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                raise ValueError(f"Phone {phone} already exists for this contact.")

        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        if old_phone == new_phone:
            raise ValueError("New phone number must be different from the old one")

        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True

        raise ValueError(f"Phone {old_phone} not found in record")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True

        raise ValueError(f"Phone {phone} not found in record")

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
        phones = ", ".join(str(p) for p in self.phones)
        parts = [
            f"Name: {self.name}",
            f"Phones: {phones}" if phones else None,
            f"Email: {self.email}" if self.email else None,
            f"Birthday: {self.birthday}" if self.birthday else None,
            f"Address: {self.address}" if self.address else None
        ]
        return " | ".join(p for p in parts if p)


# ----------- AddressBook -------------------

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Only Record instances can be added.")
        self.data[record.name.value] = record

    def get_record(self, name):
        return self.data.get(name)

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"No record found for name: {name}")

    def search(self, query):
        result = []
        query_lower = query.lower()

        # замінив results на result
        for record in self.data.values():
            if query_lower in record.name.value.lower():
                result.append(record)
            elif any(query_lower in p.value.lower() for p in record.phones):
                result.append(record)
            elif record.email and query_lower in record.email.value.lower():
                result.append(record)
            elif record.address and query_lower in record.address.value.lower():
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
                        "congratulation_date": bday.strftime("%d.%m.%Y")
                    })
        return upcoming

# ----------- Note & NotesBook ---------------

class Note:
    def __init__(self, text):
        if not text.strip():
            raise ValueError("Note cannot be empty.")
        self.text = text.strip()

    def edit(self, new_text):
        if not new_text.strip():
            raise ValueError("Note text cannot be empty")
        self.text = new_text

    def __str__(self):
        return self.text

class NoteBook(UserDict):
    def add_note(self, key, note: Note):
        self.data[key] = note

    def delete_note(self, key):
        if key in self.data:
            del self.data[key]
        else:
            raise ValueError(f"Note '{key}' not found.")

    def edit_note(self, key, new_text):
        if key in self.data:
            self.data[key].edit(new_text)
            # print(f"Note '{key}' updated.")
        else:
            raise ValueError(f"Note '{key}' not found.")

    def search_notes(self, query):
        results = {}
        query_lower = query.lower()
        for key, note in self.data.items():
            if query_lower in note.text.lower():
                results[key] = note
        return results
