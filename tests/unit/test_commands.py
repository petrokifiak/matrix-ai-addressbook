import os
import sys
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from config import ERRORS, MESSAGES
from commands.base import Context
from models import AddressBook, NoteBook, Record
from commands.contact_commands import (
    AddContactCommand, ChangeContactCommand, DeleteContactCommand,
    RestoreContactCommand, SearchContactsCommand, ShowPhoneCommand,
    AddPhoneCommand, AddEmailCommand, ShowEmailCommand, AddAddressCommand,
    ShowAddressCommand, AddBirthdayCommand, ShowBirthdayCommand,
    BirthdaysCommand, ShowAllCommand, ShowArchivedCommand
)
from commands.note_commands import (
    AddNoteCommand, ShowNotesCommand, SearchNotesCommand, EditNoteCommand,
    DeleteNoteCommand, AddTagCommand, SearchByTagCommand, SortNotesCommand
)

class TestContactCommands(unittest.TestCase):
    def setUp(self):
        self.context = Context(address_book=AddressBook(), notebook=NoteBook())

    def test_add_contact_success(self):
        args = ["John", "0501234567"]
        result = AddContactCommand().execute(args, self.context)
        self.assertEqual(result, MESSAGES["contact_added"])
        self.assertIn("John", self.context.address_book.data)
        self.assertEqual(self.context.address_book.data["John"].phones[0].value, "0501234567")

    def test_add_contact_missing_args(self):
        with self.assertRaises(IndexError):
            AddContactCommand().execute(["John"], self.context)

    def test_add_contact_invalid_phone(self):
        with self.assertRaises(ValueError):
            AddContactCommand().execute(["John", "12345"], self.context)

    def test_change_contact_success(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        args = ["John", "0501234567", "0671112233"]
        result = ChangeContactCommand().execute(args, self.context)
        self.assertEqual(result, MESSAGES["contact_updated"])
        self.assertEqual(self.context.address_book.data["John"].phones[0].value, "0671112233")

    def test_change_contact_not_found(self):
        with self.assertRaises(KeyError):
            ChangeContactCommand().execute(["Ghost", "0501234567", "0671112233"], self.context)

    def test_delete_contact_success(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        result = DeleteContactCommand().execute(["John"], self.context)
        self.assertEqual(result, MESSAGES["contact_archived"])
        self.assertTrue(self.context.address_book.find("John").is_archived)

    def test_search_contacts(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        AddContactCommand().execute(["Alice", "0679876543"], self.context)
        
        result_table = SearchContactsCommand().execute(["John"], self.context)
        # Should not be a string returning no matching contacts
        self.assertNotEqual(result_table, MESSAGES["no_matching_contacts"])

        result_not_found = SearchContactsCommand().execute(["Nobody"], self.context)
        self.assertEqual(result_not_found, MESSAGES["no_matching_contacts"])

    def test_show_phone(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        result = ShowPhoneCommand().execute(["John"], self.context)
        self.assertEqual(result, "0501234567")

    def test_add_phone(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        result = AddPhoneCommand().execute(["John", "0671112233"], self.context)
        self.assertEqual(result, MESSAGES["phone_added"])
        self.assertEqual(len(self.context.address_book.data["John"].phones), 2)

    def test_add_and_show_email(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        res_add = AddEmailCommand().execute(["John", "john@example.com"], self.context)
        self.assertEqual(res_add, MESSAGES["email_added"])

        res_show = ShowEmailCommand().execute(["John"], self.context)
        self.assertEqual(res_show, "john@example.com")

    def test_add_and_show_address(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        res_add = AddAddressCommand().execute(["John", "Kyiv,", "Main", "St", "10"], self.context)
        self.assertEqual(res_add, MESSAGES["address_added"])

        res_show = ShowAddressCommand().execute(["John"], self.context)
        self.assertEqual(res_show, "Kyiv, Main St 10")

    def test_add_and_show_birthday(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        res_add = AddBirthdayCommand().execute(["John", "15.08.1995"], self.context)
        self.assertEqual(res_add, MESSAGES["birthday_added"])

        res_show = ShowBirthdayCommand().execute(["John"], self.context)
        turning = self.context.address_book.find("John").get_turning_age()
        self.assertEqual(res_show, f"15.08.1995 (turning {turning} years old!)")

    def test_birthdays_handler(self):
        AddContactCommand().execute(["John", "0501234567"], self.context)
        target_date = date.today() + timedelta(days=2)
        bday_str = f"{target_date.day:02d}.{target_date.month:02d}.1990"
        AddBirthdayCommand().execute(["John", bday_str], self.context)

        result = BirthdaysCommand().execute(["7"], self.context)
        self.assertNotEqual(result, MESSAGES["no_upcoming_birthdays"])

    def test_show_all(self):
        self.assertEqual(ShowAllCommand().execute([], self.context), MESSAGES["no_contacts"])
        AddContactCommand().execute(["John", "0501234567"], self.context)
        res = ShowAllCommand().execute([], self.context)
        self.assertNotEqual(res, MESSAGES["no_contacts"])


class TestNoteCommands(unittest.TestCase):
    def setUp(self):
        self.context = Context(address_book=AddressBook(), notebook=NoteBook())

    def test_add_note_success(self):
        args = ["MyTitle", "This", "is", "the", "content"]
        result = AddNoteCommand().execute(args, self.context)
        
        self.assertEqual(len(self.context.notebook.data), 1)
        note = list(self.context.notebook.data.values())[0]
        self.assertEqual(note.title, "MyTitle")
        self.assertEqual(note.content, "This is the content")
        self.assertEqual(result, f"{MESSAGES['note_added']} ID: {note.id}")

    def test_add_note_missing_content(self):
        with self.assertRaises(IndexError):
            AddNoteCommand().execute(["MyTitle"], self.context)
        self.assertEqual(len(self.context.notebook.data), 0)

    def test_edit_note_success(self):
        note = self.context.notebook.add_note("OriginalTitle", "Original Content")
        args = [str(note.id), "New", "Content", "Here"]
        result = EditNoteCommand().execute(args, self.context)
        
        self.assertEqual(self.context.notebook.data[note.id].content, "New Content Here")
        self.assertEqual(result, MESSAGES["note_updated"])

    def test_delete_note_success(self):
        note = self.context.notebook.add_note("ToDelete", "Content")
        args = [str(note.id)]
        result = DeleteNoteCommand().execute(args, self.context)
        
        self.assertNotIn(note.id, self.context.notebook.data)
        self.assertEqual(result, MESSAGES["note_deleted"])

    def test_search_notes(self):
        self.context.notebook.add_note("Apple", "Red fruit")
        self.context.notebook.add_note("Banana", "Yellow fruit")
        
        result = SearchNotesCommand().execute(["fruit"], self.context)
        self.assertNotEqual(result, MESSAGES["no_matching_notes"])

    def test_show_notes_empty(self):
        result = ShowNotesCommand().execute([], self.context)
        self.assertEqual(result, MESSAGES.get("no_notes", "No notes found."))

    def test_add_tag_success(self):
        note = self.context.notebook.add_note("Apple", "Red")
        args = [str(note.id), "fruit", "sweet"]
        result = AddTagCommand().execute(args, self.context)
        self.assertEqual(result, MESSAGES.get("tag_added", "Tags added."))
        self.assertEqual(len(note.tags), 2)
        self.assertEqual(note.tags[0].value, "fruit")

    def test_search_by_tag_success(self):
        self.context.notebook.add_note("Apple", "Red", ["fruit"])
        result = SearchByTagCommand().execute(["fruit"], self.context)
        self.assertNotEqual(result, MESSAGES.get("no_matching_notes", "No notes found."))

if __name__ == "__main__":
    unittest.main()
