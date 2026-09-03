from commands.base import Command, Context
from config import ERRORS, MESSAGES
from models.record import Record
from storage.exporters import FileExporter
from core.events import dispatcher
from formatters import generate_contacts_table, generate_birthdays_table

def get_record(book, name: str) -> Record:
    """Helper function to get a record or raise KeyError."""
    record = book.find(name)
    if record is None:
        raise KeyError
    return record


class AddContactCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if len(args) < 2:
            raise IndexError
        name, phone = args[0], args[1]
        book = context.address_book
        record = book.find(name)
        if record is None:
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
        else:
            record.add_phone(phone)
            
        dispatcher.dispatch("CONTACT_ADDED", {"name": name, "phone": phone})
        return MESSAGES["contact_added"]

class ChangeContactCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if len(args) < 3:
            raise IndexError
        name, old_phone, new_phone = args[0], args[1], args[2]
        record = get_record(context.address_book, name)
        record.edit_phone(old_phone, new_phone)
        return MESSAGES["contact_updated"]

class DeleteContactCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        name = args[0]
        context.address_book.delete(name)
        return MESSAGES["contact_archived"]

class RestoreContactCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        name = args[0]
        record = get_record(context.address_book, name)
        record.is_archived = False
        return MESSAGES["contact_restored"]

class SearchContactsCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        query = " ".join(args)
        results = context.address_book.search(query)
        if not results:
            return MESSAGES["no_matching_contacts"]
        return generate_contacts_table(results)

class ShowPhoneCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        name = args[0]
        record = get_record(context.address_book, name)
        if not record.phones:
            return f"No phone numbers found for {record.name.value}."
        return "; ".join(p.value for p in record.phones)

class AddPhoneCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if len(args) < 2:
            raise IndexError
        name, phone = args[0], args[1]
        record = get_record(context.address_book, name)
        record.add_phone(phone)
        return MESSAGES["phone_added"]

class AddEmailCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if len(args) < 2:
            raise IndexError
        name, email = args[0], args[1]
        record = get_record(context.address_book, name)
        record.add_email(email)
        return MESSAGES["email_added"]

class ShowEmailCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        name = args[0]
        record = get_record(context.address_book, name)
        if not record.emails:
            return ERRORS["no_email"]
        return "; ".join(e.value for e in record.emails)

class AddAddressCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if len(args) < 2:
            raise IndexError
        name = args[0]
        address = " ".join(args[1:])
        record = get_record(context.address_book, name)
        record.add_address(address)
        return MESSAGES["address_added"]

class ShowAddressCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        name = args[0]
        record = get_record(context.address_book, name)
        if not record.addresses:
            return ERRORS["no_address"]
        return "; ".join(a.value for a in record.addresses)

class AddBirthdayCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if len(args) < 2:
            raise IndexError
        name, bday = args[0], args[1]
        record = get_record(context.address_book, name)
        record.add_birthday(bday)
        return MESSAGES["birthday_added"]

class ShowBirthdayCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        name = args[0]
        record = get_record(context.address_book, name)
        if not record.birthday:
            return ERRORS["no_birthday"]
        return f"{record.birthday} (turning {record.get_turning_age()} years old!)"

class BirthdaysCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        days = 7
        if args:
            try:
                days = int(args[0])
                if days <= 0:
                    raise ValueError(ERRORS["invalid_days"])
            except ValueError as e:
                if str(e) == ERRORS["invalid_days"]:
                    raise e
                raise ValueError(ERRORS["invalid_days"])
        upcoming = context.address_book.get_upcoming_birthdays(days)
        if not upcoming:
            return MESSAGES["no_upcoming_birthdays"]
        return generate_birthdays_table(upcoming, days)

class ShowAllCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        book = context.address_book
        if not book.data:
            return MESSAGES["no_contacts"]
        
        show_archived_flag = "--all" in args or "-a" in args
        
        if show_archived_flag:
            active_records = list(book.data.values())
        else:
            active_records = [r for r in book.data.values() if not r.is_archived]
            
        if not active_records:
            return MESSAGES["no_contacts"]
        return generate_contacts_table(active_records)

class ShowArchivedCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        book = context.address_book
        if not book.data:
            return MESSAGES["no_archived_contacts"]
        archived_records = [r for r in book.data.values() if r.is_archived]
        if not archived_records:
            return MESSAGES["no_archived_contacts"]
        return generate_contacts_table(archived_records)

class ExportContactsCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        filepath = args[0]
        exporter = FileExporter()
        return exporter.export_contacts(context.address_book, filepath)

class ImportContactsCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        filepath = args[0]
        exporter = FileExporter()
        return exporter.import_contacts(context.address_book, filepath)

class ClearContactsCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        context.address_book.data.clear()
        return MESSAGES["contacts_cleared"]
