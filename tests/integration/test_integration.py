import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.models import AddressBook, NoteBook
from src.handlers import execute_command
from src.storage import save_data, load_data

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()
        self.notebook = NoteBook()

    def test_full_contact_lifecycle(self):
        # 1. Add contact
        res = execute_command("add", ["John", "0501234567"], self.book, self.notebook)
        self.assertEqual(res, "Contact added.")
        
        # 2. Add second phone
        res = execute_command("add-phone", ["John", "0671112233"], self.book, self.notebook)
        self.assertEqual(res, "Phone added.")
        
        # 3. Add email
        res = execute_command("add-email", ["John", "john@example.com"], self.book, self.notebook)
        self.assertEqual(res, "Email added.")
        
        # 4. Add address
        res = execute_command("add-address", ["John", "Kyiv,", "Main", "St", "1"], self.book, self.notebook)
        self.assertEqual(res, "Address added.")
        
        # 5. Add birthday
        res = execute_command("add-birthday", ["John", "15.08.1995"], self.book, self.notebook)
        self.assertEqual(res, "Birthday added.")
        
        # 6. Verify getters
        self.assertEqual(execute_command("phone", ["John"], self.book, self.notebook), "0501234567; 0671112233")
        self.assertEqual(execute_command("show-email", ["John"], self.book, self.notebook), "john@example.com")
        self.assertEqual(execute_command("show-address", ["John"], self.book, self.notebook), "Kyiv, Main St 1")
        self.assertEqual(execute_command("show-birthday", ["John"], self.book, self.notebook), "15.08.1995")
        
        # 7. Search contacts
        search_res = execute_command("search-contacts", ["Kyiv"], self.book, self.notebook)
        self.assertIn("John", search_res)
        self.assertIn("john@example.com", search_res)
        
        # 8. Change phone
        change_res = execute_command("change", ["John", "0501234567", "0998887766"], self.book, self.notebook)
        self.assertEqual(change_res, "Contact updated.")
        self.assertEqual(execute_command("phone", ["John"], self.book, self.notebook), "0998887766; 0671112233")
        
        # 9. Delete contact
        del_res = execute_command("delete-contact", ["John"], self.book, self.notebook)
        self.assertEqual(del_res, "Contact deleted.")
        self.assertIsNone(self.book.find("John"))

    def test_full_note_lifecycle(self):
        # 1. Add note
        res = execute_command("add-note", ["Shopping", "Milk,", "Bread,", "Cheese"], self.book, self.notebook)
        self.assertIn("Note added.", res)
        
        # 2. Add tags
        res = execute_command("add-tag", ["1", "food", "groceries"], self.book, self.notebook)
        self.assertEqual(res, "Tag added to note.")
        
        # 3. Search note by tag
        res = execute_command("search-by-tag", ["food"], self.book, self.notebook)
        self.assertIn("Shopping", res)
        
        # 4. Edit note
        res = execute_command("edit-note", ["1", "Milk,", "Bread,", "Cheese,", "Apples"], self.book, self.notebook)
        self.assertEqual(res, "Note updated.")
        
        # 5. Search note by content
        res = execute_command("search-notes", ["Apples"], self.book, self.notebook)
        self.assertIn("Shopping", res)
        
        # 6. Sort notes by specific tags
        res_sort = execute_command("sort-notes-by-tags", ["food", "groceries"], self.book, self.notebook)
        self.assertIn("Shopping", res_sort)

        # 7. Delete note
        res = execute_command("delete-note", ["1"], self.book, self.notebook)
        self.assertEqual(res, "Note deleted.")

    def test_persistence_save_and_load(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Add contact and note
            execute_command("add", ["Alice", "0501112233"], self.book, self.notebook)
            execute_command("add-email", ["Alice", "alice@example.com"], self.book, self.notebook)
            execute_command("add-note", ["Meeting", "Discuss project roadmap"], self.book, self.notebook)
            
            # Save to disk
            save_data(self.book, self.notebook, filename=tmp_path)
            
            # Load into fresh instances
            loaded_book, loaded_notebook = load_data(filename=tmp_path)
            
            self.assertIn("Alice", loaded_book.data)
            self.assertEqual(loaded_book.data["Alice"].phones[0].value, "0501112233")
            self.assertEqual(loaded_book.data["Alice"].emails[0].value, "alice@example.com")
            
            self.assertEqual(len(loaded_notebook.data), 1)
            loaded_note = list(loaded_notebook.data.values())[0]
            self.assertEqual(loaded_note.title, "Meeting")
            self.assertEqual(loaded_note.content, "Discuss project roadmap")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if __name__ == "__main__":
    unittest.main()
