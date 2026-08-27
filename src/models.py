import re
from collections import UserDict
from datetime import datetime

from config import ERRORS
from constants import DATE_FORMAT, PHONE_FORMAT, EMAIL_FORMAT

class Field:
    """Base class for record fields."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Class for storing contact name. Required field."""
    def __init__(self, value):
        # TODO: Implement name validation
        super().__init__(value)

class Phone(Field):
    """Class for storing phone number. Format: 10 digits."""
    def __init__(self, value):
        if not re.search(PHONE_FORMAT,value):
            raise ValueError(ERRORS["invalid_phone"])
        super().__init__(value)

class Email(Field):
    """Class for storing email."""
    def __init__(self, value):
        if not re.search(EMAIL_FORMAT,value):
            raise ValueError(ERRORS["invalid_email"])
        super().__init__(value)

class Address(Field):
    """Class for storing contact physical address."""
    def __init__(self, value):
        # TODO: Implement saving address
        super().__init__(value)

class Birthday(Field):
    """Class for storing birthday. Format: DD.MM.YYYY."""
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(ERRORS["invalid_birthday"])
        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)

class Tag(Field):
    """Class for note tags."""
    def __init__(self, value):
        # TODO: Implement saving tag (remove #, lowercase)
        super().__init__(value)

class Record:
    """Class for storing contact info (name, phones, email, address, birthday)."""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.addresses: list[Address] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        # TODO: Implement adding phone
        pass

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        # TODO: Implement editing phone
        pass

    def find_phone(self, phone: str) -> Phone | None:
        # TODO: Implement finding phone
        pass

    def remove_phone(self, phone: str) -> None:
        # TODO: Implement deleting phone
        pass

    def add_email(self, email: str) -> None:
        # TODO: Implement adding email
        pass

    def add_address(self, address: str) -> None:
        # TODO: Implement adding address
        pass

    def add_birthday(self, birthday: str) -> None:
        # TODO: Implement setting birthday
        pass

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) or "None"
        emails_str = "; ".join(e.value for e in self.emails) or "None"
        addresses_str = "; ".join(a.value for a in self.addresses) or "None"
        birthday_str = str(self.birthday) if self.birthday else "None"
        return f"Contact name: {self.name.value}, phones: {phones_str}, emails: {emails_str}, addresses: {addresses_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    """Class for managing contacts (contacts database)."""
    def add_record(self, record: Record) -> None:
        # TODO: Add record to self.data with name as key
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        # TODO: Search contact by name
        return self.data.get(name)

    def delete(self, name: str) -> None:
        # TODO: Delete contact by name
        if name in self.data:
            del self.data[name]

    def search(self, query: str) -> list[Record]:
        # TODO: Search contacts by query substring
        return []

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        # TODO: Implement list of birthdays for next N days
        return []

class Note:
    """
    Represents a single note with an ID, title, content, and optional tags.

    Args:
        note_id (int): The unique identifier for the note.
        title (str): The title of the note.
        content (str): The text content of the note.
        tags (list[str] | None, optional): A list of tags to associate with the note. Defaults to None.
    
    Returns:
        Note: A new instance of Note.
    """
    def __init__(self, note_id: int, title: str, content: str, tags: list[str] | None = None):
        self.id = note_id
        self.title = title.strip()
        self.content = content.strip()
        self.tags: list[Tag] = []
        if tags:
            for t in tags:
                self.add_tag(t)

    def add_tag(self, tag: str) -> None:
        tag_clean = tag.lstrip("#").lower()
        if not any(t.value == tag_clean for t in self.tags):
            self.tags.append(Tag(tag_clean))

    def edit_content(self, new_content: str):
        if not new_content.strip():
            raise ValueError("Content cannot be empty")
        self.content = new_content.strip()

    def __str__(self):
        tags_str = ", ".join(f"#{tag.value}" for tag in self.tags)
        return f"[{self.title}] {self.content} (Tags: {tags_str if tags_str else 'None'})"

class NoteBook(UserDict[int, Note]):
    """
    A collection of Note objects, managed as a dictionary mapping note IDs to Note instances.

    Args:
        None

    Returns:
        NoteBook: A new empty instance of NoteBook.
    """
    def __init__(self):
        super().__init__()
        self._next_id: int = 1

    def add_note(self, title: str, content: str, tags: list[str] | None = None) -> Note:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")

        note_id = max(self.data.keys(), default=0) + 1
        note = Note(note_id, title, content, tags)
        self.data[note_id] = note
        return note

    def edit_note(self, identifier: str | int, new_content: str) -> bool:
        note = self.find_note(identifier)
        if note:
            note.edit_content(new_content)
            return True
        return False
    
    def find_note(self, identifier: str | int) -> Note | None:
        if str(identifier).isdigit():
            return self.data.get(int(identifier))
        # Search by name
        for note in self.data.values():
            if note.title.lower() == str(identifier).lower():
                return note
        return None

    def delete_note(self, identifier: str | int) -> bool:
        note = self.find_note(identifier)
        if note:
            del self.data[note.id]
            return True
        return False

    def search_notes(self, query: str) -> list[Note]:
        """
        Searches for notes containing the query string in either the title or content.
        The search is case-insensitive.
        """
        query_lower = query.lower()
        return [
            note for note in self.data.values() 
            if query_lower in note.title.lower() or query_lower in note.content.lower()
        ]

    def search_by_tag(self, tag: str) -> list[Note]:
        tag_clean = tag.lstrip("#").lower()
        return [
            note for note in self.data.values()
            if any(t.value == tag_clean for t in note.tags)
        ]

    def sort_notes_by_tags(self) -> list[Note]:
        return sorted(self.data.values(), key=lambda n: len(n.tags), reverse=True)
