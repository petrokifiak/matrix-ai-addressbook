from abc import ABC, abstractmethod
from commands.base import Context, Command
from typing import Callable

class Middleware(ABC):
    """Chain of Responsibility for command processing."""
    
    def __init__(self):
        self.next_middleware = None

    def set_next(self, middleware: 'Middleware') -> 'Middleware':
        self.next_middleware = middleware
        return middleware

    @abstractmethod
    def handle(self, command_name: str, args: list[str], context: Context, executor: Callable) -> str:
        if self.next_middleware:
            return self.next_middleware.handle(command_name, args, context, executor)
        return executor(command_name, args, context)

class LoggingMiddleware(Middleware):
    def handle(self, command_name: str, args: list[str], context: Context, executor: Callable) -> str:
        # Example of cross-cutting concern
        print(f"[MIDDLEWARE] Executing command '{command_name}' with args {args}")
        return super().handle(command_name, args, context, executor)

class ValidationMiddleware(Middleware):
    def handle(self, command_name: str, args: list[str], context: Context, executor: Callable) -> str:
        # Check if the context is valid before executing
        if context.address_book is None or context.notebook is None:
            raise ValueError("Application state is corrupted.")
        return super().handle(command_name, args, context, executor)
