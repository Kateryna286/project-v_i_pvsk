from utils import input_error, normalize_phone, autosave
from models import AddressBook, Record, Birthday, Email, Address, NoteBook, Note
from formatters import format_contacts, format_notes, format_notes_list


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
@autosave
def add_contact_interactive(book: AddressBook):
    """Interactively collects contact info and adds it to the address book."""
    name = input("Enter contact name: ").strip()
    if not name:
        raise ValueError("Name is required.")

    if book.get_record(name):
        raise ValueError(
            f"A contact with the name '{name.capitalize()}' already exists. "
            f"To modify it, use the 'change' command."
        )

    record = Record(name)

    # Add phones
    while True:
        phone = input("Enter a phone number (or press Enter to skip): ").strip()
        if not phone:
            break
        try:
            record.add_phone(phone)
            print(f"Phone {phone} added.")
            break
        except ValueError as e:
            print(f"{e}")

    # Add email
    while True:
        email = input("Enter email (press Enter to skip): ").strip()
        if not email:
            break
        try:
            record.set_email(email)
            print(f"Email {email} added.")
            break
        except ValueError as e:
            print(f"{e} (expected format: name@example.com)")

    # Add address
    address = input("Enter address (press Enter to skip): ").strip()
    if address:
        try:
            record.set_address(address)
            print(f"Address '{address}' added.")
        except ValueError as e:
            print(f"{e} (please enter a non-empty address)")

    # Add birthday
    while True:
        birthday = input("Enter birthday (DD.MM.YYYY, press Enter to skip): ").strip()
        if not birthday:
            break
        try:
            record.set_birthday(birthday)
            print(f"Birthday {birthday} added.")
            break
        except ValueError as e:
            print(f"{e}")

    # Add record to book
    book.add_record(record)
    return f"\nContact created:\n{record}"


@input_error
@autosave
def change_contact_interactive(book: AddressBook):
    name = input("Enter the name of the contact to change: ").strip()
    record = book.get_record(name)
    if not record:
        return f"Contact '{name}' not found."

    print(f"\nWhat would you like to change for {record.name.value}?")
    options = ["name", "phone", "email", "birthday", "address"]
    print("Options:", ", ".join(options))

    while True:
        field = input("Field to change (or type 'esc' to cancel): ").strip().lower()

        if field == "esc":
            return "Change cancelled."

        if field not in options:
            print(
                "Invalid field. Please choose from: name, phone, email, birthday, address."
            )
            continue
        break

    if field == "phone":
        if not record.phones:
            return "No phone numbers found for this contact. Use the 'add-phone' command to add one"

        if len(record.phones) == 1:
            old_phone = record.phones[0].value
            print(f"Current phone: {old_phone}")
            while True:
                new_phone = input(
                    "Enter a new phone number (or 'esc' to cancel): "
                ).strip()

                if new_phone.lower() == "esc":
                    return "Phone number change cancelled."

                try:
                    record.edit_phone(old_phone, new_phone)
                    return "Phone updated."
                except ValueError as e:
                    print(f"{e} Please try again.")

        else:
            print("Phone numbers:")
            for idx, p in enumerate(record.phones, 1):
                print(f"{idx}. {p.value}")

            while True:
                index_input = input(
                    "Enter the number of the phone to change (or 'esc' to cancel): "
                ).strip()

                if index_input.lower() == "esc":
                    return "Phone number change cancelled."

                if not index_input.isdigit():
                    print("Please enter a valid number.")
                    continue

                index = int(index_input)
                if index < 1 or index > len(record.phones):
                    print(f"Please choose a number between 1 and {len(record.phones)}.")
                    continue

                old_phone = record.phones[index - 1].value
                while True:
                    new_phone = input(
                        "Enter new phone number (or 'esc' to cancel): "
                    ).strip()
                    if new_phone.lower() == "esc":
                        return "Phone number change cancelled."

                    try:
                        record.edit_phone(old_phone, new_phone)
                        return "Phone updated."
                    except ValueError as e:
                        print(f"{e}")

    elif field == "email":
        if not record.email:
            return "No email found for this contact. Use the 'add-email' command to add one"

        old = record.email.value
        print(f"Current email: {old}")
        while True:
            new_email = input("Enter new email (or 'esc' to cancel): ").strip()

            if new_email.lower() == "esc":
                return "Email change cancelled."

            try:
                record.set_email(new_email)
                return "Email updated."
            except ValueError as e:
                print(f"{e} (expected format: name@example.com)")

    elif field == "birthday":
        if not record.birthday:
            return "No birthday found for this contact. Use the 'add-birthday' command to add one"

        old = record.birthday.value.strftime("%d.%m.%Y")
        print(f"Current birthday: {old}")
        while True:
            new_birthday = input("Enter new birthday (or 'esc' to cancel): ").strip()

            if new_birthday.lower() == "esc":
                return "Birthday change cancelled."

            try:
                record.set_birthday(new_birthday)
                return "Birthday updated."
            except ValueError as e:
                print(f"{e}")

    elif field == "address":
        if not record.address:
            return "No address found for this contact. Use the 'add-address' command to add one"
        old = record.address.value
        print(f"Current address: {old}")
        new_address = input("Enter new address (or 'esc' to cancel): ").strip()
        if new_address.lower() == "esc":
            return "Address change cancelled."
        record.set_address(new_address)
        return "Address updated."

    elif field == "name":
        old = record.name.value
        print(f"Current name: {old}")
        new_name = input("Enter new name (or 'esc' to cancel): ").strip()
        if new_name.lower() == "esc":
            return "Name change cancelled."

        if book.get_record(new_name):
            return f"A contact with the name '{new_name}' already exists."

        book.remove_record(old)
        record.set_name(new_name)
        book.add_record(record)
        return "Name updated."

    else:
        return (
            "Invalid field. Please choose from name, phone, email, birthday, address."
        )


