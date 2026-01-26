"""
Compatibility shim: re-exports from config.enemy_defs (canonical source).
Canonical definitions live in config.enemy_data; config.enemy_defs re-exports them
and provides get_enemy_def() / clear_enemy_def_cache(). Import from here or from
config.enemy_defs.
"""
from config.enemy_defs import (
    BOSS_TEMPLATE,
    BASE_ENEMIES_PER_WAVE,
    ENEMY_FIRE_RATE_MULTIPLIER,
    ENEMY_HP_CAP,
    ENEMY_HP_SCALE_MULTIPLIER,
    ENEMY_SPAWN_MULTIPLIER,
    ENEMY_SPEED_SCALE_MULTIPLIER,
    ENEMY_TEMPLATES,
    FRIENDLY_AI_TEMPLATES,
    MAX_ENEMIES_PER_WAVE,
    QUEEN_FIXED_HP,
    QUEEN_SPEED_MULTIPLIER,
)
