You are editing the repo `game.py_cursor_gpt_assisted-MAIN_BRANCH`.

GOAL
====
Add a small, future-proof **event bus** to decouple systems, and integrate it at a few **minimal, safe insertion points**, with **pytest tests** for the new behavior. Keep changes additive and conservative so existing behavior and tests continue to pass.

High-level requirements:
- Introduce an `EventBus` abstraction with a simple `GameEvent` container.
- Attach an EventBus instance to `AppContext` so systems can opt-in to publishing/subscribing.
- Emit at least one meaningful gameplay event (`"enemy_killed"`) from the existing flow where enemies are killed.
- Add focused pytest tests for:
  - The event bus itself.
  - The `"enemy_killed"` integration at the kill site.
- Preserve style, naming, and patterns used elsewhere in the project.


STEP 1 — Add event_bus.py
==========================
Create a new module at the top level:

**File:** `event_bus.py`

Implement a simple, type-annotated event system:

- A small `GameEvent` dataclass to carry:
  - `type: str`
  - `payload: dict[str, object]`
- An `EventBus` class that supports:
  - `subscribe(event_type: str, handler: Callable[[GameEvent], None]) -> None`
  - `unsubscribe(event_type: str, handler: Callable[[GameEvent], None]) -> None`
  - `publish(event: GameEvent) -> None`
- Behavior:
  - Multiple handlers per event type, called in registration order.
  - Publishing to an event type with **no subscribers** should be a no-op (no errors).
  - Handlers must be robust: if a handler raises, log it via `logging` but do **not** prevent other handlers from running.
- Keep implementation small and straightforward, matching the project’s style (docstrings, logging usage similar to other utility modules).


STEP 2 — Wire EventBus into AppContext
======================================
We want the event bus available via `AppContext`, which already holds telemetry, config, and other shared services.

**File:** `context.py`

