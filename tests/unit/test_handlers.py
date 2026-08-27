import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.models import NoteBook
from src.handlers import add_note, edit_note, delete_note, search_notes, show_notes, add_tag, search_by_tag, sort_notes
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
        result = sort_notes(self.notebook)
        self.assertTrue(result.index("Apple") < result.index("Banana"))

if __name__ == "__main__":
    unittest.main()

class TestExecuteCommand(unittest.TestCase):
    def test_fuzzy_matching_single(self):
        from src.handlers import execute_command
        from src.models import AddressBook, NoteBook
        book = AddressBook()
        notebook = NoteBook()
        result = execute_command("add-noe", [], book, notebook)
        self.assertIn("Did you mean: add-note", result)

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
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from src.models import NoteBook
from src.handlers import add_note, edit_note, delete_note, search_notes, show_notes, add_tag, search_by_tag, sort_notes
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
        result = sort_notes(self.notebook)
        self.assertTrue(result.index("Apple") < result.index("Banana"))

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

if __name__ == "__main__":
    unittest.main()
