"""Telemetry logging integration during gameplay."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from state import GameState


def update(state: "GameState", dt: float) -> None:
    """Flush or log telemetry for this frame. Called from gameplay screen.
    Stub: per-frame telemetry still runs in game.py; extend here when extracted."""
    pass
