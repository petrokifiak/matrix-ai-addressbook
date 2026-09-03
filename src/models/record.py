from datetime import date
from models.fields import Name, Phone, Email, Address, Birthday

def birthday_in_year(bday: date, year: int) -> date:
    try:
        return bday.replace(year=year)
    except ValueError:
        return bday.replace(year=year, month=2, day=28)

class Record:
    """Class for storing contact info (name, phones, email, address, birthday)."""
    is_archived = False

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.emails: list[Email] = []
        self.addresses: list[Address] = []
        self.birthday: Birthday | None = None
        self.is_archived: bool = False

    def add_phone(self, phone: str) -> None:
        p = Phone(phone)
        if not any(item.value == p.value for item in self.phones):
            self.phones.append(p)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        old_clean = str(old_phone).strip()
        p = self.find_phone(old_clean)
        if p is None:
            raise ValueError("Phone number not found.")
        new_p = Phone(new_phone)
        p.value = new_p.value

    def find_phone(self, phone: str) -> Phone | None:
        clean_phone = str(phone).strip()
        return next((p for p in self.phones if p.value == clean_phone), None)

    def remove_phone(self, phone: str) -> None:
        p = self.find_phone(phone)
        if p is None:
            raise ValueError("Phone number not found.")
        self.phones.remove(p)

    def add_email(self, email: str) -> None:
        e = Email(email)
        if not any(item.value == e.value for item in self.emails):
            self.emails.append(e)

    def add_address(self, address: str) -> None:
        a = Address(address)
        self.addresses.append(a)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def get_age(self, on_date: date | None = None) -> int | None:
        if not self.birthday:
            return None
        on_date = on_date or date.today()
        bday = self.birthday.value
        age = on_date.year - bday.year
        if on_date < birthday_in_year(bday, on_date.year):
            age -= 1
        return age

    def get_turning_age(self, on_date: date | None = None) -> int | None:
        age = self.get_age(on_date)
        return None if age is None else age + 1

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones) or "None"
        emails_str = "; ".join(e.value for e in self.emails) or "None"
        addresses_str = "; ".join(a.value for a in self.addresses) or "None"
        birthday_str = str(self.birthday) if self.birthday else "None"
        archived_str = " (Archived)" if self.is_archived else ""
        return (
            f"Contact name: {self.name.value}{archived_str}, "
            f"phones: {phones_str}, "
            f"emails: {emails_str}, "
            f"addresses: {addresses_str}, "
            f"birthday: {birthday_str}"
        )
