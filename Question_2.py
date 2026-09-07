from collections import defaultdict
from typing import Callable


class EventDispatcher:
    def __init__(self):
        # Stores event types and their callbacks
        self._subscribers = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable):
        """Register a callback for an event."""
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        """Remove a callback from an event."""
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(callback)

                # Remove empty event entries
                if not self._subscribers[event_type]:
                    del self._subscribers

            except ValueError:
                pass

    def dispatch(self, event_type: str, *args, **kwargs):
        """Execute all callbacks for an event."""
        for callback in self._subscribers.get(event_type, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                print(f"Error: {e}")

def send_email(username):
    print(f"Email sent to {username}")


def update_database(username):
    print(f"Database updated for {username}")


def failing_callback(username):
    raise Exception("Database connection failed")


dispatcher = EventDispatcher()

dispatcher.subscribe("user_registered", send_email)
dispatcher.subscribe("user_registered", failing_callback)
dispatcher.subscribe("user_registered", update_database)

dispatcher.dispatch("user_registered", "Linda")

dispatcher.unsubscribe("user_registered", failing_callback)

dispatcher.dispatch("user_registered", "Linda")

