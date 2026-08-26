from constants import Command
from config import MESSAGES
from utils import parse_input
from handlers import execute_command
from storage import save_data, load_data

def main() -> None:
    book, notebook = load_data()

    print(MESSAGES["welcome"])

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in [Command.CLOSE.value, Command.EXIT.value]:
            print(MESSAGES["goodbye"])
            save_data(book, notebook)
            break
        elif command == "":
            continue
        
        result = execute_command(command, args, book, notebook)
        print(result)

if __name__ == "__main__":
    main()