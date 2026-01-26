"""
Gameplay systems: movement, collision, spawn, AI, telemetry.
Each provides update(state, dt). Orchestrated by screens.gameplay.
audio_system is used by game.py for init_mixer/sync_from_config and play_sfx/play_music.
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
