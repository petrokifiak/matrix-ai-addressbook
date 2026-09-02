from abc import ABC, abstractmethod
from typing import Any

from models.address_book import AddressBook
from models.notebook import NoteBook

class Context:
    """Context passed to all commands containing application state."""
    def __init__(self, address_book: AddressBook, notebook: NoteBook):
        self.address_book = address_book
        self.notebook = notebook

class Command(ABC):
    """Abstract base class for all CLI commands. Uses the Template Method Pattern."""
    
    def __call__(self, args: list[str], context: Context) -> str:
        """Template method defining the execution lifecycle."""
        self.pre_execute(args, context)
        try:
            result = self.execute(args, context)
            self.post_execute(result, context)
            return result
        except Exception as e:
            return self.on_error(e, context)

    def pre_execute(self, args: list[str], context: Context) -> None:
        """Hook for pre-execution logic (e.g., logging, validation)."""
        pass

    @abstractmethod
    def execute(self, args: list[str], context: Context) -> str:
        """Core logic to be implemented by subclasses."""
        pass

    def post_execute(self, result: str, context: Context) -> None:
        """Hook for post-execution logic (e.g., triggering saves, analytics)."""
        pass

    def on_error(self, error: Exception, context: Context) -> str:
        """Default error handler. Can be overridden."""
        raise error
