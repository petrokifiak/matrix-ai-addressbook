from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label
from textual.containers import Container

from core.app import Application

class AddressBookTUI(App):
    """A Textual app to manage the address book."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.core_app = Application()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        
        # Load contacts
        contacts = self.core_app.context.address_book.data.values()
        
        items = []
        for contact in contacts:
            name = contact.name.value
            phones = ", ".join(p.value for p in contact.phones)
            items.append(ListItem(Label(f"👤 {name} - 📞 {phones}")))
            
        yield Container(
            Label("My Contacts", id="title"),
            ListView(*items, id="contacts_list")
        )
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

if __name__ == "__main__":
    app = AddressBookTUI()
    app.run()
