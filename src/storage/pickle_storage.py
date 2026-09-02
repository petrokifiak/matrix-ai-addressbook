import os
import pickle
from pathlib import Path
from typing import Tuple

from models.address_book import AddressBook
from models.notebook import NoteBook
from storage.base import StorageBackend

DEFAULT_STORAGE_DIR = Path.home() / ".personal_assistant"
DEFAULT_STORAGE_FILENAME = "assistant_data.pkl"
DEFAULT_STORAGE_FILE = DEFAULT_STORAGE_DIR / DEFAULT_STORAGE_FILENAME

def get_default_path() -> str:
    DEFAULT_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    return str(DEFAULT_STORAGE_FILE)

class PickleStorage(StorageBackend):
    def save(self, address_book: AddressBook, notebook: NoteBook, filename: str | None = None) -> None:
        target_path = filename if filename else get_default_path()
        with open(target_path, "wb") as file:
            pickle.dump({"contacts": address_book, "notes": notebook}, file)

    def load(self, filename: str | None = None) -> Tuple[AddressBook, NoteBook]:
        target_path = filename if filename else get_default_path()
        if os.path.exists(target_path):
            try:
                with open(target_path, "rb") as file:
                    data = pickle.load(file)
                    if isinstance(data, dict):
                        contacts = data.get("contacts", AddressBook())
                        notes = data.get("notes", NoteBook())
                        return contacts, notes
            except (FileNotFoundError, EOFError, pickle.UnpicklingError, AttributeError, ModuleNotFoundError) as e:
                pass
        return AddressBook(), NoteBook()
