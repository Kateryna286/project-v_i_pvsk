from commands import COMMANDS, show_help, greet, suggest_command, show_commands_table
from models import AddressBook, NoteBook
from utils import parse_input
from storage import save_data, load_data, load_notebook
from colorama import Fore, Style, init

init(autoreset=True)


def main():
    book = load_data()
    notebook = load_notebook()

    print(greet())
    print(Fore.MAGENTA + "\nCommand Table:\n" + Style.RESET_ALL)
    show_commands_table()

    try:
        while True:
            user_input = input(Fore.CYAN + ">>> " + Style.RESET_ALL)
            command, args = parse_input(user_input)

            if command in ("exit", "close"):
                print(Fore.GREEN + "Session ended. Goodbye! 👋")
                break

            action = COMMANDS.get(command)
            if action:
                try:
                    result = action["func"](args, book, notebook)
                    print(action["color"] + result)
                except Exception as e:
                    print(Fore.RED + str(e))
            else:
                print(suggest_command(command))

    except KeyboardInterrupt:
        print(Fore.RED + "\nSession interrupted. Saving your data and exiting...")
    finally:
        save_data(book)
        save_data(notebook)


if __name__ == "__main__":
    main()