@input_error
def show_phone_interactive(book):
    name = input("Enter the name of the contact: ").strip()
    record = book.get_record(name)
    if not record:
        return "Contact was not found."

    if not record.phones:
        return f"No phone numbers found for {name.capitalize()}."

    phones = ", ".join(p.value for p in record.phones)
    return f"Phone numbers for {name.capitalize()}: {phones}"


@input_error
@autosave
def add_birthday_interactive(book):
    name = input("Enter the name of the contact: ").strip()
    record = book.get_record(name)
    if not record:
        return "Contact was not found."

    if record.birthday:
        return "This contact already has a bitrthday. To change it, use the 'change' command."

    while True:
        date_str = input("Enter birthday (DD.MM.YYYY): ").strip()
        if not date_str:
            return "Birthday is required."
        try:
            record.set_birthday(date_str)
            return f"Birthday {date_str} added for {name.capitalize()}."
        except ValueError as e:
            print(f"{e}")


@input_error
def show_birthday_interactive(book):
    name = input("Enter the name of the contact: ").strip()
    record = book.get_record(name)
    if not record:
        return "Contact was not found."

    if not record.birthday:
        return f"Birthday for {name} is not set."

    birthday_str = record.birthday.value.strftime("%d.%m.%Y")
    return f"{name.capitalize()}'s birthday: {birthday_str}"


@input_error
def birthdays_interactive(book):
    try:
        days_str = input(
            "Enter number of days to look ahead for birthdays (default is 7): "
        ).strip()
        days = int(days_str) if days_str else 7
        if days < 0:
            raise ValueError("Number of days must be zero or positive.")
    except ValueError:
        return "Please enter a valid non-negative integer for days."

    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"There are no upcoming birthdays in the next {days} day(s)."

    result = f"Upcoming birthdays within {days} day(s):\n"
    for user in upcoming:
        result += f"• {user['name']} - 🎂 {user['congratulation_date']}\n"
    return result.strip()


@input_error
@autosave
def add_phone_interactive(book):
    name = input("Enter the contact name: ").strip()
    record = book.get_record(name)
    if not record:
        return "Contact was not found."

    while True:
        phone = input("Enter the new phone number (or press Enter to cancel): ").strip()
        if not phone:
            return "Phone number not provided."
        try:
            record.add_phone(phone)
            return f"Phone number {phone} added to {name}."
        except ValueError as e:
            print(f"{e}")


