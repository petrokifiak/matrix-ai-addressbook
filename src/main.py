from config import MESSAGES
from constants import Colors, Command
from handlers import execute_command
from storage import load_data, save_data
from utils import parse_input, print_colored


def main() -> None:
    """Main CLI entry point for the assistant bot."""
    book, notebook = load_data()

    print(f"{Colors.CYAN}{MESSAGES['welcome']}{Colors.RESET}")

    while True:
        try:
            user_input = input(
                f"{Colors.YELLOW}Enter a command:{Colors.RESET} "
            )
            command, args = parse_input(user_input)

            if command in [Command.CLOSE.value, Command.EXIT.value]:
                print(f"{Colors.CYAN}{MESSAGES['goodbye']}{Colors.RESET}")
                save_data(book, notebook)
                break
            elif command == "":
                continue

            result = execute_command(command, args, book, notebook)
            print_colored(result)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Colors.CYAN}{MESSAGES['goodbye']}{Colors.RESET}")
            save_data(book, notebook)
            break


if __name__ == "__main__":
    main()