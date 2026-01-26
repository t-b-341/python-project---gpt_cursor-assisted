"""
Gameplay systems: movement, collision, spawn, AI.
Each provides update(state, dt). Order is defined in systems.registry.
Telemetry per-frame is in telemetry_system.update_telemetry(gs, dt, app_ctx), called from game.py.
audio_system is used by game.py for init_mixer/sync_from_config and play_sfx/play_music.
"""
from .registry import SIMULATION_SYSTEMS

# Ordered list of systems run each gameplay frame (movement, collision, spawn, AI).
# screens.gameplay uses this; game.py fixed-step loop uses simulation_systems.SIMULATION_SYSTEMS.
# Per-frame telemetry is called from game.py via telemetry_system.update_telemetry.
GAMEPLAY_SYSTEMS = list(SIMULATION_SYSTEMS)
