import difflib
from typing import Dict

from commands.base import Command, Context
from config import ERRORS
from core.middleware import Middleware

class CommandRegistry:
    """Registry and invoker for commands."""
    
    def __init__(self):
        self._commands: Dict[str, Command] = {}
        self._middleware_chain: Middleware | None = None
        
    def register(self, name: str, command: Command) -> None:
        self._commands[name] = command

    def set_middleware(self, middleware: Middleware) -> None:
        self._middleware_chain = middleware
        
    def _execute_command(self, name: str, args: list[str], context: Context) -> str:
        if name in self._commands:
            # Call the template method (__call__) instead of execute directly
            return self._commands[name](args, context)
            
        valid_commands = list(self._commands.keys())
        matches = difflib.get_close_matches(
            name, valid_commands, n=3, cutoff=0.5
        )
        if matches:
            if len(matches) == 1:
                return (
                    f"Invalid command '{name}'. "
                    f"Did you mean: {matches[0]}?"
                )
            suggestions = ", ".join(matches)
            return (
                f"Invalid command '{name}'. "
                f"Did you mean one of these: {suggestions}?"
            )
        raise ValueError(ERRORS["invalid_command"])

    def execute(self, name: str, args: list[str], context: Context) -> str:
        if self._middleware_chain:
            return self._middleware_chain.handle(name, args, context, self._execute_command)
        return self._execute_command(name, args, context)
