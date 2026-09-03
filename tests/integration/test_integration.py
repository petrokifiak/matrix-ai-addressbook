import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from core.app import Application
from storage.pickle_storage import PickleStorage
from models import AddressBook, NoteBook

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = Application()
        # Override storage to prevent modifying actual user data during tests
        self.temp_storage = tempfile.NamedTemporaryFile(delete=False)
        self.temp_storage.close()
        self.app.storage.file_name = self.temp_storage.name
        self.app.context.address_book = AddressBook()
        self.app.context.notebook = NoteBook()

    def tearDown(self):
        if os.path.exists(self.temp_storage.name):
            os.remove(self.temp_storage.name)

    def test_full_contact_lifecycle(self):
        # 1. Add contact
        res = self.app.execute("add", ["John", "0501234567"])
        self.assertEqual(res, "Contact added.")

        # 2. Add second phone
        res = self.app.execute("add-phone", ["John", "0671112233"])
        self.assertEqual(res, "Phone added.")

        # 3. Add email
        res = self.app.execute("add-email", ["John", "john@example.com"])
        self.assertEqual(res, "Email added.")

        # 4. Add address
        res = self.app.execute("add-address", ["John", "Kyiv,", "Main", "St", "1"])
        self.assertEqual(res, "Address added.")

        # 5. Add birthday
        res = self.app.execute("add-birthday", ["John", "15.08.1995"])
        self.assertEqual(res, "Birthday added.")

        # 6. Verify getters
        self.assertEqual(self.app.execute("phone", ["John"]), "0501234567; 0671112233")
        self.assertEqual(self.app.execute("show-email", ["John"]), "john@example.com")
        self.assertEqual(self.app.execute("show-address", ["John"]), "Kyiv, Main St 1")
        turning = self.app.context.address_book.find("John").get_turning_age()
        self.assertEqual(self.app.execute("show-birthday", ["John"]), f"15.08.1995 (turning {turning} years old!)")
        
        # 7. Search contacts
        search_res = self.app.execute("search-contacts", ["Kyiv"])
        self.assertNotEqual(search_res, "No matching contacts found.")

        # 8. Change phone
        change_res = self.app.execute("change", ["John", "0501234567", "0998887766"])
        self.assertEqual(change_res, "Contact updated.")
        self.assertEqual(self.app.execute("phone", ["John"]), "0998887766; 0671112233")

        # 9. Delete contact (Archive)
        del_res = self.app.execute("delete-contact", ["John"])
        self.assertEqual(del_res, "Contact archived.")
        self.assertTrue(self.app.context.address_book.find("John").is_archived)

        # 10. Restore contact
        restore_res = self.app.execute("restore-contact", ["John"])
        self.assertEqual(restore_res, "Contact restored.")
        self.assertFalse(self.app.context.address_book.find("John").is_archived)

    def test_full_note_lifecycle(self):
        # 1. Add note
        res = self.app.execute("add-note", ["Shopping", "Milk,", "Bread,", "Cheese"])
        self.assertIn("Note added.", res)

        # 2. Add tags
        res = self.app.execute("add-tag", ["1", "food", "groceries"])
        self.assertEqual(res, "Tag added to note.")

        # 3. Search note by tag
        res = self.app.execute("search-by-tag", ["food"])
        self.assertNotEqual(res, "No notes found.")

        # 4. Edit note
        res = self.app.execute("edit-note", ["1", "Milk,", "Bread,", "Cheese,", "Apples"])
        self.assertEqual(res, "Note updated.")

        # 5. Search note by content
        res = self.app.execute("search-notes", ["Apples"])
        self.assertNotEqual(res, "No matching notes found.")

        # 6. Sort notes by specific tags
        res_sort = self.app.execute("sort-notes-by-tags", ["food", "groceries"])
        self.assertNotEqual(res_sort, "No matching notes found.")

        # 7. Delete note
        res = self.app.execute("delete-note", ["1"])
        self.assertEqual(res, "Note deleted.")

    def test_persistence_save_and_load(self):
        # Add contact and note
        self.app.execute("add", ["Alice", "0501112233"])
        self.app.execute("add-email", ["Alice", "alice@example.com"])
        self.app.execute("add-note", ["Meeting", "Discuss project roadmap"])

        # Save to disk
        self.app.save()

        # Load into fresh instances
        storage = PickleStorage()
        storage.file_name = self.temp_storage.name
        loaded_book, loaded_notebook = storage.load()

        self.assertIn("Alice", loaded_book.data)
        self.assertEqual(loaded_book.data["Alice"].phones[0].value, "0501112233")
        self.assertEqual(loaded_book.data["Alice"].emails[0].value, "alice@example.com")

        self.assertEqual(len(loaded_notebook.data), 1)
        loaded_note = list(loaded_notebook.data.values())[0]
        self.assertEqual(loaded_note.title, "Meeting")
        self.assertEqual(loaded_note.content, "Discuss project roadmap")

    def test_export_import_contacts(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_json:
            json_path = tmp_json.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_csv:
            csv_path = tmp_csv.name

        try:
            # 1. Add some data
            self.app.execute("add", ["Bob", "0509998877"])
            self.app.execute("add-email", ["Bob", "bob@example.com"])

            # 2. Export to JSON
            res = self.app.execute("export-contacts", [json_path])
            self.assertEqual(res, "Contacts exported successfully.")

            # 3. Create a fresh book to test import
            self.app.execute("clear-contacts", [])
            res = self.app.execute("import-contacts", [json_path])
            self.assertEqual(res, "Contacts imported successfully.")
            self.assertIn("Bob", self.app.context.address_book.data)
            self.assertEqual(self.app.context.address_book.data["Bob"].phones[0].value, "0509998877")
            self.assertEqual(self.app.context.address_book.data["Bob"].emails[0].value, "bob@example.com")

            # 4. Export to CSV (from original book)
            res = self.app.execute("export-contacts", [csv_path])
            self.assertEqual(res, "Contacts exported successfully.")

            # 5. Import from CSV to another fresh book
            self.app.execute("clear-contacts", [])
            res = self.app.execute("import-contacts", [csv_path])
            self.assertEqual(res, "Contacts imported successfully.")
            self.assertIn("Bob", self.app.context.address_book.data)
            self.assertEqual(self.app.context.address_book.data["Bob"].phones[0].value, "0509998877")
            self.assertEqual(self.app.context.address_book.data["Bob"].emails[0].value, "bob@example.com")
        finally:
            if os.path.exists(json_path):
                os.remove(json_path)
            if os.path.exists(csv_path):
                os.remove(csv_path)


    def test_export_import_notes(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp_json:
            json_path = tmp_json.name

        try:
            # 1. Add some notes
            self.app.execute("add-note", ["Idea", "Build a robot"])
            self.app.execute("add-tag", ["Idea", "tech"])

            # 2. Export notes to JSON
            res = self.app.execute("export-notes", [json_path])
            self.assertEqual(res, "Notes exported successfully.")

            # 3. Create a fresh notebook to test import
            self.app.execute("clear-notes", [])
            res = self.app.execute("import-notes", [json_path])
            self.assertEqual(res, "Notes imported successfully.")
            self.assertEqual(len(self.app.context.notebook.data), 1)
            
            imported_note = list(self.app.context.notebook.data.values())[0]
            self.assertEqual(imported_note.title, "Idea")
            self.assertEqual(imported_note.content, "Build a robot")
            self.assertEqual(imported_note.tags[0].value, "tech")

        finally:
            if os.path.exists(json_path):
                os.remove(json_path)


    def test_clear_commands(self):
        # 1. Add data
        self.app.execute("add", ["TestUser", "0501112233"])
        self.app.execute("add-note", ["TestNote", "Content"])

        self.assertEqual(len(self.app.context.address_book.data), 1)
        self.assertEqual(len(self.app.context.notebook.data), 1)

        # 2. Clear contacts
        res = self.app.execute("clear-contacts", [])
        self.assertEqual(res, "All contacts have been successfully cleared.")
        self.assertEqual(len(self.app.context.address_book.data), 0)
        self.assertEqual(len(self.app.context.notebook.data), 1)

        # 3. Add contact back, clear notes
        self.app.execute("add", ["TestUser", "0501112233"])
        res = self.app.execute("clear-notes", [])
        self.assertEqual(res, "All notes have been successfully cleared.")
        self.assertEqual(len(self.app.context.address_book.data), 1)
        self.assertEqual(len(self.app.context.notebook.data), 0)

        # 4. Add note back, clear data
        self.app.execute("add-note", ["TestNote", "Content"])
        res = self.app.execute("clear-data", [])
        self.assertEqual(res, "All data has been successfully cleared.")
        self.assertEqual(len(self.app.context.address_book.data), 0)
        self.assertEqual(len(self.app.context.notebook.data), 0)

if __name__ == "__main__":
    unittest.main()
