"""Telemetry logging integration during gameplay. Per-frame sampling and flush tick."""
from __future__ import annotations

from constants import POS_SAMPLE_INTERVAL
from context import AppContext
from telemetry import PlayerPosEvent
from state import GameState


def update_telemetry(gs: GameState, dt: float, app_ctx: AppContext) -> None:
    """Per-frame telemetry: flush tick and position/run_state samples at POS_SAMPLE_INTERVAL.
    Reads/writes app_ctx.last_telemetry_sample_t. No-op if telemetry disabled or no client."""
    if not getattr(app_ctx.config, "enable_telemetry", False) or not app_ctx.telemetry_client:
        return
    client = app_ctx.telemetry_client
    client.tick(dt)
    now = gs.run_time
    last_t = app_ctx.last_telemetry_sample_t
    if last_t < 0:
        app_ctx.last_telemetry_sample_t = now
        return
    if now - last_t < POS_SAMPLE_INTERVAL or not gs.player_rect:
        return
    client.log_player_position(
        PlayerPosEvent(t=now, x=gs.player_rect.centerx, y=gs.player_rect.centery)
    )
    client.log_run_state_sample(now, gs.player_hp, len(gs.enemies))
    app_ctx.last_telemetry_sample_t = now