@input_error
@autosave
def add_email_interactive(book):
    name = input("Enter the name of the contact: ").strip()
    record = book.get_record(name)
    if not record:
        return "Contact was not found."

    if record.email:
        return (
            "This contact already has an email. To change it, use the 'change' command."
        )

    while True:
        email = input("Enter email address: ").strip()
        if not email:
            return "Email is required."
        try:
            record.set_email(email)
            return f"Email {email} added to {name}."
        except ValueError as e:
            print(f"{e}")


@input_error
@autosave
def add_address_interactive(book):
    name = input("Enter the name of the contact: ").strip()
    record = book.get_record(name)
    if not record:
        return "Contact was not found."

    if record.address:
        return "This contact already has an address. To change it, use the 'change' command."

    while True:
        address = input("Enter address: ").strip()
        if not address:
            print("Address cannot be empty.")
            continue
        try:
            record.set_address(address)
            return f"Address added to {name}."
        except ValueError as e:
            print(f"{e}")


@input_error
@autosave
def delete_contact_interactive(book):
    name = input("Enter the name of the contact to delete: ").strip()
    record = book.get_record(name)
    if not record:
        return "Contact was not found."

    print("\nHere is the contact info:")
    print(record.get_info())

    while True:
        confirm = (
            input(f"Are you sure you want to delete '{name.capitalize()}'? (y/n): ")
            .strip()
            .lower()
        )
        if confirm in ("y", "yes"):
            book.remove_record(record.name.value)
            return f"Contact '{record.name.value}' was deleted."
        elif confirm in ("n", "no"):
            return "Deletion cancelled."
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


@input_error
def find_contact_interactive(book):
    """
    Interactive contact search in the address book.
    The user enters a keyword, and the program displays matching contacts.
    """
    query = (
        input("Enter a keyword to search (name, phone, email, or address): ")
        .strip()
        .lower()
    )
    if not query:
        return "Search query cannot be empty."

    matches = []
    for record in book.values():
        if query in record.name.value.lower():
            matches.append(record)
        elif any(query in phone.value.lower() for phone in record.phones):
            matches.append(record)
        elif record.email and query in record.email.value.lower():
            matches.append(record)
        elif record.address and query in record.address.value.lower():
            matches.append(record)

    if not matches:
        return "No contacts matched your search."

    return format_contacts({r.name.value: r for r in matches})


@input_error
@autosave
def add_note_interactive(notebook):
    text = input("Enter the note text: ").strip()
    if not text:
        return "Note text cannot be empty."

    tags_input = input("Enter tags (comma-separated, or press Enter to skip): ").strip()
    tags = (
        [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        if tags_input
        else []
    )

    note_id = notebook._generate_id()
    note = Note(text, tags)
    notebook.add_note(note_id, note)
    return f"Note '{note_id}' added successfully."


@input_error
def find_note_interactive(notebook):
    query = input("Enter a search keyword (text or tag): ").strip()
    results = notebook.search_notes(query)
    if not results:
        return "No notes matched your search."

    return format_notes_list(list(results.items()))


@input_error
def sort_notes_by_tag_interactive(notebook):
    tag = input("Enter a tag to sort notes by: ").strip()
    sorted_notes = notebook.sort_notes_by_tag(tag)
    if not sorted_notes:
        return "No notes to show."

    return format_notes_list(sorted_notes)


@input_error
@autosave
def edit_note_interactive(notebook):
    key = input("Enter the note id of the note to edit: ").strip()
    if key not in notebook.data:
        return f"Note '{key}' not found."

    new_text = input(
        "Enter new text (Press 'Enter' for skip and keep current): "
    ).strip()
    tags_input = input(
        "Enter new tags (comma-separated, Press 'Enter' for skip and keep current): "
    ).strip()
    new_tags = [t.strip() for t in tags_input.split(",")] if tags_input else None

    notebook.edit_note(key, new_text or None, new_tags)
    return f"Note '{key}' updated successfully."


@input_error
@autosave
def delete_note_interactive(notebook):
    key = input("Enter the ID of the note to delete: ").strip()
    notebook.delete_note(key)
    return f"Note '{key}' deleted successfully."
