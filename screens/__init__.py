"""
Screen handlers for menu, gameplay, pause, high scores, name input, etc.
Each screen can provide handle_events(events, game_state, ctx) and render(screen, game_state, ctx).
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
# handle_events(events, game_state, ctx) -> {"screen": str|None, "quit": bool, "restart": bool}
# render(screen_surface, game_state, ctx) -> None
SCREEN_HANDLERS = {
    STATE_PAUSED: {"handle_events": pause.handle_events, "render": pause.render},
    STATE_HIGH_SCORES: {"handle_events": high_scores.handle_events, "render": high_scores.render},
    STATE_NAME_INPUT: {"handle_events": name_input.handle_events, "render": name_input.render},
}
