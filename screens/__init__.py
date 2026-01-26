"""
Screen handlers for menu, gameplay, pause, high scores, name input, etc.
Each screen provides handle_events(events, game_state, screen_ctx) and render(app_ctx, game_state, screen_ctx).
app_ctx is AppContext (screen, fonts, width, height, etc.); screen_ctx is a dict with get_high_scores, save_high_score, etc.
"""

from . import pause
from . import high_scores
from . import name_input
from constants import (
    STATE_PAUSED,
    STATE_HIGH_SCORES,
    STATE_NAME_INPUT,
)

# Registry: screen_id -> {"handle_events": callable | None, "render": callable}
# handle_events(events, game_state, screen_ctx) -> {"screen": str|None, "quit": bool, "restart": bool}
# render(app_ctx: AppContext, game_state, screen_ctx) -> None
SCREEN_HANDLERS = {
    STATE_PAUSED: {"handle_events": pause.handle_events, "render": pause.render},
    STATE_HIGH_SCORES: {"handle_events": high_scores.handle_events, "render": high_scores.render},
    STATE_NAME_INPUT: {"handle_events": name_input.handle_events, "render": name_input.render},
}
