import re
from datetime import datetime

from config import ERRORS
from constants import DATE_FORMAT, PHONE_FORMAT, EMAIL_FORMAT

class Field:
    """Base class for record fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing contact name. Required field."""

    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError("Name cannot be empty")
        super().__init__(str(value).strip())


class Phone(Field):
    """Class for storing phone number. Format: 10 digits."""

    def __init__(self, value):
        clean_value = str(value).strip()
        if not re.search(PHONE_FORMAT, clean_value):
            raise ValueError(ERRORS["invalid_phone"])
        super().__init__(clean_value)


class Email(Field):
    """Class for storing email."""

    def __init__(self, value):
        clean_value = str(value).strip()
        if not re.search(EMAIL_FORMAT, clean_value):
            raise ValueError(ERRORS["invalid_email"])
        super().__init__(clean_value)


class Address(Field):
    """Class for storing contact physical address."""

    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError("Address cannot be empty")
        super().__init__(str(value).strip())


class Birthday(Field):
    """Class for storing birthday. Format: DD.MM.YYYY."""

    def __init__(self, value):
        val_str = str(value).strip()
        try:
            parts = val_str.split('.')
            if len(parts) != 3:
                raise ValueError("Format must be DD.MM.YYYY")
            
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            
            if day < 1:
                raise ValueError(f"Minus or zero value {day} for date is not allowed.")
            if month < 1 or month > 12:
                raise ValueError(f"Invalid month: {month}")
            if year < 1:
                raise ValueError("Year cannot be negative or zero.")
                
            # Check calendar bounds explicitly
            import calendar
            max_days = calendar.monthrange(year, month)[1]
            if day > max_days:
                if month == 2 and day == 29:
                    raise ValueError(f"29 for year where it's not a leap year ({year}).")
                raise ValueError(f"Value {day} for date is out of bounds for month {month}.")
            
            birthday = datetime(year, month, day).date()
        except ValueError as e:
            # If it's our custom ValueError, raise it directly
            if "Format must be" not in str(e) and "invalid literal" not in str(e):
                raise ValueError(str(e))
            raise ValueError(f"{ERRORS['invalid_birthday']} Details: {str(e)}")
        
        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)


class Tag(Field):
    """Class for note tags."""

    def __init__(self, value):
        clean_value = str(value).lstrip("#").strip().lower()
        if not clean_value:
            raise ValueError("Tag cannot be empty")
        super().__init__(clean_value)
