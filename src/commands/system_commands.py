from commands.base import Command, Context
from config import MESSAGES
from help import get_help

class HelloCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        return MESSAGES["hello"]

class HelpCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        return get_help(args)

class ClearDataCommand(Command):
    def execute(self, args: list[str], context: Context) -> str:
        context.address_book.data.clear()
        context.notebook.data.clear()
        return MESSAGES["data_cleared"]
