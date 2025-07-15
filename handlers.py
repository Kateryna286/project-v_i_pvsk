from utils import input_error
from models import AddressBook, Record, Birthday, Email, Address, NoteBook

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError
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
    pass


@input_error
def show_phone(args, book):
    pass

@input_error
def show_all(book):
    pass

@input_error
def add_birthday(args, book):
    pass

@input_error
def show_birthday(args, book):
    pass

@input_error
def birthdays(book):
    pass

@input_error
def add_email(args, book):
    pass

@input_error
def add_address(args, book):
    pass

@input_error
def delete_contact(args, book):
    pass

@input_error
def find_contact(args, book):
    pass

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
