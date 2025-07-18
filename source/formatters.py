from tabulate import tabulate
from colorama import Fore, Style, init

init(autoreset=True)


def format_contacts(book):
    """Форматує контакти у кольорову таблицю"""
    headers = [
        Fore.CYAN + "Name" + Style.RESET_ALL,
        Fore.CYAN + "Phones" + Style.RESET_ALL,
        Fore.CYAN + "Emails" + Style.RESET_ALL,
        Fore.CYAN + "Addresses" + Style.RESET_ALL,
        Fore.CYAN + "Birthday" + Style.RESET_ALL,
    ]
    table = []

    for record in book.values():
        phones = (
            ", ".join(phone.value for phone in record.phones) if record.phones else "-"
        )
        email = record.email.value if record.email else "-"
        address = record.address.value if record.address else "-"
        birthday = (
            record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "-"
        )
        table.append([record.name.value, phones, email, address, birthday])

    return tabulate(table, headers=headers, tablefmt="fancy_grid")


def format_notes(notebook):
    """Форматує нотатки у кольорову таблицю"""
    headers = [
        Fore.MAGENTA + "ID" + Style.RESET_ALL,
        Fore.MAGENTA + "Text" + Style.RESET_ALL,
        Fore.MAGENTA + "Tags" + Style.RESET_ALL,
    ]
    table = []

    for note_id, note in notebook.data.items():
        tags_str = ", ".join(note.tags) if note.tags else "-"
        table.append([note_id, note.text, tags_str])

    return tabulate(table, headers=headers, tablefmt="fancy_grid")


def format_notes_list(notes):
    headers = [
        Fore.MAGENTA + "ID" + Style.RESET_ALL,
        Fore.MAGENTA + "Text" + Style.RESET_ALL,
        Fore.MAGENTA + "Tags" + Style.RESET_ALL,
    ]
    table = []

    for note_id, note in notes:
        tags = ", ".join(note.tags) if note.tags else "-"
        table.append([note_id, note.text, tags])

    return tabulate(table, headers=headers, tablefmt="fancy_grid")
