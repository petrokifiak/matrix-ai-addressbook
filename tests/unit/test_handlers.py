import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.models import AddressBook, Record, NoteBook
from src.handlers import (
    add_contact, change_contact, delete_contact, search_contacts,
    show_phone, add_phone, add_email, show_email,
    add_address, show_address, add_birthday, show_birthday,
    birthdays, show_all,
    add_note, edit_note, delete_note, search_notes, show_notes,
    add_tag, search_by_tag, sort_notes, execute_command
)
from src.config import MESSAGES, ERRORS

class TestContactHandlers(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()

    def test_add_contact_success(self):
        args = ["John", "0501234567"]
        result = add_contact(args, self.book)
        self.assertEqual(result, MESSAGES["contact_added"])
        self.assertIn("John", self.book.data)
        self.assertEqual(self.book.data["John"].phones[0].value, "0501234567")

    def test_add_contact_missing_args(self):
        args = ["John"]
        result = add_contact(args, self.book)
        self.assertEqual(result, ERRORS["missing_args"])

    def test_add_contact_invalid_phone(self):
        args = ["John", "12345"]
        result = add_contact(args, self.book)
        self.assertEqual(result, ERRORS["invalid_phone"])

    def test_change_contact_success(self):
        add_contact(["John", "0501234567"], self.book)
        args = ["John", "0501234567", "0671112233"]
        result = change_contact(args, self.book)
        self.assertEqual(result, MESSAGES["contact_updated"])
        self.assertEqual(self.book.data["John"].phones[0].value, "0671112233")

    def test_change_contact_not_found(self):
        args = ["Ghost", "0501234567", "0671112233"]
        result = change_contact(args, self.book)
        self.assertEqual(result, ERRORS["contact_not_found"])

    def test_delete_contact_success(self):
        add_contact(["John", "0501234567"], self.book)
        result = delete_contact(["John"], self.book)
        self.assertEqual(result, MESSAGES["contact_deleted"])
        self.assertNotIn("John", self.book.data)

    def test_delete_contact_not_found(self):
        result = delete_contact(["Ghost"], self.book)
        self.assertEqual(result, ERRORS["contact_not_found"])

    def test_search_contacts(self):
        add_contact(["John", "0501234567"], self.book)
        add_contact(["Alice", "0679876543"], self.book)
        
        result = search_contacts(["John"], self.book)
        self.assertIn("John", result)
        self.assertNotIn("Alice", result)

        result_not_found = search_contacts(["Nobody"], self.book)
        self.assertEqual(result_not_found, MESSAGES["no_matching_contacts"])

    def test_show_phone(self):
        add_contact(["John", "0501234567"], self.book)
        result = show_phone(["John"], self.book)
        self.assertEqual(result, "0501234567")

    def test_add_phone(self):
        add_contact(["John", "0501234567"], self.book)
        result = add_phone(["John", "0671112233"], self.book)
        self.assertEqual(result, MESSAGES["phone_added"])
        self.assertEqual(len(self.book.data["John"].phones), 2)

    def test_add_and_show_email(self):
        add_contact(["John", "0501234567"], self.book)
        res_add = add_email(["John", "john@example.com"], self.book)
        self.assertEqual(res_add, MESSAGES["email_added"])

        res_show = show_email(["John"], self.book)
        self.assertEqual(res_show, "john@example.com")

    def test_add_and_show_address(self):
        add_contact(["John", "0501234567"], self.book)
        res_add = add_address(["John", "Kyiv,", "Main", "St", "10"], self.book)
        self.assertEqual(res_add, MESSAGES["address_added"])

        res_show = show_address(["John"], self.book)
        self.assertEqual(res_show, "Kyiv, Main St 10")

    def test_add_and_show_birthday(self):
        add_contact(["John", "0501234567"], self.book)
        res_add = add_birthday(["John", "15.08.1995"], self.book)
        self.assertEqual(res_add, MESSAGES["birthday_added"])

        res_show = show_birthday(["John"], self.book)
        turning = self.book.find("John").get_turning_age()
        self.assertEqual(res_show, f"15.08.1995 (turning {turning} years old!)")

    def test_birthdays_handler(self):
        add_contact(["John", "0501234567"], self.book)
        from datetime import date, timedelta
        target_date = date.today() + timedelta(days=2)
        bday_str = f"{target_date.day:02d}.{target_date.month:02d}.1990"
        add_birthday(["John", bday_str], self.book)

        result = birthdays(["7"], self.book)
        self.assertIn("John", result)
        self.assertIn(f"turning {target_date.year - 1990} years old!", result)

    def test_show_all(self):
        self.assertEqual(show_all(self.book), MESSAGES["no_contacts"])
        add_contact(["John", "0501234567"], self.book)
        res = show_all(self.book)
        self.assertIn("John", res)

class TestNoteHandlers(unittest.TestCase):
    def setUp(self):
        self.notebook = NoteBook()

    def test_add_note_success(self):
        args = ["MyTitle", "This", "is", "the", "content"]
        result = add_note(args, self.notebook)
        
        self.assertEqual(len(self.notebook.data), 1)
        note = list(self.notebook.data.values())[0]
        self.assertEqual(note.title, "MyTitle")
        self.assertEqual(note.content, "This is the content")
        self.assertEqual(result, f"{MESSAGES['note_added']} ID: {note.id}")

    def test_add_note_missing_content(self):
        # Should raise IndexError which decorator catches and returns missing_args
        args = ["MyTitle"]
        result = add_note(args, self.notebook)
        self.assertEqual(result, ERRORS["missing_args"])
        self.assertEqual(len(self.notebook.data), 0)

    def test_edit_note_success(self):
        note = self.notebook.add_note("OriginalTitle", "Original Content")
        args = [str(note.id), "New", "Content", "Here"]
        result = edit_note(args, self.notebook)
        
        self.assertEqual(self.notebook.data[note.id].content, "New Content Here")
        self.assertEqual(result, MESSAGES["note_updated"])

    def test_edit_note_by_title_success(self):
        note = self.notebook.add_note("OriginalTitle", "Original Content")
        args = ["OriginalTitle", "New", "Content", "By", "Title"]
        result = edit_note(args, self.notebook)
        
        self.assertEqual(self.notebook.data[note.id].content, "New Content By Title")
        self.assertEqual(result, MESSAGES["note_updated"])

    def test_edit_note_not_found(self):
        # ValueError is caught by decorator, and it checks if message matches ERRORS.
        args = ["999", "New", "Content"]
        result = edit_note(args, self.notebook)
        self.assertEqual(result, ERRORS["note_not_found"])

    def test_edit_note_missing_content(self):
        note = self.notebook.add_note("Title", "Content")
        args = [str(note.id)]
        result = edit_note(args, self.notebook)
        self.assertEqual(result, ERRORS["missing_args"])

    def test_delete_note_success(self):
        note = self.notebook.add_note("ToDelete", "Content")
        args = [str(note.id)]
        result = delete_note(args, self.notebook)
        
        self.assertNotIn(note.id, self.notebook.data)
        self.assertEqual(result, MESSAGES["note_deleted"])

    def test_delete_note_not_found(self):
        args = ["999"]
        result = delete_note(args, self.notebook)
        self.assertEqual(result, ERRORS["note_not_found"])

    def test_search_notes_success(self):
        self.notebook.add_note("Apple", "Red fruit")
        self.notebook.add_note("Banana", "Yellow fruit")
        
        args = ["fruit"]
        result = search_notes(args, self.notebook)
        self.assertIn("Apple", result)
        self.assertIn("Banana", result)

    def test_search_notes_not_found(self):
        self.notebook.add_note("Apple", "Red fruit")
        args = ["grape"]
        result = search_notes(args, self.notebook)
        self.assertEqual(result, MESSAGES["no_matching_notes"])

    def test_show_notes_success(self):
        self.notebook.add_note("Apple", "Red fruit")
        self.notebook.add_note("Banana", "Yellow fruit")
        result = show_notes(self.notebook)
        self.assertIn("Apple", result)
        self.assertIn("Banana", result)

    def test_show_notes_empty(self):
        result = show_notes(self.notebook)
        self.assertEqual(result, MESSAGES["no_notes"])

    def test_add_tag_success(self):
        note = self.notebook.add_note("Apple", "Red")
        args = [str(note.id), "fruit", "sweet"]
        result = add_tag(args, self.notebook)
        self.assertEqual(result, MESSAGES.get("tag_added", "Tags added."))
        self.assertEqual(len(note.tags), 2)
        self.assertEqual(note.tags[0].value, "fruit")

    def test_search_by_tag_success(self):
        self.notebook.add_note("Apple", "Red", ["fruit"])
        args = ["fruit"]
        result = search_by_tag(args, self.notebook)
        self.assertIn("Apple", result)

    def test_sort_notes_success(self):
        self.notebook.add_note("Apple", "Red", ["fruit", "red"])
        self.notebook.add_note("Banana", "Yellow", ["fruit"])
        result = sort_notes([], self.notebook)
        self.assertTrue(result.index("Apple") < result.index("Banana"))

    def test_sort_notes_by_specific_tags(self):
        self.notebook.add_note("Report", "Important report", ["work", "urgent"])
        self.notebook.add_note("Letter", "A letter to friend", ["work"])
        self.notebook.add_note("Groceries", "Milk and bread", ["home"])
        
        result = sort_notes(["work", "urgent"], self.notebook)
        self.assertIn("Report", result)
        self.assertIn("Letter", result)
        self.assertNotIn("Groceries", result)
        self.assertTrue(result.index("Report") < result.index("Letter"))

class TestExecuteCommand(unittest.TestCase):
    def test_fuzzy_matching_single(self):
        from src.handlers import execute_command
        from src.models import AddressBook, NoteBook
        book = AddressBook()
        notebook = NoteBook()
        result = execute_command("add-noe", [], book, notebook)
        self.assertIn("add-note", result)
        self.assertIn("Did you mean", result)

    def test_fuzzy_matching_multiple(self):
        from src.handlers import execute_command
        from src.models import AddressBook, NoteBook
        book = AddressBook()
        notebook = NoteBook()
        # "add-" should match add, add-note, add-tag, etc.
        result = execute_command("add-", [], book, notebook)
        self.assertIn("Did you mean one of these:", result)
        self.assertIn("add-note", result)
        self.assertIn("add", result)

    def test_fuzzy_matching_none(self):
        from src.handlers import execute_command
        from src.models import AddressBook, NoteBook
        from src.config import ERRORS
        book = AddressBook()
        notebook = NoteBook()
        result = execute_command("asdfghjkl", [], book, notebook)
        self.assertEqual(result, ERRORS["invalid_command"])

    def test_help_general(self):
        from src.handlers import execute_command
        from src.models import AddressBook, NoteBook
        book = AddressBook()
        notebook = NoteBook()
        result = execute_command("help", [], book, notebook)
        self.assertIn("Available categories:", result)
        self.assertIn("- Contacts", result)
        self.assertIn("- Notes", result)

    def test_help_specific_command(self):
        from src.handlers import execute_command
        from src.models import AddressBook, NoteBook
        book = AddressBook()
        notebook = NoteBook()
        result = execute_command("help", ["add-note"], book, notebook)
        self.assertIn("Command:", result)
        self.assertIn("add-note", result)
        self.assertIn("Creates a text note.", result)
        self.assertIn("Syntax:", result)

    def test_help_not_found(self):
        from src.handlers import execute_command
        from src.models import AddressBook, NoteBook
        book = AddressBook()
        notebook = NoteBook()
        result = execute_command("help", ["some-fake-cmd"], book, notebook)
        self.assertIn("not found", result)

if __name__ == "__main__":
    unittest.main()
