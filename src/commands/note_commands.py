from commands.base import Command, Context
from config import ERRORS, MESSAGES
from storage.exporters import FileExporter
from core.events import dispatcher
from formatters import generate_notes_table

class AddNoteCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        title = args[0]
        content = " ".join(args[1:])
        if not content:
            raise IndexError
        note = context.notebook.add_note(title, content)
        dispatcher.dispatch("NOTE_ADDED", {"title": title, "content": content})
        return f"{MESSAGES['note_added']} ID: {note.id}"

class ShowNotesCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not context.notebook.data:
            return MESSAGES.get("no_notes", "No notes found.")
        return generate_notes_table(list(context.notebook.data.values()))

class SearchNotesCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        query = " ".join(args)
        if not query:
            raise IndexError
        results = context.notebook.search_notes(query)
        if not results:
            return MESSAGES["no_matching_notes"]
        return generate_notes_table(results)

class EditNoteCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if len(args) < 2:
            raise IndexError
        identifier = args[0]
        new_content = " ".join(args[1:])
        if not new_content:
            raise IndexError
        success = context.notebook.edit_note(identifier, new_content)
        if not success:
            raise ValueError(ERRORS["note_not_found"])
        return MESSAGES["note_updated"]

class DeleteNoteCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        identifier = args[0]
        success = context.notebook.delete_note(identifier)
        if not success:
            raise ValueError(ERRORS["note_not_found"])
        return MESSAGES["note_deleted"]

class AddTagCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if len(args) < 2:
            raise IndexError
        identifier = args[0]
        tags = args[1:]
        note = context.notebook.find_note(identifier)
        if not note:
            raise ValueError(ERRORS["note_not_found"])
        for tag in tags:
            note.add_tag(tag)
        return MESSAGES.get("tag_added", "Tags added.")

class SearchByTagCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        tag = args[0]
        results = context.notebook.search_by_tag(tag)
        if not results:
            return MESSAGES.get("no_matching_notes", "No notes found.")
        return generate_notes_table(results)

class SortNotesCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        results = context.notebook.sort_notes_by_tags(args)
        if not results:
            if args:
                return MESSAGES.get("no_matching_notes", "No matching notes found.")
            return MESSAGES.get("no_notes", "No notes found.")
        return generate_notes_table(results)

class ExportNotesCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        filepath = args[0]
        exporter = FileExporter()
        return exporter.export_notes(context.notebook, filepath)

class ImportNotesCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        if not args:
            raise IndexError
        filepath = args[0]
        exporter = FileExporter()
        return exporter.import_notes(context.notebook, filepath)

class ClearNotesCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        context.notebook.data.clear()
        return MESSAGES["notes_cleared"]
