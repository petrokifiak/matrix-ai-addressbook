from enum import Enum


class Command(Enum):
    HELLO = "hello"
    ADD = "add"
    ADD_PHONE = "add-phone"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"
    CHANGE = "change"
    PHONE = "phone"
    DELETE_CONTACT = "delete-contact"
    DELETE = "delete"
    RESTORE_CONTACT = "restore-contact"
    ARCHIVED = "archived"
    SEARCH_CONTACTS = "search-contacts"
    FIND_CONTACTS = "find-contacts"
    ADD_EMAIL = "add-email"
    SHOW_EMAIL = "show-email"
    ADD_ADDRESS = "add-address"
    SHOW_ADDRESS = "show-address"
    ALL = "all"
    ADD_NOTE = "add-note"
    SHOW_NOTES = "show-notes"
    ALL_NOTES = "all-notes"
    SEARCH_NOTES = "search-notes"
    EDIT_NOTE = "edit-note"
    DELETE_NOTE = "delete-note"
    ADD_TAG = "add-tag"
    SEARCH_BY_TAG = "search-by-tag"
    SORT_NOTES_BY_TAGS = "sort-notes-by-tags"
    EXPORT_NOTES = "export-notes"
    IMPORT_NOTES = "import-notes"
    EXPORT_CONTACTS = "export-contacts"
    IMPORT_CONTACTS = "import-contacts"
    CLEAR_DATA = "clear-data"
    CLEAR_CONTACTS = "clear-contacts"
    CLEAR_NOTES = "clear-notes"
    CLOSE = "close"
    EXIT = "exit"
    HELP = "help"




DATE_FORMAT = "%d.%m.%Y"
PHONE_FORMAT = r"^\d{10}$"
EMAIL_FORMAT = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"


class Colors:
    CYAN = ''
    GREEN = ''
    RED = ''
    YELLOW = ''
    RESET = ''

