"""GameplayScene: runs simulation (movement, collision, spawn, AI, telemetry) and renders the game world."""
from __future__ import annotations

from constants import STATE_PLAYING
from screens import gameplay as gameplay_screen


class GameplayScene:
    """Scene for STATE_PLAYING / STATE_ENDURANCE. update runs GAMEPLAY_SYSTEMS; render uses screens.gameplay."""

    def __init__(self, state_id: str = STATE_PLAYING) -> None:
        self._state_id = state_id

    def state_id(self) -> str:
        return self._state_id

    def handle_input(self, events, game_state, ctx: dict) -> dict:
        """Run gameplay input (movement, fire, abilities). Transition to pause is handled by the loop on ESC."""
        out = {"screen": None, "quit": False, "restart": False, "restart_to_wave1": False, "replay": False}
        handle_gameplay_input = ctx.get("handle_gameplay_input")
        if handle_gameplay_input:
            handle_gameplay_input(events, game_state, ctx.get("gameplay_input_ctx") or ctx)
        return out

    def update(self, dt: float, game_state, ctx: dict) -> None:
        gameplay_screen.update(game_state, dt, ctx.get("gameplay_ctx") or {})

    def render(self, render_ctx, game_state, ctx: dict) -> None:
        app_ctx = ctx.get("app_ctx")
        gameplay_ctx = ctx.get("gameplay_ctx")
        if app_ctx is not None and gameplay_ctx is not None:
            gameplay_screen.render(app_ctx, game_state, gameplay_ctx)

    def on_enter(self, game_state, ctx: dict) -> None:
        pass

    def on_exit(self, game_state, ctx: dict) -> None:
        pass
