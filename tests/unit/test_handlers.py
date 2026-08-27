import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.models import NoteBook
from src.handlers import add_note, edit_note, delete_note, search_notes, show_notes
from src.config import MESSAGES, ERRORS

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

if __name__ == "__main__":
    unittest.main()
