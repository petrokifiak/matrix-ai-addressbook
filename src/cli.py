import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
import os

from core.app import Application
from utils import parse_input

app = typer.Typer(help="Matrix AI Addressbook CLI", invoke_without_command=True)
console = Console(color_system=None)

core_app = Application()

def _execute_and_print(command: str, args: list[str]):
    try:
        result = core_app.execute(command, args)
        console.print(Panel(result, title=f"Command: {command}", border_style="green"))
        core_app.save()
    except Exception as e:
        console.print(Panel(str(e), title="Error", border_style="red"))

@app.command()
def add(name: str, phone: str):
    """Add a new contact with a phone number."""
    _execute_and_print("add", [name, phone])

@app.command()
def all():
    """Show all contacts."""
    try:
        result = core_app.execute("all", [])
        
        # If it returns a string, we can try to parse it, but for now we just print it beautifully.
        # Ideally, 'all' should return data, but since we rely on the old command, we just print the string.
        console.print(Panel(result, title="All Contacts", border_style="blue"))
    except Exception as e:
        console.print(Panel(str(e), title="Error", border_style="red"))

@app.command()
def add_note(title: str, content: str):
    """Add a new note."""
    _execute_and_print("add-note", [title, content])

@app.command()
def notes():
    """Show all notes."""
    _execute_and_print("all-notes", [])

@app.command()
def tui():
    """Launch the full-screen Textual TUI."""
    import subprocess
    import sys
    import os
    
    # We run the TUI in a separate process to avoid Typer/Textual context clashes
    tui_script = os.path.join(os.path.dirname(__file__), "tui.py")
    subprocess.run([sys.executable, tui_script])

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Matrix AI Addressbook
    """
    if ctx.invoked_subcommand is None:
        console.print("Welcome to Matrix AI Addressbook!")
        
        # Extract all registered commands dynamically
        valid_commands = list(core_app.registry._commands.keys())
        # Add exit commands
        valid_commands.extend(["exit", "close"])
        
        command_completer = WordCompleter(valid_commands, ignore_case=True, match_middle=True)
        
        # Setup history
        history_file = os.path.join(os.path.dirname(__file__), "..", "data", ".command_history")
        session_history = FileHistory(history_file)
        
        while True:
            try:
                user_input = prompt("Enter a command: ", completer=command_completer, history=session_history)
                cmd, args = parse_input(user_input)
                
                if cmd in ["close", "exit"]:
                    core_app.save()
                    console.print("Goodbye!")
                    break
                elif not cmd:
                    continue
                    
                _execute_and_print(cmd, args)
            except (KeyboardInterrupt, EOFError):
                core_app.save()
                console.print("\nGoodbye!")
                break

if __name__ == "__main__":
    app()
