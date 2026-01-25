"""
Gameplay screen: runs during STATE_PLAYING and STATE_ENDURANCE.
Orchestrates movement, collision, spawn, AI, and telemetry systems.
UI/HUD drawing is delegated to systems.ui_system.
"""
from systems import GAMEPLAY_SYSTEMS
from systems.ui_system import render as ui_render


def update(state, dt: float, ctx: dict) -> None:
    """Run all gameplay systems for this frame."""
    for system_update in GAMEPLAY_SYSTEMS:
        system_update(state, dt)


def render(screen, state, ctx: dict) -> None:
    """Draw all gameplay HUD/UI. Delegates to ui_system.render."""
    ui_render(state, screen, ctx)
