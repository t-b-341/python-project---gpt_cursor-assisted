"""
Cross-cutting systems used during gameplay.
Each system provides update(state: GameState, dt: float) -> None.
Orchestrated by the gameplay screen in its update().
"""
from .movement_system import update as movement_update
from .collision_system import update as collision_update
from .spawn_system import update as spawn_update
from .ai_system import update as ai_update
from .telemetry_system import update as telemetry_update

# Ordered list of systems run each gameplay frame
GAMEPLAY_SYSTEMS = [
    movement_update,
    collision_update,
    spawn_update,
    ai_update,
    telemetry_update,
]
