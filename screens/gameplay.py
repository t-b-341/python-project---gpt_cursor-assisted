"""
Gameplay screen: runs during STATE_PLAYING and STATE_ENDURANCE.
Orchestrates movement, collision, spawn, AI, and telemetry systems.
Rendering: world via rendering.render_gameplay, then HUD/UI via ui_system.
"""
from systems import GAMEPLAY_SYSTEMS
from systems.ui_system import render as ui_render

from rendering import render_gameplay


def update(state, dt: float, ctx: dict) -> None:
    """Run all gameplay systems for this frame."""
    for system_update in GAMEPLAY_SYSTEMS:
        system_update(state, dt)


def render(screen, state, ctx: dict) -> None:
    """Draw world and entities, then HUD/UI. ctx must contain both world and HUD keys."""
    render_gameplay(state, screen, ctx)
    ui_render(state, screen, ctx)
