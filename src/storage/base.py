from abc import ABC, abstractmethod
from typing import Tuple

from models.address_book import AddressBook
from models.notebook import NoteBook

class StorageBackend(ABC):
    @abstractmethod
    def save(self, address_book: AddressBook, notebook: NoteBook, filename: str | None = None) -> None:
        pass

    @abstractmethod
    def load(self, filename: str | None = None) -> Tuple[AddressBook, NoteBook]:
        pass

class BaseExporter(ABC):
    @abstractmethod
    def export_contacts(self, book: AddressBook, filepath: str) -> str:
        pass

    @abstractmethod
    def import_contacts(self, book: AddressBook, filepath: str) -> str:
        pass

    @abstractmethod
    def export_notes(self, notebook: NoteBook, filepath: str) -> str:
        pass

    @abstractmethod
    def import_notes(self, notebook: NoteBook, filepath: str) -> str:
        pass
