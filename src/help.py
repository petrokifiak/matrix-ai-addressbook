from constants import Colors


HELP_DICT = {
    "Contacts": {
        "add": {
            "syntax": "add <name> <phone>",
            "desc": "Adds a new contact.",
            "example": "add John 0501234567",
        },
        "add-phone": {
            "syntax": "add-phone <name> <phone>",
            "desc": "Adds another phone to a contact.",
            "example": "add-phone John 0671234567",
        },
        "change": {
            "syntax": "change <name> <old_phone> <new_phone>",
            "desc": "Changes a phone number.",
            "example": "change John 0501234567 0671234567",
        },
        "phone": {
            "syntax": "phone <name>",
            "desc": "Shows phone numbers.",
            "example": "phone John",
        },
        "delete-contact": {
            "syntax": "delete-contact <name>",
            "desc": "Deletes a contact.",
            "example": "delete-contact John",
        },
        "all": {
            "syntax": "all [--all | -a]",
            "desc": "Shows all contacts (use --all or -a to include archived).",
            "example": "all --all",
        },
        "archived": {
            "syntax": "archived",
            "desc": "Shows all archived contacts.",
            "example": "archived",
        },
        "restore-contact": {
            "syntax": "restore-contact <name>",
            "desc": "Restores an archived contact.",
            "example": "restore-contact John",
        },
        "add-birthday": {
            "syntax": "add-birthday <name> <date>",
            "desc": "Adds a birthday.",
            "example": "add-birthday John 15.08.1995",
        },
        "show-birthday": {
            "syntax": "show-birthday <name>",
            "desc": "Shows a birthday.",
            "example": "show-birthday John",
        },
        "birthdays": {
            "syntax": "birthdays <days>",
            "desc": "Shows birthdays for the next N days.",
            "example": "birthdays 7",
        },
        "add-email": {
            "syntax": "add-email <name> <email>",
            "desc": "Adds an email.",
            "example": "add-email John john@mail.com",
        },
        "show-email": {
            "syntax": "show-email <name>",
            "desc": "Shows an email.",
            "example": "show-email John",
        },
        "add-address": {
            "syntax": "add-address <name> <address...>",
            "desc": "Adds an address.",
            "example": "add-address John Kyiv",
        },
        "show-address": {
            "syntax": "show-address <name>",
            "desc": "Shows an address.",
            "example": "show-address John",
        },
        "search-contacts": {
            "syntax": "search-contacts <query>",
            "desc": "Searches for contacts.",
            "example": "search-contacts John",
        },
        "export-contacts": {
            "syntax": "export-contacts <filename.csv|json>",
            "desc": "Exports contacts to a CSV or JSON file.",
            "example": "export-contacts backup.json",
        },
        "import-contacts": {
            "syntax": "import-contacts <filepath>",
            "desc": "Imports contacts from a CSV or JSON file.",
            "example": "import-contacts contacts_backup.csv",
        },
        "clear-contacts": {
            "syntax": "clear-contacts",
            "desc": "Clears all saved contacts.",
            "example": "clear-contacts",
        },
    },
    "Notes": {
        "add-note": {
            "syntax": "add-note <title> <content...>",
            "desc": "Creates a text note.",
            "example": "add-note Idea Build a robot",
        },
        "show-notes": {
            "syntax": "show-notes",
            "desc": "Shows all notes.",
            "example": "show-notes",
        },
        "search-notes": {
            "syntax": "search-notes <query>",
            "desc": "Searches for notes.",
            "example": "search-notes robot",
        },
        "edit-note": {
            "syntax": "edit-note <title_or_id> <new_content...>",
            "desc": "Edits a note.",
            "example": "edit-note Idea Build a smart robot",
        },
        "delete-note": {
            "syntax": "delete-note <title_or_id>",
            "desc": "Deletes a note.",
            "example": "delete-note Idea",
        },
        "add-tag": {
            "syntax": "add-tag <title_or_id> <tag1> [tag2...]",
            "desc": "Adds tags.",
            "example": "add-tag Idea tech fun",
        },
        "search-by-tag": {
            "syntax": "search-by-tag <tag>",
            "desc": "Searches by tag.",
            "example": "search-by-tag tech",
        },
        "sort-notes-by-tags": {
            "syntax": "sort-notes-by-tags [tag1 tag2...]",
            "desc": "Sorts notes by matching tags (or total tags).",
            "example": "sort-notes-by-tags work urgent",
        },
        "export-notes": {
            "syntax": "export-notes <filename.json>",
            "desc": "Exports notes to a JSON file.",
            "example": "export-notes notes_backup.json",
        },
        "import-notes": {
            "syntax": "import-notes <filepath.json>",
            "desc": "Imports notes from a JSON file.",
            "example": "import-notes notes_backup.json",
        },
        "clear-notes": {
            "syntax": "clear-notes",
            "desc": "Clears all saved notes.",
            "example": "clear-notes",
        },
    },
    "General": {
        "hello": {
            "syntax": "hello",
            "desc": "Displays a greeting message.",
            "example": "hello",
        },
        "clear-data": {
            "syntax": "clear-data",
            "desc": "Clears all saved contacts and notes.",
            "example": "clear-data",
        },
        "help": {
            "syntax": "help [command]",
            "desc": "Shows command help.",
            "example": "help add-note",
        },
        "close": {
            "syntax": "close",
            "desc": "Exits the program.",
            "example": "close",
        },
        "exit": {
            "syntax": "exit",
            "desc": "Exits the program.",
            "example": "exit",
        },
    },
}


def get_help(args: list[str]) -> str:
    """Prints interactive help for commands."""
    if not args:
        lines = [f"{Colors.YELLOW}Available categories:{Colors.RESET}"]
        for category in HELP_DICT.keys():
            lines.append(f"{Colors.CYAN}- {category}{Colors.RESET}")
        lines.append(
            f"\n{Colors.YELLOW}Type 'help <category>' "
            f"to see commands in a category.{Colors.RESET}"
        )
        lines.append(
            f"{Colors.YELLOW}Type 'help <command>' "
            f"to see details for a specific command.{Colors.RESET}"
        )
        return "\n".join(lines)

    command_name = args[0]

    # Check if user typed a category name (case-insensitive)
    for category, commands in HELP_DICT.items():
        if command_name.lower() == category.lower():
            lines = [f"{Colors.YELLOW}--- {category} ---{Colors.RESET}"]
            for cmd, info in commands.items():
                lines.append(
                    f"{Colors.CYAN}{cmd:<20}{Colors.RESET} : {info['desc']}"
                )
            lines.append(
                f"\n{Colors.YELLOW}For details type: help <command>{Colors.RESET}"
            )
            return "\n".join(lines)

    # Check if user typed a specific command
    for category, commands in HELP_DICT.items():
        if command_name in commands:
            info = commands[command_name]
            return (
                f"{Colors.YELLOW}Command:{Colors.RESET} "
                f"{Colors.CYAN}{command_name}{Colors.RESET}\n"
                f"{Colors.YELLOW}Description:{Colors.RESET} {info['desc']}\n"
                f"{Colors.YELLOW}Syntax:{Colors.RESET} {info['syntax']}\n"
                f"{Colors.YELLOW}Example:{Colors.RESET} {info['example']}"
            )

    return (
        f"{Colors.YELLOW}Command '{command_name}' not found. "
        f"Type 'help' for a list of commands.{Colors.RESET}"
    )

