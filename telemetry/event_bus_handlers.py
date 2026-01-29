"""EventBus handlers that convert gameplay events into telemetry logs."""
from __future__ import annotations

import logging
from typing import Any

from event_bus import EventBus, GameEvent
from telemetry.events import ScoreEvent


def register_telemetry_event_handlers(
    event_bus: EventBus | None,
    ctx: Any,
    game_state: Any,
) -> None:
    """
    Register EventBus handlers that convert gameplay events into telemetry logs.
    Safe no-ops when telemetry is disabled or client is missing.
    """
    if event_bus is None:
        return

    def _on_enemy_killed(ev: GameEvent) -> None:
        # Config gate
        cfg = getattr(ctx, "config", None)
        if not cfg or not getattr(cfg, "enable_telemetry", False):
            return

        client = getattr(ctx, "telemetry_client", None)
        if not client:
            return

        # Extract fields from the payload
        payload = ev.payload or {}
        score_delta = int(payload.get("score_delta", 0))

        if score_delta == 0:
            return  # nothing meaningful to log

        enemy_type = str(payload.get("enemy_type", "enemy"))

        t = float(getattr(game_state, "run_time", 0.0))
        score_total = int(getattr(game_state, "score", 0))

        event = ScoreEvent(
            t=t,
            score=score_total,
            score_change=score_delta,
            source=enemy_type,
        )

        try:
            client.log_score(event)
        except Exception:
            logging.exception("Failed to log ScoreEvent for enemy_killed")

    event_bus.subscribe("enemy_killed", _on_enemy_killed)
