from commands.registry import CommandRegistry
from commands.base import Context
from commands.contact_commands import (
    AddContactCommand, ChangeContactCommand, DeleteContactCommand,
    RestoreContactCommand, SearchContactsCommand, ShowPhoneCommand,
    AddPhoneCommand, AddEmailCommand, ShowEmailCommand,
    AddAddressCommand, ShowAddressCommand, AddBirthdayCommand,
    ShowBirthdayCommand, BirthdaysCommand, ShowAllCommand,
    ShowArchivedCommand, ExportContactsCommand, ImportContactsCommand,
    ClearContactsCommand
)
from commands.note_commands import (
    AddNoteCommand, ShowNotesCommand, SearchNotesCommand,
    EditNoteCommand, DeleteNoteCommand, AddTagCommand,
    SearchByTagCommand, SortNotesCommand, ExportNotesCommand,
    ImportNotesCommand, ClearNotesCommand
)
from commands.system_commands import (
    HelloCommand, HelpCommand, ClearDataCommand
)
from constants import Command
from storage.pickle_storage import PickleStorage
from core.middleware import LoggingMiddleware, ValidationMiddleware
from core.events import dispatcher, LoggingObserver

class Application:
    """Core application state container."""
    def __init__(self):
        self.storage = PickleStorage()
        book, notebook = self.storage.load()
        self.context = Context(address_book=book, notebook=notebook)
        self.registry = CommandRegistry()
        self._setup_middleware()
        self._setup_observers()
        self._register_commands()

    def _setup_middleware(self):
        log_mw = LoggingMiddleware()
        val_mw = ValidationMiddleware()
        log_mw.set_next(val_mw)
        self.registry.set_middleware(log_mw)

    def _setup_observers(self):
        observer = LoggingObserver()
        dispatcher.subscribe("CONTACT_ADDED", observer.on_contact_added)
        dispatcher.subscribe("NOTE_ADDED", observer.on_note_added)

    def _register_commands(self):
        # System
        self.registry.register(Command.HELLO.value, HelloCommand())
        self.registry.register(Command.HELP.value, HelpCommand())
        self.registry.register(Command.CLEAR_DATA.value, ClearDataCommand())
        
        # Contacts
        self.registry.register(Command.ADD.value, AddContactCommand())
        self.registry.register(Command.CHANGE.value, ChangeContactCommand())
        self.registry.register(Command.DELETE.value, DeleteContactCommand())
        self.registry.register(Command.DELETE_CONTACT.value, DeleteContactCommand())
        self.registry.register(Command.RESTORE_CONTACT.value, RestoreContactCommand())
        self.registry.register(Command.ARCHIVED.value, ShowArchivedCommand())
        self.registry.register(Command.SEARCH_CONTACTS.value, SearchContactsCommand())
        self.registry.register(Command.FIND_CONTACTS.value, SearchContactsCommand())
        self.registry.register(Command.PHONE.value, ShowPhoneCommand())
        self.registry.register(Command.ADD_PHONE.value, AddPhoneCommand())
        self.registry.register(Command.ADD_EMAIL.value, AddEmailCommand())
        self.registry.register(Command.SHOW_EMAIL.value, ShowEmailCommand())
        self.registry.register(Command.ADD_ADDRESS.value, AddAddressCommand())
        self.registry.register(Command.SHOW_ADDRESS.value, ShowAddressCommand())
        self.registry.register(Command.ADD_BIRTHDAY.value, AddBirthdayCommand())
        self.registry.register(Command.SHOW_BIRTHDAY.value, ShowBirthdayCommand())
        self.registry.register(Command.BIRTHDAYS.value, BirthdaysCommand())
        self.registry.register(Command.ALL.value, ShowAllCommand())
        self.registry.register(Command.EXPORT_CONTACTS.value, ExportContactsCommand())
        self.registry.register(Command.IMPORT_CONTACTS.value, ImportContactsCommand())
        self.registry.register(Command.CLEAR_CONTACTS.value, ClearContactsCommand())

        # Notes
        self.registry.register(Command.ADD_NOTE.value, AddNoteCommand())
        self.registry.register(Command.SHOW_NOTES.value, ShowNotesCommand())
        self.registry.register(Command.ALL_NOTES.value, ShowNotesCommand())
        self.registry.register(Command.SEARCH_NOTES.value, SearchNotesCommand())
        self.registry.register(Command.EDIT_NOTE.value, EditNoteCommand())
        self.registry.register(Command.DELETE_NOTE.value, DeleteNoteCommand())
        self.registry.register(Command.ADD_TAG.value, AddTagCommand())
        self.registry.register(Command.SEARCH_BY_TAG.value, SearchByTagCommand())
        self.registry.register(Command.SORT_NOTES_BY_TAGS.value, SortNotesCommand())
        self.registry.register(Command.EXPORT_NOTES.value, ExportNotesCommand())
        self.registry.register(Command.IMPORT_NOTES.value, ImportNotesCommand())
        self.registry.register(Command.CLEAR_NOTES.value, ClearNotesCommand())

    def execute(self, command_name: str, args: list[str]) -> str:
        return self.registry.execute(command_name, args, self.context)

    def save(self):
        self.storage.save(self.context.address_book, self.context.notebook)
