from models import AddressBook, NoteBook

def get_default_path() -> str:
    """
    Повертає шлях за замовчуванням до файлу збереження в домашній директорії користувача.
    """
    # TODO: Реалізувати створення директорії та повернення шляху
    pass

def save_data(address_book: AddressBook, notebook: NoteBook | None = None, filename: str | None = None) -> None:
    """
    Зберігає адресну книгу та блокнот на диск за допомогою модуля pickle.
    """
    # TODO: Реалізувати серіалізацію контактів та нотаток у файл
    pass

def load_data(filename: str | None = None) -> tuple[AddressBook, NoteBook]:
    """
    Завантажує адресну книгу та блокнот з диска. Якщо файлу немає, повертає нові пусті екземпляри.
    """
    # TODO: Реалізувати десеріалізацію даних з файлу
    return AddressBook(), NoteBook()
