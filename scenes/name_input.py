"""NameInputScene: enter name for high score. Wraps screens.name_input handle_events and render."""
from __future__ import annotations

from constants import STATE_NAME_INPUT
from rendering import RenderContext
from screens import name_input as name_input_screen


class NameInputScene:
    def state_id(self) -> str:
        return STATE_NAME_INPUT

    def handle_input(self, events, game_state, ctx: dict) -> dict:
        return name_input_screen.handle_events(events, game_state, ctx)

    def update(self, dt: float, game_state, ctx: dict) -> None:
        pass

    def render(self, render_ctx: RenderContext, game_state, ctx: dict) -> None:
        name_input_screen.render(render_ctx, game_state, ctx)

    def on_enter(self, game_state, ctx: dict) -> None:
        pass

    def on_exit(self, game_state, ctx: dict) -> None:
        pass
