import re
from collections import UserDict
from datetime import date, datetime, timedelta

from config import ERRORS
from constants import DATE_FORMAT, PHONE_FORMAT, EMAIL_FORMAT

def birthday_in_year(bday: date, year: int) -> date:
    try:
        return bday.replace(year=year)
    except ValueError:
        return bday.replace(year=year, month=2, day=28)

class Field:
    """Base class for record fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing contact name. Required field."""

    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError("Name cannot be empty")
        super().__init__(str(value).strip())


class Phone(Field):
    """Class for storing phone number. Format: 10 digits."""

    def __init__(self, value):
        clean_value = str(value).strip()
        if not re.search(PHONE_FORMAT, clean_value):
            raise ValueError(ERRORS["invalid_phone"])
        super().__init__(clean_value)


class Email(Field):
    """Class for storing email."""

    def __init__(self, value):
        clean_value = str(value).strip()
        if not re.search(EMAIL_FORMAT, clean_value):
            raise ValueError(ERRORS["invalid_email"])
        super().__init__(clean_value)


class Address(Field):
    """Class for storing contact physical address."""

    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError("Address cannot be empty")
        super().__init__(str(value).strip())


class Birthday(Field):
    """Class for storing birthday. Format: DD.MM.YYYY."""

    def __init__(self, value):
        try:
            birthday = datetime.strptime(
                str(value).strip(), DATE_FORMAT
            ).date()
        except ValueError:
            raise ValueError(ERRORS["invalid_birthday"])
        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)


class Tag(Field):
    """Class for note tags."""

    def __init__(self, value):
        clean_value = str(value).lstrip("#").strip().lower()
        if not clean_value:
            raise ValueError("Tag cannot be empty")
        super().__init__(clean_value)


class Record:
    """Class for storing contact info (name, phones, email, address, birthday)."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.addresses: list[Address] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        p = Phone(phone)
        if not any(item.value == p.value for item in self.phones):
            self.phones.append(p)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        old_clean = str(old_phone).strip()
        p = self.find_phone(old_clean)
        if p is None:
            raise ValueError("Phone number not found.")
        new_p = Phone(new_phone)
        p.value = new_p.value

    def find_phone(self, phone: str) -> Phone | None:
        clean_phone = str(phone).strip()
        return next((p for p in self.phones if p.value == clean_phone), None)

    def remove_phone(self, phone: str) -> None:
        p = self.find_phone(phone)
        if p is None:
            raise ValueError("Phone number not found.")
        self.phones.remove(p)

    def add_email(self, email: str) -> None:
        e = Email(email)
        if not any(item.value == e.value for item in self.emails):
            self.emails.append(e)

    def add_address(self, address: str) -> None:
        a = Address(address)
        self.addresses.append(a)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def get_age(self, on_date: date | None = None) -> int | None:
        if not self.birthday:
            return None
        on_date = on_date or date.today()
        bday = self.birthday.value
        age = on_date.year - bday.year
        if on_date < birthday_in_year(bday, on_date.year):
            age -= 1
        return age

    def get_turning_age(self, on_date: date | None = None) -> int | None:
        age = self.get_age(on_date)
        return None if age is None else age + 1

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) or "None"
        emails_str = "; ".join(e.value for e in self.emails) or "None"
        addresses_str = "; ".join(a.value for a in self.addresses) or "None"
        birthday_str = str(self.birthday) if self.birthday else "None"
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones_str}, "
            f"emails: {emails_str}, "
            f"addresses: {addresses_str}, "
            f"birthday: {birthday_str}"
        )


class AddressBook(UserDict):
    """Class for managing contacts (contacts database)."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError

    def search(self, query: str) -> list[Record]:
        query_lower = query.lower()
        results = []
        for record in self.data.values():
            if query_lower in record.name.value.lower():
                results.append(record)
                continue
            if any(query_lower in p.value.lower() for p in record.phones):
                results.append(record)
                continue
            if any(query_lower in e.value.lower() for e in record.emails):
                results.append(record)
                continue
            if any(query_lower in a.value.lower() for a in record.addresses):
                results.append(record)
                continue
        return results

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        today = date.today()
        upcoming = []
        for record in self.data.values():
            if not record.birthday:
                continue
            bday = record.birthday.value  # datetime.date object
            bday_this_year = birthday_in_year(bday, today.year)
            if bday_this_year < today:
                bday_this_year = birthday_in_year(bday, today.year + 1)

            delta = (bday_this_year - today).days
            if 0 <= delta <= days:
                congratulation_date = bday_this_year
                if congratulation_date.weekday() == 5:  # Saturday -> Monday
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # Sunday -> Monday
                    congratulation_date += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime(DATE_FORMAT),
                    # Count from the birthday itself, not from the date shifted to Monday
                    "age": bday_this_year.year - bday.year
                })
        return upcoming


class Note:
    """Represents a single note with an ID, title, content, and optional tags.

    Args:
        note_id (int): The unique identifier for the note.
        title (str): The title of the note.
        content (str): The text content of the note.
        tags (list[str] | None, optional): Tags to associate with the note.
            Defaults to None.

    Returns:
        Note: A new instance of Note.
    """

    def __init__(
        self,
        note_id: int,
        title: str,
        content: str,
        tags: list[str] | None = None,
    ):
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
        return (
            f"[{self.title}] {self.content} "
            f"(Tags: {tags_str if tags_str else 'None'})"
        )


class NoteBook(UserDict[int, Note]):
    """A collection of Note objects managed as a dictionary of IDs to Notes.

    Args:
        None

    Returns:
        NoteBook: A new empty instance of NoteBook.
    """

    def __init__(self):
        super().__init__()
        self._next_id: int = 1

    def add_note(
        self,
        title: str,
        content: str,
        tags: list[str] | None = None,
    ) -> Note:
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
        """Search notes containing the query in title or content (case-insensitive)."""
        query_lower = query.lower()
        return [
            note
            for note in self.data.values()
            if (
                query_lower in note.title.lower()
                or query_lower in note.content.lower()
            )
        ]

    def search_by_tag(self, tag: str) -> list[Note]:
        tag_clean = tag.lstrip("#").lower()
        return [
            note
            for note in self.data.values()
            if any(t.value == tag_clean for t in note.tags)
        ]

    def sort_notes_by_tags(self, tags: list[str] | None = None) -> list[Note]:
        """Sort notes by specified tags (match count descending).

        If no tags are specified, sorts all notes by total number of tags.
        """
        if tags:
            clean_tags = [
                t.lstrip("#").strip().lower() for t in tags if t.strip()
            ]
            scored_notes = []
            # Iterate through all stored notes in the notebook
            for note in self.data.values():
                # Extract clean string values of all tags assigned to note
                note_tag_vals = {t.value for t in note.tags}
                # Calculate how many searched tags match the current note
                match_count = sum(1 for t in clean_tags if t in note_tag_vals)
                # If at least one matching tag, include note with score
                if match_count > 0:
                    scored_notes.append((match_count, note))
            # Sort by match count descending, then by total tags descending
            scored_notes.sort(
                key=lambda item: (item[0], len(item[1].tags)),
                reverse=True,
            )
            return [note for _, note in scored_notes]

        return sorted(
            self.data.values(),
            key=lambda n: len(n.tags),
            reverse=True,
        )

