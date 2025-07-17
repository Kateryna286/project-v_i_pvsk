from handlers import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    add_email,
    add_address,
    delete_contact,
    find_contact,
    add_note,
    find_note,
    delete_note,
    edit_note,
    show_notes,
    show_help,
    greet,
)
from models import AddressBook, NoteBook
from utils import parse_input
from storage import save_data, load_data, save_notebook, load_notebook
from colorama import Fore, Style, init

init(autoreset=True)


def main():
    book = load_data()
    notebook = load_notebook()

    print(Fore.CYAN + greet())

    try:
        while True:
            user_input = input(Fore.CYAN + ">>> " + Style.RESET_ALL)
            command, args = parse_input(user_input)

            if command in ("exit", "close"):
                print(Fore.GREEN + "Session ended. Goodbye!")
                break
            elif command == "add":
                print(Fore.GREEN + add_contact(args, book))
            elif command == "add-birthday":
                print(Fore.GREEN + add_birthday(args, book))
            elif command == "add-note":
                print(Fore.GREEN + add_note(args, notebook))
            elif command == "all":
                print(Fore.YELLOW + show_all(book))
            elif command == "birthdays":
                print(Fore.YELLOW + birthdays(book))
            elif command == "change":
                print(Fore.GREEN + change_contact(args, book))
            elif command == "phone":
                print(Fore.YELLOW + show_phone(args, book))
            elif command == "show-birthday":
                print(Fore.YELLOW + show_birthday(args, book))
            elif command == "find-note":
                print(Fore.YELLOW + find_note(args, notebook))
            elif command == "del-note":
                print(Fore.RED + delete_note(args, notebook))
            elif command == "del-contact":
                print(Fore.RED + delete_contact(args, book))
            elif command == "edit-note":
                print(Fore.GREEN + edit_note(args, notebook))
            elif command == "show-notes":
                print(Fore.YELLOW + show_notes(notebook))
            elif command == "hello":
                print(Fore.CYAN + "Hello! How can I assist you today?")
            elif command == "help":
                print(Fore.YELLOW + show_help())
            else:
                print(
                    Fore.RED
                    + "Sorry, I did not recognize that command. Please try again."
                )
    except KeyboardInterrupt:
        print(Fore.RED + "\nSession interrupted. Saving your data and exiting...")
    finally:
        save_data(book)
        save_notebook(notebook)


if __name__ == "__main__":
    main()
