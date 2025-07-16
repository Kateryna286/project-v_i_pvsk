from handlers import add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays, add_email, add_address, delete_contact, find_contact, add_note, find_note, delete_note, edit_note, show_help
from models import AddressBook, NoteBook
from utils import parse_input
from storage import save_data, load_data


def main():
    """Main loop for handling user commands."""
    
    book = load_data()
    print("Welcome to your assistant bot!")

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
        elif command == "hello":
            print("How can I help you?")
        elif command == "help":
            print(show_help())
        else:
            print("Unknown command. Try again.")

    save_data(book)


if __name__ == "__main__":
    main()
