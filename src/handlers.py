import difflib
from decorators import input_error
from constants import Command
from config import ERRORS, MESSAGES
from models import AddressBook, Record, NoteBook
from help import get_help

def get_record(book: AddressBook, name: str) -> Record:
    """Helper function to get a record or raise KeyError."""
    record = book.find(name)
    if record is None:
        raise KeyError
    return record

# region Contact Handlers
@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Handler for adding a contact.
    Syntax: add <name> <phone>
    """
    if len(args) < 2:
        raise IndexError
    name, phone = args[0], args[1]
    record = book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    else:
        record.add_phone(phone)
    return MESSAGES["contact_added"]

@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """
    Handler for changing a phone number.
    Syntax: change <name> <old_phone> <new_phone>
    """
    if len(args) < 3:
        raise IndexError
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = get_record(book, name)
    record.edit_phone(old_phone, new_phone)
    return MESSAGES["contact_updated"]

@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """
    Handler for deleting a contact.
    Syntax: delete-contact <name>
    """
    if not args:
        raise IndexError
    name = args[0]
    book.delete(name)
    return MESSAGES["contact_deleted"]

@input_error
def search_contacts(args: list[str], book: AddressBook) -> str:
    """
    Handler for searching contacts by query substring.
    Syntax: search-contacts <query>
    """
    if not args:
        raise IndexError
    query = " ".join(args)
    results = book.search(query)
    if not results:
        return MESSAGES["no_matching_contacts"]
    return "\n".join(str(record) for record in results)

@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """
    Handler for showing contact phone numbers.
    Syntax: phone <name>
    """
    if not args:
        raise IndexError
    name = args[0]
    record = get_record(book, name)
    if not record.phones:
        return f"No phone numbers found for {record.name.value}."
    return "; ".join(p.value for p in record.phones)

@input_error
def add_phone(args: list[str], book: AddressBook) -> str:
    """
    Handler for adding an additional phone number.
    Syntax: add-phone <name> <phone>
    """
    if len(args) < 2:
        raise IndexError
    name, phone = args[0], args[1]
    record = get_record(book, name)
    record.add_phone(phone)
    return MESSAGES["phone_added"]

@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    """
    Handler for adding an email to contact.
    Syntax: add-email <name> <email>
    """
    if len(args) < 2:
        raise IndexError
    name, email = args[0], args[1]
    record = get_record(book, name)
    record.add_email(email)
    return MESSAGES["email_added"]

@input_error
def show_email(args: list[str], book: AddressBook) -> str:
    """
    Handler for showing contact email.
    Syntax: show-email <name>
    """
    if not args:
        raise IndexError
    name = args[0]
    record = get_record(book, name)
    if not record.emails:
        return ERRORS["no_email"]
    return "; ".join(e.value for e in record.emails)

@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    """
    Handler for adding contact address.
    Syntax: add-address <name> <address...>
    """
    if len(args) < 2:
        raise IndexError
    name = args[0]
    address = " ".join(args[1:])
    record = get_record(book, name)
    record.add_address(address)
    return MESSAGES["address_added"]

@input_error
def show_address(args: list[str], book: AddressBook) -> str:
    """
    Handler for showing contact address.
    Syntax: show-address <name>
    """
    if not args:
        raise IndexError
    name = args[0]
    record = get_record(book, name)
    if not record.addresses:
        return ERRORS["no_address"]
    return "; ".join(a.value for a in record.addresses)

@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """
    Handler for adding birthday to contact.
    Syntax: add-birthday <name> <date>
    """
    if len(args) < 2:
        raise IndexError
    name, bday = args[0], args[1]
    record = get_record(book, name)
    record.add_birthday(bday)
    return MESSAGES["birthday_added"]

@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """
    Handler for showing contact birthday.
    Syntax: show-birthday <name>
    """
    if not args:
        raise IndexError
    name = args[0]
    record = get_record(book, name)
    if not record.birthday:
        return ERRORS["no_birthday"]
    return str(record.birthday)

@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """
    Handler for showing upcoming birthdays.
    Syntax: birthdays [days]
    """
    days = 7
    if args:
        try:
            days = int(args[0])
            if days <= 0:
                raise ValueError(ERRORS["invalid_days"])
        except ValueError as e:
            if str(e) == ERRORS["invalid_days"]:
                raise e
            raise ValueError(ERRORS["invalid_days"])
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return MESSAGES["no_upcoming_birthdays"]
    return "\n".join(f"{item['name']}: {item['congratulation_date']}" for item in upcoming)

@input_error
def show_all(book: AddressBook) -> str:
    """
    Handler for showing all saved contacts.
    Syntax: all
    """
    if not book.data:
        return MESSAGES["no_contacts"]
    return "\n".join(str(record) for record in book.data.values())
# endregion

# region Note Handler
@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    title = args[0]
    content = " ".join(args[1:])
    if not content:
        raise IndexError
    note = notebook.add_note(title, content)
    return f"{MESSAGES['note_added']} ID: {note.id}"

@input_error
def show_notes(notebook: NoteBook) -> str:
    if not notebook.data:
        return MESSAGES.get("no_notes", "No notes found.")
    return "\n".join(str(note) for note in notebook.data.values())

@input_error
def search_notes(args: list[str], notebook: NoteBook) -> str:
    query = " ".join(args)
    if not query:
        raise IndexError
    results = notebook.search_notes(query)
    if not results:
        return MESSAGES["no_matching_notes"]
    return "\n".join(str(note) for note in results)

@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    identifier = args[0]
    new_content = " ".join(args[1:])
    if not new_content:
        raise IndexError
    success = notebook.edit_note(identifier, new_content)
    if not success:
        raise ValueError(ERRORS["note_not_found"])
    return MESSAGES["note_updated"]

@input_error
def delete_note(args: list[str], notebook: NoteBook) -> str:
    identifier = args[0]
    success = notebook.delete_note(identifier)
    if not success:
        raise ValueError(ERRORS["note_not_found"])
    return MESSAGES["note_deleted"]

@input_error
def add_tag(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise IndexError
    identifier = args[0]
    tags = args[1:]
    note = notebook.find_note(identifier)
    if not note:
        raise ValueError(ERRORS["note_not_found"])
    for tag in tags:
        note.add_tag(tag)
    return MESSAGES.get("tag_added", "Tags added.")

@input_error
def search_by_tag(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise IndexError
    tag = args[0]
    results = notebook.search_by_tag(tag)
    if not results:
        return MESSAGES.get("no_matching_notes", "No notes found.")
    return "\n".join(str(note) for note in results)

@input_error
def sort_notes(notebook: NoteBook) -> str:
    results = notebook.sort_notes_by_tags()
    if not results:
        return MESSAGES.get("no_notes", "No notes found.")
    return "\n".join(str(note) for note in results)
# endregion

@input_error
def execute_command(command: str, args: list[str], address_book: AddressBook, notebook: NoteBook | None = None) -> str:
    """Bot command router."""
    if notebook is None:
        notebook = NoteBook()

    if command == Command.HELLO.value:
        return MESSAGES["hello"]
    elif command == Command.HELP.value:
        return get_help(args)
    elif command == Command.ADD.value:
        return add_contact(args, address_book)
    elif command == Command.CHANGE.value:
        return change_contact(args, address_book)
    elif command in [Command.DELETE.value, Command.DELETE_CONTACT.value]:
        return delete_contact(args, address_book)
    elif command in [Command.SEARCH_CONTACTS.value, Command.FIND_CONTACTS.value]:
        return search_contacts(args, address_book)
    elif command == Command.PHONE.value:
        return show_phone(args, address_book)
    elif command == Command.ADD_PHONE.value:
        return add_phone(args, address_book)
    elif command == Command.ADD_EMAIL.value:
        return add_email(args, address_book)
    elif command == Command.SHOW_EMAIL.value:
        return show_email(args, address_book)
    elif command == Command.ADD_ADDRESS.value:
        return add_address(args, address_book)
    elif command == Command.SHOW_ADDRESS.value:
        return show_address(args, address_book)
    elif command == Command.ADD_BIRTHDAY.value:
        return add_birthday(args, address_book)
    elif command == Command.SHOW_BIRTHDAY.value:
        return show_birthday(args, address_book)
    elif command == Command.BIRTHDAYS.value:
        return birthdays(args, address_book)
    elif command == Command.ALL.value:
        return show_all(address_book)
    elif command == Command.ADD_NOTE.value:
        return add_note(args, notebook)
    elif command in [Command.SHOW_NOTES.value, Command.ALL_NOTES.value]:
        return show_notes(notebook)
    elif command == Command.SEARCH_NOTES.value:
        return search_notes(args, notebook)
    elif command == Command.EDIT_NOTE.value:
        return edit_note(args, notebook)
    elif command == Command.DELETE_NOTE.value:
        return delete_note(args, notebook)
    elif command == Command.ADD_TAG.value:
        return add_tag(args, notebook)
    elif command == Command.SEARCH_BY_TAG.value:
        return search_by_tag(args, notebook)
    elif command == Command.SORT_NOTES_BY_TAGS.value:
        return sort_notes(notebook)
    else:
        valid_commands = [cmd.value for cmd in Command]
        matches = difflib.get_close_matches(command, valid_commands, n=3, cutoff=0.5)
        if matches:
            if len(matches) == 1:
                return f"Invalid command '{command}'. Did you mean: {matches[0]}?"
            suggestions = ", ".join(matches)
            return f"Invalid command '{command}'. Did you mean one of these: {suggestions}?"
        raise ValueError(ERRORS["invalid_command"])
