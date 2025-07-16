from utils import input_error
from models import AddressBook, Record, Birthday, Email, Address, NoteBook

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("You must enter a name and phone number.")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message
    

@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("You need to enter three arguments: name, old number, new number.")
    
    name, old, new = args
    record = book.find(name)
    
    if not record:
        return "Contact not found."

    if old not in [phone.value for phone in record.phones]:
        raise ValueError("Old phone number not found in contact.")
    
    record.edit_phone(old, new)
    return "The phone number has been updated."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"Phone numbers for {name}: " + ', '.join(p.value for p in record.phones)
    return "Contact not found."


@input_error
def show_all(book):
    return "\n".join(str(record) for record in book.values()) or "Address book is empty."

@input_error
def add_birthday(args, book):
    name, date_str = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(date_str)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    if not record.birthday:
        return "Birthday not set."
    return f"{name}'s birthday: {record.birthday.value}"


@input_error
def birthdays(book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays this week."
    result = "Upcoming birthdays:\n"
    for user in upcoming:
        result += f"{user['name']} - {user['congratulation_date']}\n"
    return result.strip()

@input_error
def add_email(args, book):
    name, email = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_email(email)
    return "Email added."

@input_error
def add_address(args, book):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_address(address)
    return "Address added."

@input_error
def delete_contact(args, book):
    name = args[0]
    if book.delete(name):
        return f"Contact {name} deleted."
    return "Contact not found."

@input_error
def find_contact(args, book):
    keyword = args[0]
    matches = book.search(keyword)
    if not matches:
        return "No matching contacts found."
    return "\n".join(str(record) for record in matches)

@input_error
def add_note(args, notebook):
    pass

@input_error
def find_note(args, notebook):
    pass

@input_error
def delete_note(args, notebook):
    pass

@input_error
def edit_note(args, notebook):
    pass
