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
        emails = (
            ", ".join(email.value for email in getattr(record, "emails", []))
            if hasattr(record, "emails")
            else "-"
        )
        addresses = (
            ", ".join(addr.value for addr in getattr(record, "addresses", []))
            if hasattr(record, "addresses")
            else "-"
        )
        birthday = (
            record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "-"
        )
        table.append([record.name, phones, emails, addresses, birthday])

    return tabulate(table, headers=headers, tablefmt="fancy_grid")


def format_notes(notebook):
    """Форматує нотатки у кольорову таблицю"""
    headers = [
        Fore.MAGENTA + "Title" + Style.RESET_ALL,
        Fore.MAGENTA + "Text" + Style.RESET_ALL,
    ]
    table = []

    for title, note in notebook.data.items():
        table.append([title, str(note)])

    return tabulate(table, headers=headers, tablefmt="fancy_grid")
