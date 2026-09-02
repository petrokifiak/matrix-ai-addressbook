import os
from pathlib import Path

from config import ERRORS, MESSAGES
from models.address_book import AddressBook
from models.record import Record
from models.notebook import NoteBook
from storage.base import BaseExporter
from storage.strategies import ExportStrategy, JSONExportStrategy, CSVExportStrategy

def _resolve_filepath(filepath: str) -> str:
    path = Path(filepath)
    if len(path.parts) == 1:
        data_dir = Path(__file__).parent.parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        return str(data_dir / filepath)
    return filepath

class FileExporter(BaseExporter):
    """Acts as a Factory to select the correct ExportStrategy based on extension."""

    def _get_strategy(self, filepath: str) -> ExportStrategy:
        if filepath.endswith(".json"):
            return JSONExportStrategy()
        elif filepath.endswith(".csv"):
            return CSVExportStrategy()
        raise ValueError(ERRORS["unsupported_format"])

    def export_contacts(self, book: AddressBook, filepath: str) -> str:
        filepath = _resolve_filepath(filepath)
        strategy = self._get_strategy(filepath)
        strategy.export_contacts(book, filepath)
        return MESSAGES["contacts_exported"]

    def import_contacts(self, book: AddressBook, filepath: str) -> str:
        filepath = _resolve_filepath(filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(ERRORS["file_not_found"])
            
        strategy = self._get_strategy(filepath)
        try:
            data = strategy.import_contacts(book, filepath)
        except Exception:
            raise ValueError(ERRORS["import_error"])

        for item in data:
            name = item.get("name")
            if not name:
                continue

            record = book.find(name)
            if not record:
                record = Record(name)
                book.add_record(record)

            for phone in item.get("phones", []):
                if phone.strip():
                    try:
                        record.add_phone(phone)
                    except ValueError:
                        print(f"Warning: Skipped invalid phone '{phone}' for '{name}'.")

            for email in item.get("emails", []):
                if email.strip():
                    try:
                        record.add_email(email)
                    except ValueError:
                        print(f"Warning: Skipped invalid email '{email}' for '{name}'.")

            for address in item.get("addresses", []):
                if address.strip():
                    try:
                        record.add_address(address)
                    except ValueError:
                        pass

            birthday = item.get("birthday", "")
            if birthday and birthday.strip() and not record.birthday:
                try:
                    record.add_birthday(birthday)
                except ValueError:
                    print(f"Warning: Skipped invalid birthday '{birthday}' for '{name}'.")

        return MESSAGES["contacts_imported"]

    def export_notes(self, notebook: NoteBook, filepath: str) -> str:
        filepath = _resolve_filepath(filepath)
        strategy = self._get_strategy(filepath)
        strategy.export_notes(notebook, filepath)
        return MESSAGES["notes_exported"]

    def import_notes(self, notebook: NoteBook, filepath: str) -> str:
        filepath = _resolve_filepath(filepath)
        if not os.path.exists(filepath):
            raise FileNotFoundError(ERRORS["file_not_found"])
            
        strategy = self._get_strategy(filepath)
        try:
            data = strategy.import_notes(notebook, filepath)
        except Exception:
            raise ValueError(ERRORS["import_error"])

        for item in data:
            title = item.get("title")
            content = item.get("content")
            tags = item.get("tags", [])
            
            if not title or not content:
                continue
                
            try:
                notebook.add_note(title, content, tags)
            except ValueError:
                pass

        return MESSAGES["notes_imported"]
