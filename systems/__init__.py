"""
Gameplay systems: movement, collision, spawn, AI, telemetry.
Each provides update(state, dt). Order is defined in systems.registry.
audio_system is used by game.py for init_mixer/sync_from_config and play_sfx/play_music.
"""
from .registry import SIMULATION_SYSTEMS
from .telemetry_system import update as telemetry_update

# Ordered list of systems run each gameplay frame (simulation systems + telemetry).
# screens.gameplay uses this; game.py fixed-step loop uses registry.SIMULATION_SYSTEMS.
GAMEPLAY_SYSTEMS = [*SIMULATION_SYSTEMS, telemetry_update]
