from utils import input_error, normalize_phone
from models import AddressBook, Record, Birthday, Email, Address, NoteBook, Note
from formatters import format_contacts, format_notes

@input_error
def show_all(book):
    if not book.values():
        return "Your address book is currently empty."
    return format_contacts(book)

@input_error
def show_notes(notebook):
    if not notebook.data:
        return "There are no notes available."
    return format_notes(notebook)

@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Please provide both a name and a phone number.")
    name, phone, *_ = args
    record = book.get_record(name)
    message = "Contact updated successfully."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added successfully."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError("Please enter exactly three arguments: name, old number, and new number.")
    
    name, old, new = args
    record = book.get_record(name)
    if not record:
        return "Contact was not found."

    normalized_old = normalize_phone(old)
    if normalized_old not in [normalize_phone(p.value) for p in record.phones]:
        raise ValueError("The old phone number was not found in the contact.")
    
    record.edit_phone(old, new)
    return "Phone number updated successfully."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.get_record(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        return f"Phone numbers for {name}: {phones}"
    return "Contact was not found."

@input_error
def add_birthday(args, book):
    name, date_str = args
    record = book.get_record(name)
    if not record:
        return "Contact was not found."
    record.set_birthday(date_str)
    return "Birthday added successfully."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.get_record(name)
    if not record:
        return "Contact was not found."
    if not record.birthday:
        return "Birthday is not set."
    birthday_str = record.birthday.value.strftime("%d.%m.%Y")
    return f"{name}'s birthday: {birthday_str}"

@input_error
def birthdays(book, days=7):
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"There are no upcoming birthdays in the next {days} day(s)."
    result = f"Upcoming birthdays within {days} day(s):\n"
    for user in upcoming:
        result += f"{user['name']} - {user['congratulation_date']}\n"
    return result.strip()

@input_error
def add_email(args, book):
    name, email = args
    record = book.get_record(name)
    if not record:
        return "Contact was not found."
    record.add_email(email)
    return "Email added successfully."

@input_error
def add_address(args, book):
    name = args[0]
    address = " ".join(args[1:])
    record = book.get_record(name)
    if not record:
        return "Contact was not found."
    record.add_address(address)
    return "Address added successfully."

@input_error
def delete_contact(args, book):
    name = args[0]
    try:
        book.remove_record(name)
        return f"Contact '{name}' was deleted."
    except KeyError:
        return "Contact was not found."

@input_error
def find_contact(args, book):
    keyword = args[0].lower()
    matches = [record for record in book.values()
               if keyword in record.name.lower() or
               any(keyword in p.value.lower() for p in record.phones)]
    if not matches:
        return "No contacts matched your search."
    return format_contacts({r.name: r for r in matches})

@input_error
def add_note(args, notebook):
    if len(args) < 2:
        raise ValueError("Please provide a title and the note text.")
    title = args[0]
    text = " ".join(args[1:])
    note = Note(text)
    notebook.add_note(title, note)
    return f"Note '{title}' added successfully."

@input_error
def find_note(args, notebook):
    if not args:
        raise ValueError("Please provide a search keyword.")
    query = " ".join(args).lower()
    results = {title: note for title, note in notebook.data.items()
               if query in title.lower() or query in str(note).lower()}
    if not results:
        return "No notes matched your search."
    output = ["Matching notes:"]
    for title, note in results.items():
        output.append(f"• {title}: {note}")
    return "\n".join(output)

@input_error
def delete_note(args, notebook):
    if not args:
        raise ValueError("Please provide the title of the note to delete.")
    title = " ".join(args)
    notebook.delete_note(title)
    return f"Note '{title}' deleted successfully."

@input_error
def edit_note(args, notebook):
    if len(args) < 2:
        raise ValueError("Please provide the title and the new text.")
    title = args[0]
    new_text = " ".join(args[1:])
    notebook.edit_note(title, new_text)
    return f"Note '{title}' updated successfully."

def show_help():
    return (
        "\nAvailable commands:\n"
        "add - Add a new contact\n"
        "change - Change contact's phone number\n"
        "phone - Show phone numbers for contact\n"
        "all - Show all contacts\n"
        "add-birthday - Add birthday to contact\n"
        "show-birthday - Show contact's birthday\n"
        "birthdays - Show upcoming birthdays\n"
        "delete - Delete contact\n"
        "find - Search contacts\n"
        "add-note - Add a note\n"
        "find-note - Find a note\n"
        "edit-note - Edit a note\n"
        "delete-note - Delete a note\n"
        "show-notes - Show all notes\n"
        "hello - Greeting\n"
        "help - Show this help message\n"
        "exit / close - Exit the assistant\n"
    )
