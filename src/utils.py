from constants import Colors
from config import MESSAGES, ERRORS

def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.split()
    if not parts:
        return "", []
    cmd = parts[0].strip().lower()
    args = parts[1:]
    return cmd, args

def print_colored(text: str) -> None:
    """Prints text with the appropriate color based on its content."""
    if text is None:
        print(f"{Colors.YELLOW}This feature is not implemented yet.{Colors.RESET}")
        return

    # If the text already contains ANSI codes (e.g. from help.py)
    if "\033[" in text:
        print(text)
        return

    # Check for errors
    is_error = False
    for err in ERRORS.values():
        if err in text:
            is_error = True
            break
    
    if is_error or text.startswith("Invalid") or text.startswith("Command '"):
        print(f"{Colors.RED}{text}{Colors.RESET}")
    # Check for success messages
    elif any(msg in text for msg in MESSAGES.values()) and text not in (MESSAGES.get("welcome", ""), MESSAGES.get("goodbye", "")):
        print(f"{Colors.GREEN}{text}{Colors.RESET}")
    else:
        # Standard output
        print(text)
