"""
Gameplay screen: runs during STATE_PLAYING and STATE_ENDURANCE.
Orchestrates movement, collision, spawn, AI, and telemetry systems.
"""
from systems import GAMEPLAY_SYSTEMS


def update(state, dt: float, ctx: dict) -> None:
    """Run all gameplay systems for this frame."""
    for system_update in GAMEPLAY_SYSTEMS:
        system_update(state, dt)
