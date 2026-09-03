from models.fields import Tag

class Note:
    """Represents a single note with an ID, title, content, and optional tags.

    Args:
        note_id (int): The unique identifier for the note.
        title (str): The title of the note.
        content (str): The text content of the note.
        tags (list[str] | None, optional): Tags to associate with the note.
            Defaults to None.

    Returns:
        Note: A new instance of Note.
    """

    def __init__(
        self,
        note_id: int,
        title: str,
        content: str,
        tags: list[str] | None = None,
    ):
        self.id = note_id
        self.title = title.strip()
        self.content = content.strip()
        self.tags: list[Tag] = []
        if tags:
            for t in tags:
                self.add_tag(t)

    def add_tag(self, tag: str) -> None:
        tag_clean = tag.lstrip("#").lower()
        if not any(t.value == tag_clean for t in self.tags):
            self.tags.append(Tag(tag_clean))

    def edit_content(self, new_content: str):
        if not new_content.strip():
            raise ValueError("Content cannot be empty")
        self.content = new_content.strip()

    def __str__(self):
        tags_str = ", ".join(f"#{tag.value}" for tag in self.tags)
        return (
            f"[{self.title}] {self.content} "
            f"(Tags: {tags_str if tags_str else 'None'})"
        )
