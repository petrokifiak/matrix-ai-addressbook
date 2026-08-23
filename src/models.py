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
    """Клас для зберігання окремої нотатки (id/title, content, tags)."""
    def __init__(self, title: str, content: str, tags: list[str] | None = None):
        self.title = title
        self.content = content
        self.tags = [Tag(t) for t in (tags or [])]

    def add_tag(self, tag: str) -> None:
        # TODO: Додати тег до нотатки
        pass

    def __str__(self):
        tags_str = ", ".join(f"#{t.value}" for t in self.tags)
        return f"[{self.title}] {self.content} (Tags: {tags_str if tags_str else 'None'})"

class NoteBook(UserDict):
    """Клас для управління нотатками."""
    def add_note(self, note: Note) -> None:
        # TODO: Додати нотатку
        self.data[note.title] = note

    def find_note(self, query: str) -> Note | None:
        # TODO: Знайти нотатку
        return self.data.get(query)

    def delete_note(self, title: str) -> bool:
        # TODO: Видалити нотатку
        if title in self.data:
            del self.data[title]
            return True
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
