from collections import UserDict
from datetime import date, timedelta
from constants import DATE_FORMAT
from models.record import Record, birthday_in_year

class AddressBook(UserDict):
    """Class for managing contacts (contacts database)."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            self.data[name].is_archived = True
        else:
            raise KeyError

    def search(self, query: str) -> list[Record]:
        query_lower = query.lower()
        results = []
        for record in self.data.values():
            if record.is_archived:
                continue
            if query_lower in record.name.value.lower():
                results.append(record)
                continue
            if any(query_lower in p.value.lower() for p in record.phones):
                results.append(record)
                continue
            if any(query_lower in e.value.lower() for e in record.emails):
                results.append(record)
                continue
            if any(query_lower in a.value.lower() for a in record.addresses):
                results.append(record)
                continue
        return results

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        today = date.today()
        upcoming = []
        for record in self.data.values():
            if record.is_archived or not record.birthday:
                continue
            bday = record.birthday.value  # datetime.date object
            bday_this_year = birthday_in_year(bday, today.year)
            if bday_this_year < today:
                bday_this_year = birthday_in_year(bday, today.year + 1)

            delta = (bday_this_year - today).days
            if 0 <= delta <= days:
                congratulation_date = bday_this_year
                if congratulation_date.weekday() == 5:  # Saturday -> Monday
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # Sunday -> Monday
                    congratulation_date += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime(DATE_FORMAT),
                    # Count from the birthday itself, not from the date shifted to Monday
                    "age": bday_this_year.year - bday.year
                })
        return upcoming
