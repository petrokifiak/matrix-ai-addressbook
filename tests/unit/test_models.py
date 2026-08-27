import unittest
from src.models import Note, NoteBook, Tag

class TestNote(unittest.TestCase):
    def test_note_creation(self):
        note = Note(1, "Test Title", "Test Content")
        self.assertEqual(note.id, 1)
        self.assertEqual(note.title, "Test Title")
        self.assertEqual(note.content, "Test Content")
        self.assertEqual(note.tags, [])

    def test_note_with_tags(self):
        note = Note(1, "Title", "Content", ["work", "important"])
        self.assertEqual(len(note.tags), 2)
        self.assertEqual(note.tags[0].value, "work")
        self.assertEqual(note.tags[1].value, "important")

    def test_add_tag(self):
        note = Note(1, "Title", "Content")
        note.add_tag("urgent")
        self.assertEqual(len(note.tags), 1)
        self.assertEqual(note.tags[0].value, "urgent")
        
    def test_edit_content(self):
        note = Note(1, "Title", "Old Content")
        note.edit_content("New Content")
        self.assertEqual(note.content, "New Content")

    def test_edit_content_empty_raises_error(self):
        note = Note(1, "Title", "Content")
        with self.assertRaises(ValueError):
            note.edit_content("")
        with self.assertRaises(ValueError):
            note.edit_content("   ")

class TestNoteBook(unittest.TestCase):
    def setUp(self):
        self.notebook = NoteBook()

    def test_add_note(self):
        note = self.notebook.add_note("My Title", "My Content")
        self.assertEqual(note.title, "My Title")
        self.assertEqual(note.content, "My Content")
        self.assertEqual(len(self.notebook.data), 1)
        self.assertIn(note.id, self.notebook.data)

    def test_add_note_empty_raises_error(self):
        with self.assertRaises(ValueError):
            self.notebook.add_note("", "Content")
        with self.assertRaises(ValueError):
            self.notebook.add_note("Title", "")

    def test_find_note_by_id(self):
        note = self.notebook.add_note("Title", "Content")
        found = self.notebook.find_note(note.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, note.id)

    def test_find_note_by_title(self):
        note = self.notebook.add_note("Unique Title", "Content")
        found = self.notebook.find_note("Unique Title")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, note.id)
        
        found_lower = self.notebook.find_note("unique title")
        self.assertIsNotNone(found_lower)
        self.assertEqual(found_lower.id, note.id)

    def test_find_note_not_found(self):
        found = self.notebook.find_note("Nonexistent")
        self.assertIsNone(found)

    def test_edit_note(self):
        note = self.notebook.add_note("Title", "Old Content")
        success = self.notebook.edit_note(note.id, "New Content")
        self.assertTrue(success)
        self.assertEqual(self.notebook.data[note.id].content, "New Content")

    def test_edit_note_not_found(self):
        success = self.notebook.edit_note(999, "New Content")
        self.assertFalse(success)

    def test_delete_note_success(self):
        note = self.notebook.add_note("ToDelete", "Content")
        success = self.notebook.delete_note(note.id)
        self.assertTrue(success)
        self.assertNotIn(note.id, self.notebook.data)

    def test_delete_note_not_found(self):
        success = self.notebook.delete_note(999)
        self.assertFalse(success)

    def test_search_notes(self):
        self.notebook.add_note("Apple", "Red fruit")
        self.notebook.add_note("Banana", "Yellow fruit")
        self.notebook.add_note("Car", "Fast vehicle")
        
        # Search by content
        results = self.notebook.search_notes("fruit")
        self.assertEqual(len(results), 2)
        
        # Search by title
        results = self.notebook.search_notes("apple")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Apple")
        
        # No match
        results = self.notebook.search_notes("grape")
        self.assertEqual(len(results), 0)

if __name__ == "__main__":
    unittest.main()
