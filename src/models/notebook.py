from collections import UserDict
from models.note import Note

class NoteBook(UserDict[int, Note]):
    """A collection of Note objects managed as a dictionary of IDs to Notes.

    Args:
        None

    Returns:
        NoteBook: A new empty instance of NoteBook.
    """

    def __init__(self):
        super().__init__()
        self._next_id: int = 1

    def add_note(
        self,
        title: str,
        content: str,
        tags: list[str] | None = None,
    ) -> Note:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if not content or not content.strip():
            raise ValueError("Content cannot be empty")

        note_id = max(self.data.keys(), default=0) + 1
        note = Note(note_id, title, content, tags)
        self.data[note_id] = note
        return note

    def edit_note(self, identifier: str | int, new_content: str) -> bool:
        note = self.find_note(identifier)
        if note:
            note.edit_content(new_content)
            return True
        return False

    def find_note(self, identifier: str | int) -> Note | None:
        if str(identifier).isdigit():
            return self.data.get(int(identifier))
        # Search by name
        for note in self.data.values():
            if note.title.lower() == str(identifier).lower():
                return note
        return None

    def delete_note(self, identifier: str | int) -> bool:
        note = self.find_note(identifier)
        if note:
            del self.data[note.id]
            return True
        return False

    def search_notes(self, query: str) -> list[Note]:
        """Search notes containing the query in title or content (case-insensitive)."""
        query_lower = query.lower()
        return [
            note
            for note in self.data.values()
            if (
                query_lower in note.title.lower()
                or query_lower in note.content.lower()
            )
        ]

    def search_by_tag(self, tag: str) -> list[Note]:
        tag_clean = tag.lstrip("#").lower()
        return [
            note
            for note in self.data.values()
            if any(t.value == tag_clean for t in note.tags)
        ]

    def sort_notes_by_tags(self, tags: list[str] | None = None) -> list[Note]:
        """Sort notes by specified tags (match count descending).

        If no tags are specified, sorts all notes by total number of tags.
        """
        if tags:
            clean_tags = [
                t.lstrip("#").strip().lower() for t in tags if t.strip()
            ]
            scored_notes = []
            # Iterate through all stored notes in the notebook
            for note in self.data.values():
                # Extract clean string values of all tags assigned to note
                note_tag_vals = {t.value for t in note.tags}
                # Calculate how many searched tags match the current note
                match_count = sum(1 for t in clean_tags if t in note_tag_vals)
                # If at least one matching tag, include note with score
                if match_count > 0:
                    scored_notes.append((match_count, note))
            # Sort by match count descending, then by total tags descending
            scored_notes.sort(
                key=lambda item: (item[0], len(item[1].tags)),
                reverse=True,
            )
            return [note for _, note in scored_notes]

        return sorted(
            self.data.values(),
            key=lambda n: len(n.tags),
            reverse=True,
        )
