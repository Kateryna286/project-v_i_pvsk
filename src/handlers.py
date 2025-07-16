from utils import input_error, normalize_phone
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

    normalized_old = normalize_phone(old)
    if normalized_old not in [normalize_phone(p.value) for p in record.phones]:
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
    try:
        book.remove_record(name)
        return f"Contact '{name}' deleted."
    except KeyError:
        return "Contact not found."


@input_error
def find_contact(args, book):
    keyword = args[0].lower()
    matches = [record for record in book.values()
               if keyword in record.name.lower() or
               any(keyword in p.value.lower() for p in record.phones)]
    if not matches:
        return "No matching contacts found."
    return "\n".join(str(record) for record in matches)


@input_error
def add_note(args, notebook):
    if len(args) < 2:
        raise ValueError("You must provide a title and the note text.")
    title = args[0]
    text = " ".join(args[1:])
    note = Note(text)
    notebook.add_note(title, note)
    return f"Note '{title}' added."


@input_error
def find_note(args, notebook):
    if not args:
        raise ValueError("Please provide a search keyword.")
    query = " ".join(args).lower()
    results = {title: note for title, note in notebook.data.items()
               if query in title.lower() or query in str(note).lower()}
    if not results:
        return "No matching notes found."
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
    return f"Note '{title}' deleted."


@input_error
def edit_note(args, notebook):
    if len(args) < 2:
        raise ValueError("You must provide the title and the new text.")
    title = args[0]
    new_text = " ".join(args[1:])
    notebook.edit_note(title, new_text)
    return f"Note '{title}' updated."


@input_error
def show_notes(notebook):
    if not notebook.data:
        return "No notes found."
    output = ["All notes:"]
    for title, note in notebook.data.items():
        output.append(f"• {title}: {note}")
    return "\n".join(output)


def show_help():
    commands = [
        ("add", "Add a new contact"),
        ("change", "Change contact's phone number"),
        ("phone", "Show phone numbers for contact"),
        ("all", "Show all contacts"),
        ("add-birthday", "Add birthday to contact"),
        ("show-birthday", "Show contact's birthday"),
        ("birthdays", "Show upcoming birthdays"),
        ("delete", "Delete contact"),
        ("find", "Search contacts"),
        ("add-note", "Add a note"),
        ("find-note", "Find a note"),
        ("edit-note", "Edit a note"),
        ("delete-note", "Delete a note"),
        ("show-notes", "Show all notes"),
        ("hello", "Greeting"),
        ("help", "Show this help message"),
        ("exit / close", "Exit the assistant"),
    ]
    return "Available commands:\n" + "\n".join(f"  {cmd:<15} — {desc}" for cmd, desc in sorted(commands))
