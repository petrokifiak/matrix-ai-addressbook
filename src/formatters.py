from rich.table import Table

def generate_contacts_table(contacts_list):
    """Generate a rich Table for a list of contacts."""
    if not contacts_list:
        return "No contacts found."
        
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Phones", style="white")
    table.add_column("Email", style="blue")
    table.add_column("Birthday", style="green")
    table.add_column("Address", style="yellow")
    
    for contact in contacts_list:
        name = str(contact.name)
        phones = ", ".join(str(p) for p in contact.phones) if contact.phones else ""
        email = ", ".join(str(e) for e in contact.emails) if hasattr(contact, "emails") and contact.emails else ""
        birthday = str(contact.birthday) if contact.birthday else ""
        address = ", ".join(str(a) for a in contact.addresses) if hasattr(contact, "addresses") and contact.addresses else ""
        
        table.add_row(name, phones, email, birthday, address)
        
    return table

def generate_birthdays_table(upcoming_list, days):
    if not upcoming_list:
        return f"No upcoming birthdays for the next {days} days."
        
    table = Table(show_header=True, header_style="bold magenta", title=f"Upcoming birthdays for the next {days} days")
    table.add_column("Name", style="cyan")
    table.add_column("Congratulation Date", style="white")
    table.add_column("Turning Age", style="green")
    
    for item in upcoming_list:
        table.add_row(item['name'], item['congratulation_date'], str(item['age']))
        
    return table

def generate_notes_table(notes_list):
    """Generate a rich Table for a list of notes."""
    if not notes_list:
        return "No notes found."
        
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Title", style="cyan", width=20)
    table.add_column("Content", style="white")
    table.add_column("Tags", style="green", justify="right")
    
    for note in notes_list:
        title = str(note.title) if note.title else "Untitled"
        content = str(note.content) if note.content else ""
        tags = ", ".join(str(t) for t in note.tags) if note.tags else ""
        
        table.add_row(title, content, tags)
        
    return table
