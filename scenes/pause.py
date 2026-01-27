"""PauseScene: pause overlay and menu. Wraps screens.pause handle_events and render."""
from __future__ import annotations

from constants import STATE_PAUSED
from rendering import RenderContext
from screens import pause as pause_screen
from scenes.transitions import SceneTransition


class PauseScene:
    def state_id(self) -> str:
        return STATE_PAUSED

    def handle_input(self, events, game_state, ctx: dict) -> dict:
        return pause_screen.handle_events(events, game_state, ctx)

    def update(self, dt: float, game_state, ctx: dict) -> None:
        pass

    def handle_input_transition(self, events, game_state, ctx: dict) -> SceneTransition:
        """Stub: call existing logic; return NONE. Used by future scene-driven loop."""
        self.handle_input(events, game_state, ctx)
        return SceneTransition.none()

    def update_transition(self, dt: float, game_state, ctx: dict) -> SceneTransition:
        """Stub: call existing logic; return NONE. Used by future scene-driven loop."""
        self.update(dt, game_state, ctx)
        return SceneTransition.none()

    def render(self, render_ctx: RenderContext, game_state, ctx: dict) -> None:
        pause_screen.render(render_ctx, game_state, ctx)

    def on_enter(self, game_state, ctx: dict) -> None:
        pass

    def on_exit(self, game_state, ctx: dict) -> None:
        pass
