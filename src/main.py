from handlers import add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays, add_email, add_address, delete_contact, find_contact, add_note, find_note, delete_note, edit_note, show_notes, show_help
from models import AddressBook, NoteBook
from utils import parse_input
from storage import save_data, load_data, save_notebook, load_notebook


def main():
    """Main loop for handling user commands."""
    book = load_data()
    notebook = load_notebook()
    print("Welcome to your assistant bot!\nPlease write \"help\" to see the commands")

    try:
        while True:
            user_input = input(">>> ")
            command, args = parse_input(user_input)

            if command in ("exit", "close"):
                print("Goodbye!")
                break
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(show_all(book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(book))
            elif command == "add-note":
                print(add_note(args, notebook))
            elif command == "find-note":
                print(find_note(args, notebook))
            elif command == "del-note":
                print(delete_note(args, notebook))
            elif command == "del-contact":
                print(delete_contact(args, book))
            elif command == "edit-note":
                print(edit_note(args, notebook))
            elif command == "show-notes":
                print(show_notes(notebook))
            elif command == "hello":
                print("How can I help you?")
            elif command == "help":
                print(show_help())
            else:
                print("Unknown command. Try again.")
    except KeyboardInterrupt:
        print("\nInterrupted. Saving data and exiting.")
    finally:
        save_data(book)
        save_notebook(notebook)


if __name__ == "__main__":
    main()
