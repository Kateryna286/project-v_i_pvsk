from colorama import Fore, Style, init
from tabulate import tabulate
import difflib

init(autoreset=True)


# ===============================
#         HELP FUNCTION
# ===============================
def show_help():
    result = ["\n📘 Available commands:"]
    for cmd, data in COMMANDS.items():
        result.append(f"{cmd} - {data['desc']}")
    result.append("exit / close - 👋 Exit the assistant")
    return "\n".join(result)


# ===============================
#         GREETING FUNCTION
# ===============================
def greet():
    return "\n".join(
        [
            f"{Fore.CYAN}🤖 Hello! I am your assistant bot.{Style.RESET_ALL}\n",
            f"{Fore.YELLOW}✨ Here is what I can do for you below in the table!:{Style.RESET_ALL}\n",
            f"{Fore.MAGENTA}❔ If you need help, just type 'help'.{Style.RESET_ALL}",
        ]
    )


# ===============================
#      SUGGESTION FUNCTION
# ===============================
def suggest_command(user_input):
    commands_list = list(COMMANDS.keys()) + ["exit", "close"]
    matches = difflib.get_close_matches(user_input, commands_list, n=3, cutoff=0.4)

    if matches:
        suggestions = []
        for cmd in matches:
            if cmd in COMMANDS:
                desc = COMMANDS[cmd]["desc"]
                suggestions.append(f"{Fore.GREEN}- {cmd}:{Style.RESET_ALL} {desc}")
            else:
                desc = "👋 Exit the assistant"
                suggestions.append(f"{Fore.GREEN}- {cmd}:{Style.RESET_ALL} {desc}")

        return f"{Fore.MAGENTA}🤔 Did you mean:{Style.RESET_ALL}\n" + "\n".join(
            suggestions
        )
    else:
        return f"{Fore.RED}❌ Unknown command.{Style.RESET_ALL} Type 'help' to see all available commands."


# ===============================
#         COMMAND HANDLERS
# ===============================
from handlers import (
    add_contact_interactive,
    add_birthday_interactive,
    add_email_interactive,
    add_address_interactive,
    add_phone_interactive,
    find_contact_interactive,
    show_all,
    birthdays_interactive,
    change_contact_interactive,
    show_phone_interactive,
    show_birthday_interactive,
    find_note_interactive,
    delete_note_interactive,
    delete_contact_interactive,
    edit_note_interactive,
    add_note_interactive,
    sort_notes_by_tag_interactive,
    show_notes,
)


# ===============================
#           COMMANDS
# ===============================
COMMANDS = {
    # ----- Contacts -----
    "add": {
        "func": lambda args, book, notebook: add_contact_interactive(book),
        "desc": "➕ Add a new contact",
        "color": Fore.GREEN,
    },
    "add-phone": {
        "func": lambda args, book, notebook: add_phone_interactive(book),
        "desc": "📞 Add phone to contact",
        "color": Fore.GREEN,
    },
    "add-email": {
        "func": lambda args, book, notebook: add_email_interactive(book),
        "desc": "📧 Add email to contact",
        "color": Fore.GREEN,
    },
    "add-birthday": {
        "func": lambda args, book, notebook: add_birthday_interactive(book),
        "desc": "🎂 Add birthday to contact",
        "color": Fore.GREEN,
    },
    "add-address": {
        "func": lambda args, book, notebook: add_address_interactive(book),
        "desc": "🏡 Add address to contact",
        "color": Fore.GREEN,
    },
    "find": {
        "func": lambda args, book, notebook: find_contact_interactive(book),
        "desc": "🔍 Search contacts",
        "color": Fore.YELLOW,
    },
    "phone": {
        "func": lambda args, book, notebook: show_phone_interactive(book),
        "desc": "📱 Show phone numbers for contact",
        "color": Fore.YELLOW,
    },
    "show-birthday": {
        "func": lambda args, book, notebook: show_birthday_interactive(book),
        "desc": "🎉 Show contact's birthday",
        "color": Fore.YELLOW,
    },
    "change": {
        "func": lambda args, book, notebook: change_contact_interactive(book),
        "desc": "✏️  Change contact's name, phone number, email, birthday, address",
        "color": Fore.GREEN,
    },
    "del": {
        "func": lambda args, book, notebook: delete_contact_interactive(book),
        "desc": "🗑️  Delete contact",
        "color": Fore.RED,
    },
    "all": {
        "func": lambda args, book, notebook: show_all(book),
        "desc": "📋 Show all contacts",
        "color": Fore.YELLOW,
    },
    "birthdays": {
        "func": lambda args, book, notebook: birthdays_interactive(book),
        "desc": "📅 Show upcoming birthdays",
        "color": Fore.YELLOW,
    },
    # ----- Notes -----
    "add-note": {
        "func": lambda args, book, notebook: add_note_interactive(notebook),
        "desc": "📝  Add a note",
        "color": Fore.GREEN,
    },
    "find-note": {
        "func": lambda args, book, notebook: find_note_interactive(notebook),
        "desc": "🔍  Find a note",
        "color": Fore.YELLOW,
    },
    "edit-note": {
        "func": lambda args, book, notebook: edit_note_interactive(notebook),
        "desc": "✏️  Edit a note",
        "color": Fore.GREEN,
    },
    "sort-note": {
        "func": lambda args, book, notebook: sort_notes_by_tag_interactive(notebook),
        "desc": "🏷️  Sort notes by tag",
        "color": Fore.YELLOW,
    },
    "del-note": {
        "func": lambda args, book, notebook: delete_note_interactive(notebook),
        "desc": "🗑️  Delete a note",
        "color": Fore.RED,
    },
    "notes": {
        "func": lambda args, book, notebook: show_notes(notebook),
        "desc": "📓  Show all notes",
        "color": Fore.YELLOW,
    },
    # ----- General -----
    "hello": {
        "func": lambda args, book, notebook: "👋 Hello! How can I assist you today?",
        "desc": "👋 Greeting",
        "color": Fore.CYAN,
    },
    "help": {
        "func": lambda args, book, notebook: show_help(),
        "desc": "❔ Show help message",
        "color": Fore.YELLOW,
    },
}


# ===============================
#        TABLE GENERATOR
# ===============================
def show_commands_table():
    table_data = []
    for command, info in COMMANDS.items():
        desc = info["desc"]
        color = info["color"]
        colored_command = f"{color}{command}{Style.RESET_ALL}"
        table_data.append([colored_command, desc])

    headers = ["Command", "Description", "Color"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


if __name__ == "__main__":
    show_commands_table()
