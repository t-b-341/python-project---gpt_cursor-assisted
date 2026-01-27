"""HighScoreScene: high scores list. Wraps screens.high_scores handle_events and render."""
from __future__ import annotations

from constants import STATE_HIGH_SCORES
from rendering import RenderContext
from screens import high_scores as high_scores_screen
from scenes.transitions import SceneTransition


class HighScoreScene:
    def state_id(self) -> str:
        return STATE_HIGH_SCORES

    def handle_input(self, events, game_state, ctx: dict) -> dict:
        return high_scores_screen.handle_events(events, game_state, ctx)

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
        high_scores_screen.render(render_ctx, game_state, ctx)

    def on_enter(self, game_state, ctx: dict) -> None:
        pass

    def on_exit(self, game_state, ctx: dict) -> None:
        pass