1. Add a new field to `AppContext`:

   - Name it `event_bus`.
   - Type annotate as `Any` or a forward reference to avoid import cycles, e.g.:

   ```python
   from typing import Any, Optional
   ...
   event_bus: Optional[Any] = None







You are editing the repo `game.py_cursor_gpt_assisted-MAIN_BRANCH`.

GOAL
====
Integrate the EventBus with the telemetry system so that `"enemy_killed"` events automatically produce `ScoreEvent` telemetry logs.  
All changes must be **additive**, **safe**, and **covered by tests**.  
Insert at the **reasonable minimal points** without refactoring unrelated systems.

Apply ALL changes in this single prompt.


====================================================================================================
STEP 1 — ADD FILE: telemetry/event_bus_handlers.py
====================================================================================================
Create the file `telemetry/event_bus_handlers.py` with the following implementation:

--------------------------------------------------------------------------------
# telemetry/event_bus_handlers.py
--------------------------------------------------------------------------------
from __future__ import annotations

from typing import Any
from telemetry.events import ScoreEvent
from event_bus import EventBus, GameEvent
import logging


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


====================================================================================================
STEP 2 — IMPORT & REGISTER HANDLERS INSIDE game.py:_create_app()
====================================================================================================
Modify `game.py` as follows:

1. Near existing telemetry imports, add:

--------------------------------------------------------------------------------
from telemetry.event_bus_handlers import register_telemetry_event_handlers
--------------------------------------------------------------------------------

2. In `_create_app()`, after `_prompt_shader_mode(ctx)` but BEFORE `_build_loop_params()`:

--------------------------------------------------------------------------------
    # Hook telemetry handlers into EventBus
    register_telemetry_event_handlers(ctx.event_bus, ctx, game_state)
--------------------------------------------------------------------------------


====================================================================================================
STEP 3 — SANITY CHECK kill_enemy EVENT SHAPE
====================================================================================================
Ensure kill_enemy publishes enemy_killed with the required fields.

In `game.py`, confirm the event publishing looks like:

--------------------------------------------------------------------------------
if ctx is not None and getattr(ctx, "event_bus", None) is not None:
    try:
        ctx.event_bus.publish(GameEvent(
            type="enemy_killed",
            payload={
                "enemy_type": enemy_type,
                "is_boss": is_boss,
                "wave_number": state.wave_number,
                "score_delta": score_delta,
            },
        ))
    except Exception:
        import logging
        logging.exception("Failed to publish enemy_killed")
--------------------------------------------------------------------------------

If it already matches, do nothing.  
If not, replace the existing publish block with the above minimal safe version.


====================================================================================================
STEP 4 — ADD TEST FILE: tests/test_telemetry_enemy_killed_event.py
====================================================================================================
Create the test file:

--------------------------------------------------------------------------------
# tests/test_telemetry_enemy_killed_event.py
--------------------------------------------------------------------------------
from __future__ import annotations

import pytest
from dataclasses import dataclass

from event_bus import EventBus, GameEvent
from telemetry.events import ScoreEvent
from telemetry.event_bus_handlers import register_telemetry_event_handlers


@dataclass
class FakeConfig:
    enable_telemetry: bool = True


class FakeTelemetryClient:
    def __init__(self):
        self.logged: list[ScoreEvent] = []

    def log_score(self, e: ScoreEvent) -> None:
        self.logged.append(e)


class FakeCtx:
    def __init__(self, enable_telemetry: bool, client):
        self.config = FakeConfig(enable_telemetry=enable_telemetry)
        self.telemetry_client = client


class FakeGameState:
    def __init__(self, score: int, run_time: float):
        self.score = score
        self.run_time = run_time


def test_enemy_killed_event_logs_score_event_when_telemetry_enabled():
    bus = EventBus()
    client = FakeTelemetryClient()
    ctx = FakeCtx(enable_telemetry=True, client=client)
    gs = FakeGameState(score=1234, run_time=12.5)

    register_telemetry_event_handlers(bus, ctx, gs)

    ev = GameEvent(
        type="enemy_killed",
        payload={"enemy_type": "grunt", "wave_number": 3, "score_delta": 50},
    )
    bus.publish(ev)

    assert len(client.logged) == 1
    se = client.logged[0]
    assert isinstance(se, ScoreEvent)
    assert se.score == 1234
    assert se.score_change == 50
    assert se.source == "grunt"
    assert se.t == pytest.approx(12.5)


def test_enemy_killed_event_noop_when_telemetry_disabled():
    bus = EventBus()
    client = FakeTelemetryClient()
    ctx = FakeCtx(enable_telemetry=False, client=client)
    gs = FakeGameState(score=500, run_time=3.0)

    register_telemetry_event_handlers(bus, ctx, gs)

    ev = GameEvent(type="enemy_killed", payload={"enemy_type": "grunt", "score_delta": 50})
    bus.publish(ev)

    assert client.logged == []


def test_enemy_killed_event_noop_when_client_is_none():
    bus = EventBus()
    ctx = FakeCtx(enable_telemetry=True, client=None)
    gs = FakeGameState(score=500, run_time=3.0)

    register_telemetry_event_handlers(bus, ctx, gs)

    ev = GameEvent(type="enemy_killed", payload={"enemy_type": "grunt", "score_delta": 50})

    # Should not raise even if client is None
    bus.publish(ev)


def test_enemy_killed_event_ignored_when_score_delta_zero():
    bus = EventBus()
    client = FakeTelemetryClient()
    ctx = FakeCtx(enable_telemetry=True, client=client)
    gs = FakeGameState(score=999, run_time=1.0)

    register_telemetry_event_handlers(bus, ctx, gs)

    ev = GameEvent(type="enemy_killed", payload={"enemy_type": "grunt", "score_delta": 0})
    bus.publish(ev)

    assert client.logged == []
--------------------------------------------------------------------------------


====================================================================================================
STEP 5 — EXPECTED RESULTS
====================================================================================================
✔ Telemetry now logs ScoreEvent automatically when enemies die  
✔ All existing gameplay continues unchanged  
✔ Integration is fully test-covered  
✔ EventBus becomes a real gameplay → telemetry bridge  
✔ Future event types can be added easily


====================================================================================================
Run the full test suite:
pytest
====================================================================================================
