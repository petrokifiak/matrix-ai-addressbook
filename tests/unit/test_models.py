import unittest
from datetime import date, timedelta

from src.constants import DATE_FORMAT
from src.models import (
    Address,
    AddressBook,
    Birthday,
    Email,
    Field,
    Name,
    Note,
    NoteBook,
    Phone,
    Record,
    Tag,
)


class TestContactFields(unittest.TestCase):
    def test_name_success(self):
        name = Name("John Doe")
        self.assertEqual(name.value, "John Doe")
        self.assertEqual(str(name), "John Doe")

    def test_name_empty_raises_error(self):
        with self.assertRaises(ValueError):
            Name("")
        with self.assertRaises(ValueError):
            Name("   ")

    def test_phone_valid(self):
        phone = Phone("0501234567")
        self.assertEqual(phone.value, "0501234567")

    def test_phone_invalid_raises_error(self):
        with self.assertRaises(ValueError):
            Phone("12345")
        with self.assertRaises(ValueError):
            Phone("050123456789")
        with self.assertRaises(ValueError):
            Phone("050123456a")

    def test_email_valid(self):
        email = Email("user@example.com")
        self.assertEqual(email.value, "user@example.com")

    def test_email_invalid_raises_error(self):
        with self.assertRaises(ValueError):
            Email("invalid-email")
        with self.assertRaises(ValueError):
            Email("user@")
        with self.assertRaises(ValueError):
            Email("@example.com")

    def test_address_valid(self):
        address = Address("Kyiv, Main St. 1")
        self.assertEqual(address.value, "Kyiv, Main St. 1")

    def test_address_empty_raises_error(self):
        with self.assertRaises(ValueError):
            Address("")

    def test_birthday_valid(self):
        bday = Birthday("15.08.1995")
        self.assertEqual(str(bday), "15.08.1995")
        self.assertEqual(bday.value, date(1995, 8, 15))

    def test_birthday_invalid_raises_error(self):
        with self.assertRaises(ValueError):
            Birthday("1995-08-15")
        with self.assertRaises(ValueError):
            Birthday("32.01.2000")

class TestRecord(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")

    def test_add_phone(self):
        self.record.add_phone("0501234567")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "0501234567")

    def test_add_duplicate_phone(self):
        self.record.add_phone("0501234567")
        self.record.add_phone("0501234567")
        self.assertEqual(len(self.record.phones), 1)

    def test_find_phone(self):
        self.record.add_phone("0501234567")
        p = self.record.find_phone("0501234567")
        self.assertIsNotNone(p)
        self.assertEqual(p.value, "0501234567")
        self.assertIsNone(self.record.find_phone("0671112233"))

    def test_edit_phone(self):
        self.record.add_phone("0501234567")
        self.record.edit_phone("0501234567", "0671112233")
        self.assertEqual(self.record.phones[0].value, "0671112233")

    def test_edit_phone_not_found(self):
        with self.assertRaises(ValueError):
            self.record.edit_phone("0501234567", "0671112233")

    def test_remove_phone(self):
        self.record.add_phone("0501234567")
        self.record.remove_phone("0501234567")
        self.assertEqual(len(self.record.phones), 0)

    def test_remove_phone_not_found(self):
        with self.assertRaises(ValueError):
            self.record.remove_phone("0501234567")

    def test_add_email(self):
        self.record.add_email("john@example.com")
        self.assertEqual(len(self.record.emails), 1)
        self.assertEqual(self.record.emails[0].value, "john@example.com")

    def test_add_address(self):
        self.record.add_address("Kyiv")
        self.assertEqual(len(self.record.addresses), 1)
        self.assertEqual(self.record.addresses[0].value, "Kyiv")

    def test_add_birthday(self):
        self.record.add_birthday("15.08.1995")
        self.assertIsNotNone(self.record.birthday)
        self.assertEqual(str(self.record.birthday), "15.08.1995")


