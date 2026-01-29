"""Simple event bus for decoupling systems. Handlers subscribe by event type; publishers emit GameEvents."""
from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

logger = logging.getLogger(__name__)


@dataclass
class GameEvent:
    """Carries an event type and optional payload for subscribers."""
    type: str
    payload: dict[str, object]


class EventBus:
    """
    Publish/subscribe event bus. Multiple handlers per event type, called in registration order.
    Publishing with no subscribers is a no-op. Handler exceptions are logged; other handlers still run.
    """
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[GameEvent], None]]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[GameEvent], None]) -> None:
        """Register a handler for the given event type."""
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[GameEvent], None]) -> None:
        """Remove a previously registered handler for the given event type."""
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
            except ValueError:
                pass

    def publish(self, event: GameEvent) -> None:
        """Notify all handlers for this event's type. Logs handler errors; does not re-raise."""
        for handler in self._handlers.get(event.type, []):
            try:
                handler(event)
            except Exception as e:
                logger.exception("Event handler failed for %s: %s", event.type, e)
