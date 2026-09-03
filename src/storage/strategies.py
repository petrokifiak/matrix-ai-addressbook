import csv
import json
from abc import ABC, abstractmethod
from models.address_book import AddressBook
from models.notebook import NoteBook
from models.record import Record

class ExportStrategy(ABC):
    """Strategy interface for exporting/importing data."""
    @abstractmethod
    def export_contacts(self, book: AddressBook, filepath: str) -> None:
        pass

    @abstractmethod
    def import_contacts(self, book: AddressBook, filepath: str) -> list[dict]:
        pass
        
    @abstractmethod
    def export_notes(self, notebook: NoteBook, filepath: str) -> None:
        pass

    @abstractmethod
    def import_notes(self, notebook: NoteBook, filepath: str) -> list[dict]:
        pass

class JSONExportStrategy(ExportStrategy):
    def export_contacts(self, book: AddressBook, filepath: str) -> None:
        data = []
        for record in book.data.values():
            data.append({
                "name": record.name.value,
                "phones": [p.value for p in record.phones],
                "emails": [e.value for e in record.emails],
                "addresses": [a.value for a in record.addresses],
                "birthday": str(record.birthday) if record.birthday else "",
            })
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def import_contacts(self, book: AddressBook, filepath: str) -> list[dict]:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def export_notes(self, notebook: NoteBook, filepath: str) -> None:
        data = []
        for note in notebook.data.values():
            data.append({
                "title": note.title,
                "content": note.content,
                "tags": [t.value for t in note.tags],
            })
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def import_notes(self, notebook: NoteBook, filepath: str) -> list[dict]:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

class CSVExportStrategy(ExportStrategy):
    def export_contacts(self, book: AddressBook, filepath: str) -> None:
        fieldnames = ["name", "phones", "emails", "addresses", "birthday"]
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for record in book.data.values():
                writer.writerow({
                    "name": record.name.value,
                    "phones": ";".join(p.value for p in record.phones),
                    "emails": ";".join(e.value for e in record.emails),
                    "addresses": ";".join(a.value for a in record.addresses),
                    "birthday": str(record.birthday) if record.birthday else "",
                })

    def import_contacts(self, book: AddressBook, filepath: str) -> list[dict]:
        data = []
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    "name": row.get("name", ""),
                    "phones": row.get("phones", "").split(";") if row.get("phones") else [],
                    "emails": row.get("emails", "").split(";") if row.get("emails") else [],
                    "addresses": row.get("addresses", "").split(";") if row.get("addresses") else [],
                    "birthday": row.get("birthday", ""),
                })
        return data

    def export_notes(self, notebook: NoteBook, filepath: str) -> None:
        raise NotImplementedError("CSV export not supported for notes.")

    def import_notes(self, notebook: NoteBook, filepath: str) -> list[dict]:
        raise NotImplementedError("CSV import not supported for notes.")
