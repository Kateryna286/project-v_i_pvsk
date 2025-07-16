from utils import input_error
from models import AddressBook, Record, Birthday, Email, Address, NoteBook, Note

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("You must enter a name and phone number.")
    name, phone, *_ = args
    record = book.get_record(name)
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
    record = book.get_record(name)
    
    if not record:
        return "Contact not found."

    if old not in [phone.value for phone in record.phones]:
        raise ValueError("Old phone number not found in contact.")
    
    record.edit_phone(old, new)
    return "The phone number has been updated."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.get_record(name)
    if record:
        return f"Phone numbers for {name}: " + ', '.join(p.value for p in record.phones)
    return "Contact not found."


@input_error
def show_all(book):
    return "\n".join(str(record) for record in book.values()) or "Address book is empty."

@input_error
def add_birthday(args, book):
    name, date_str = args
    record = book.get_record(name)
    if not record:
        return "Contact not found."
    record.set_birthday(date_str)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.get_record(name)
    if not record:
        return "Contact not found."
    if not record.birthday:
        return "Birthday not set."

    birthday_str = record.birthday.value.strftime("%d.%m.%Y")  
    return f"{name}'s birthday: {birthday_str}"


@input_error
def birthdays(book, days=7):
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No upcoming birthdays in the next {days} day(s)."
    result = f"Upcoming birthdays in the next {days} day(s):\n"
    for user in upcoming:
        result += f"{user['name']} - {user['congratulation_date']}\n"
    return result.strip()

@input_error
def add_email(args, book):
    name, email = args
    record = book.get_record(name)
    if not record:
        return "Contact not found."
    record.add_email(email)
    return "Email added."

@input_error
def add_address(args, book):
    name = args[0]
    address = " ".join(args[1:])
    record = book.get_record(name)
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
    """Adds a new note to the notebook with a title and content."""
    if len(args) < 2:
        raise ValueError("You must provide a title and the note text.")

    title = args[0]
    text = " ".join(args[1:])
    note = Note(text)
    notebook.add_note(title, note)

    return f"Note '{title}' added."

@input_error
def find_note(args, notebook):
    """Searches notes by keyword in their text."""
    if not args:
        raise ValueError("Please provide a search keyword.")

    query = " ".join(args)
    results = notebook.search_notes(query)

    if not results:
        return "No matching notes found."

    output = ["Matching notes:"]
    for title, note in results.items():
        output.append(f"• {title}: {note}")
    return "\n".join(output)

@input_error
def delete_note(args, notebook):
    """Deletes a note by its title."""
    if not args:
        raise ValueError("Please provide the title of the note to delete.")
    
    title = " ".join(args)
    notebook.delete_note(title)

    return f"Note '{title}' deleted."

@input_error
def edit_note(args, notebook):
    """Edits an existing note by its title."""
    if len(args) < 2:
        raise ValueError("You must provide the title and the new text.")

    title = args[0]
    new_text = " ".join(args[1:])
    notebook.edit_note(title, new_text)

    return f"Note '{title}' updated."

@input_error
def show_notes(notebook):
    """Displays all saved notes in the notebook."""
    if not notebook.data:
        return "No notes found."

    output = ["All notes:"]
    for title, note in notebook.data.items():
        output.append(f"• {title}: {note}")
    return "\n".join(output)


@input_error
def delete_contact(args, book):
    name = args[0]
    try:
        book.remove_record(name)
        return f"Contact '{name}' deleted."
    except KeyError:
        return "Contact not found."




def show_help():
    return (
        "Available commands:\n"
        "  add — Add a new contact\n"
        "  change — Change contact's phone number\n"
        "  phone — Show phone numbers for contact\n"
        "  all — Show all contacts\n"
        "  add-birthday — Add birthday to contact\n"
        "  show-birthday — Show contact's birthday\n"
        "  birthdays — Show upcoming birthdays\n"
        "  delete — Delete contact\n"
        "  find  — Search contacts\n"
        "  add-note — Add a note\n"
        "  find-note — Find a note\n"
        "  edit-note — Edit a note\n"
        "  delete-note — Delete a note\n"
        "  hello — Greeting\n"
        "  help — Show this help message\n"
        "  exit / close — Exit the assistant"
    )

