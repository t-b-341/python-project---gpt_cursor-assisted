"""
Gameplay screen: runs during STATE_PLAYING and STATE_ENDURANCE.
Orchestrates movement, collision, spawn, AI, and telemetry systems.
Rendering: world via rendering.render_gameplay, then HUD/UI via ui_system.
Uses AppContext for screen; gameplay_ctx dict for level/HUD data.
"""
from __future__ import annotations

from context import AppContext
from rendering import render_gameplay
from systems import GAMEPLAY_SYSTEMS
from systems.ui_system import render as ui_render


def update(state, dt: float, ctx: dict) -> None:
    """Run all gameplay systems for this frame."""
    for system_update in GAMEPLAY_SYSTEMS:
        system_update(state, dt)


def render(app_ctx: AppContext, state, gameplay_ctx: dict) -> None:
    """Draw world and entities, then HUD/UI. app_ctx: AppContext; gameplay_ctx: level/HUD keys."""
    screen = app_ctx.screen
    render_gameplay(state, screen, gameplay_ctx)
    ui_render(state, screen, gameplay_ctx)
