from collections import UserDict

class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    def __init__(self, value):
        # TODO: Реалізувати валідацію імені
        super().__init__(value)

class Phone(Field):
    """Клас для зберігання номера телефону. Формат: 10 цифр."""
    def __init__(self, value):
        # TODO: Реалізувати перевірку формату (10 цифр)
        super().__init__(value)

class Email(Field):
    """Клас для зберігання електронної пошти."""
    def __init__(self, value):
        # TODO: Реалізувати перевірку формату email через регулярні вирази
        super().__init__(value)

class Address(Field):
    """Клас для зберігання фізичної адреси контакту."""
    def __init__(self, value):
        # TODO: Реалізувати збереження адреси
        super().__init__(value)

class Birthday(Field):
    """Клас для зберігання дня народження. Формат: DD.MM.YYYY."""
    def __init__(self, value):
        # TODO: Реалізувати конвертацію у datetime.date та валідацію
        super().__init__(value)

class Tag(Field):
    """Клас для тегів нотатки."""
    def __init__(self, value):
        # TODO: Реалізувати збереження тегу (очищення від #, lowercase)
        super().__init__(value)

class Record:
    """Клас для зберігання інформації про контакт (ім'я, телефони, email, адреса, день народження)."""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.addresses: list[Address] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        # TODO: Реалізувати додавання телефону
        pass

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        # TODO: Реалізувати редагування телефону
        pass

    def find_phone(self, phone: str) -> Phone | None:
        # TODO: Реалізувати пошук телефону
        pass

    def remove_phone(self, phone: str) -> None:
        # TODO: Реалізувати видалення телефону
        pass

    def add_email(self, email: str) -> None:
        # TODO: Реалізувати додавання email
        pass

    def add_address(self, address: str) -> None:
        # TODO: Реалізувати додавання адреси
        pass

    def add_birthday(self, birthday: str) -> None:
        # TODO: Реалізувати встановлення дня народження
        pass

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) or "None"
        emails_str = "; ".join(e.value for e in self.emails) or "None"
        addresses_str = "; ".join(a.value for a in self.addresses) or "None"
        birthday_str = str(self.birthday) if self.birthday else "None"
        return f"Contact name: {self.name.value}, phones: {phones_str}, emails: {emails_str}, addresses: {addresses_str}, birthday: {birthday_str}"

class AddressBook(UserDict):
    """Клас для управління контактами (база даних контактів)."""
    def add_record(self, record: Record) -> None:
        # TODO: Додати запис у self.data за ключем імені
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        # TODO: Пошук контакту за ім'ям
        return self.data.get(name)

    def delete(self, name: str) -> None:
        # TODO: Видалення контакту за ім'ям
        if name in self.data:
            del self.data[name]

    def search(self, query: str) -> list[Record]:
        # TODO: Пошук контактів за підрядком query
        return []

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        # TODO: Реалізувати список іменинників на наступні N днів
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

    def delete_note(self, title: str) -> bool:
        # TODO: Видалити нотатку
        return False

    def search_notes(self, query: str) -> list[Note]:
        # TODO: Пошук нотаток за підрядком у заголовку чи вмісті
        return []

    def search_by_tag(self, tag: str) -> list[Note]:
        # TODO: Пошук нотаток за тегом
        return []

    def sort_notes_by_tags(self) -> list[Note]:
        # TODO: Сортування нотаток за кількістю тегів
        return []
