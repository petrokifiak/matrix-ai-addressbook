from models.record import Record

class ContactBuilder:
    """Builder Pattern for creating complex Records."""
    def __init__(self, name: str):
        self._record = Record(name)
        
    def add_phone(self, phone: str) -> 'ContactBuilder':
        self._record.add_phone(phone)
        return self
        
    def add_email(self, email: str) -> 'ContactBuilder':
        self._record.add_email(email)
        return self
        
    def add_address(self, address: str) -> 'ContactBuilder':
        self._record.add_address(address)
        return self
        
    def add_birthday(self, birthday: str) -> 'ContactBuilder':
        self._record.add_birthday(birthday)
        return self
        
    def build(self) -> Record:
        return self._record