class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.book = AddressBook()

    def test_add_and_find_record(self):
        rec = Record("Alice")
        rec.add_phone("0501234567")
        self.book.add_record(rec)
        found = self.book.find("Alice")
        self.assertIsNotNone(found)
        self.assertEqual(found.name.value, "Alice")

    def test_delete_record(self):
        rec = Record("Alice")
        self.book.add_record(rec)
        self.book.delete("Alice")
        self.assertIsNone(self.book.find("Alice"))

    def test_delete_record_not_found_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.book.delete("Nonexistent")

    def test_search_contacts(self):
        rec1 = Record("Alice")
        rec1.add_phone("0501111111")
        rec1.add_email("alice@mail.com")
        rec1.add_address("Kyiv")

        rec2 = Record("Bob")
        rec2.add_phone("0672222222")
        rec2.add_email("bob@mail.com")
        rec2.add_address("Lviv")

        self.book.add_record(rec1)
        self.book.add_record(rec2)

        # By name
        res = self.book.search("ali")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name.value, "Alice")

        # By phone
        res = self.book.search("222222")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name.value, "Bob")

        # By email
        res = self.book.search("mail.com")
        self.assertEqual(len(res), 2)

        # By address
        res = self.book.search("lviv")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].name.value, "Bob")

    def test_get_upcoming_birthdays(self):
        today = date.today()
        # Contact 1: Birthday in 3 days
        target_date_1 = today + timedelta(days=3)
        bday_str_1 = f"{target_date_1.day:02d}.{target_date_1.month:02d}.1990"
        rec1 = Record("Alice")
        rec1.add_birthday(bday_str_1)
        self.book.add_record(rec1)

        # Contact 2: Birthday in 20 days (outside 7-day window)
        target_date_2 = today + timedelta(days=20)
        bday_str_2 = f"{target_date_2.day:02d}.{target_date_2.month:02d}.1990"
        rec2 = Record("Bob")
        rec2.add_birthday(bday_str_2)
        self.book.add_record(rec2)

        upcoming = self.book.get_upcoming_birthdays(days=7)
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0]["name"], "Alice")
        self.assertEqual(upcoming[0]["age"], target_date_1.year - 1990)


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

    def test_search_by_tag(self):
        note1 = self.notebook.add_note("Apple", "Red fruit", ["fruit", "red"])
        note2 = self.notebook.add_note("Banana", "Yellow fruit", ["fruit"])
        note3 = self.notebook.add_note("Car", "Fast vehicle", ["vehicle"])

        results = self.notebook.search_by_tag("fruit")
        self.assertEqual(len(results), 2)

        results2 = self.notebook.search_by_tag("red")
        self.assertEqual(len(results2), 1)
        self.assertEqual(results2[0].id, note1.id)

        results3 = self.notebook.search_by_tag("unknown")
        self.assertEqual(len(results3), 0)

    def test_sort_notes_by_tags(self):
        note1 = self.notebook.add_note("A", "C", ["tag1"])
        note2 = self.notebook.add_note("B", "C", ["tag1", "tag2", "tag3"])
        note3 = self.notebook.add_note("C", "C")

        results = self.notebook.sort_notes_by_tags()
        self.assertEqual(results[0].id, note2.id)
        self.assertEqual(results[1].id, note1.id)
        self.assertEqual(results[2].id, note3.id)

    def test_sort_notes_by_specific_tags(self):
        note1 = self.notebook.add_note("A", "C", ["work"])
        note2 = self.notebook.add_note("B", "C", ["work", "urgent", "study"])
        note3 = self.notebook.add_note("C", "C", ["home"])

        # Searching & sorting by 'work' and 'urgent'
        results = self.notebook.sort_notes_by_tags(["work", "urgent"])
        # note2 has 2 matches, note1 has 1 match, note3 has 0 matches (excluded)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].id, note2.id)
        self.assertEqual(results[1].id, note1.id)


if __name__ == "__main__":
    unittest.main()
