from typing import Callable, Dict, List, Any

class EventDispatcher:
    """Singleton Event Dispatcher for Observer Pattern."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventDispatcher, cls).__new__(cls)
            cls._instance._listeners: Dict[str, List[Callable]] = {}
        return cls._instance

    def subscribe(self, event_type: str, listener: Callable[[Any], None]) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def dispatch(self, event_type: str, data: Any = None) -> None:
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(data)

# Global instance
dispatcher = EventDispatcher()

class LoggingObserver:
    """An observer that logs events."""
    def on_contact_added(self, data: Any) -> None:
        name = data.get('name') if isinstance(data, dict) else str(data)
        print(f"[DEBUG LOG] A new contact was added: {name}")

    def on_note_added(self, data: Any) -> None:
        title = data.get('title') if isinstance(data, dict) else str(data)
        print(f"[DEBUG LOG] A new note was added: {title}")
