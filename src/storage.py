import os
import pickle
from pathlib import Path
from models import AddressBook, NoteBook

DEFAULT_STORAGE_DIR = Path.home() / ".personal_assistant"
DEFAULT_STORAGE_FILENAME = "assistant_data.pkl"
DEFAULT_STORAGE_FILE = DEFAULT_STORAGE_DIR / DEFAULT_STORAGE_FILENAME

def get_default_path() -> str:
    """Ensure the default storage directory exists and return the path to the storage file.

    Returns:
        str: Absolute path to 'assistant_data.pkl' in '~/.personal_assistant'.
    """
    # create default storage directory if it doesn't exist with subfolders and without error FileExistsError if folder already exists 
    DEFAULT_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    return str(DEFAULT_STORAGE_FILE)

def save_data(
    address_book: AddressBook,
    notebook: NoteBook | None = None,
    filename: str | None = None,
) -> None:
    """Serialize and save AddressBook and NoteBook data to disk using pickle.

    Args:
        address_book (AddressBook): The contact book instance to save.
        notebook (NoteBook | None, optional): The note book instance. Defaults to NoteBook().
        filename (str | None, optional): Custom file path to save data into. Defaults to
            '~/.personal_assistant/assistant_data.pkl'.
    """
    notes = notebook if notebook is not None else NoteBook()
    target_path = filename if filename else get_default_path()
    with open(target_path, "wb") as file:
        pickle.dump({"contacts": address_book, "notes": notes}, file)


def load_data(filename: str | None = None):
    """Load and deserialize AddressBook and NoteBook data from disk.

    Args:
        filename (str | None, optional): Custom file path to load data from (used for testing).
            If None, loads from '~/.personal_assistant/assistant_data.pkl'.

    Returns:
        AddressBook | tuple[AddressBook, NoteBook]: Returns contacts (and notes) or fresh empty instances.
    """
    target_path = filename if filename else get_default_path()
    if os.path.exists(target_path):
        try:
            with open(target_path, "rb") as file:
                data = pickle.load(file)
                if isinstance(data, dict):
                    return data.get("contacts", AddressBook()), data.get("notes", NoteBook())
        # Return empty instance if file is empty or corrupted
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            pass

    return AddressBook(), NoteBook()