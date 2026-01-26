"""
Gameplay screen: runs during STATE_PLAYING and STATE_ENDURANCE.
Orchestrates movement, collision, spawn, AI, and telemetry systems.
Rendering: five phases (background, entities, projectiles, HUD, overlays).
Uses AppContext for screen; gameplay_ctx dict for level/HUD data.
"""
from __future__ import annotations

from context import AppContext
from rendering import (
    RenderContext,
    render_background,
    render_entities,
    render_projectiles,
)
from systems import GAMEPLAY_SYSTEMS
from systems.ui_system import render_hud, render_overlays


def update(state, dt: float, ctx: dict) -> None:
    """Run all gameplay systems for this frame."""
    for system_update in GAMEPLAY_SYSTEMS:
        system_update(state, dt)


def render(app_ctx: AppContext, state, gameplay_ctx: dict) -> None:
    """Draw frame in five phases: background, entities, projectiles, HUD, overlays. Visually identical to previous pipeline."""
    render_ctx = RenderContext.from_app_ctx(app_ctx)
    # (1) Background: theme fill, terrain, pickups
    render_background(state, gameplay_ctx, render_ctx)
    # (2) Entities: allies, enemies, player
    render_entities(state, gameplay_ctx, render_ctx)
    # (3) Projectiles/particles: projectiles, effects, beams
    render_projectiles(state, gameplay_ctx, render_ctx)
    # (4) HUD: health bars, score, metrics, cooldown bars
    render_hud(state, gameplay_ctx, render_ctx)
    # (5) Overlays: damage numbers, defeat/pickup messages, wave countdown
    render_overlays(state, gameplay_ctx, render_ctx)
