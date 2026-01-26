"""
Compatibility shim: re-exports from config.projectile_defs (canonical source).
Canonical weapon and projectile definitions live in config.projectile_defs.
Import from here or from config.projectile_defs.
"""
from config.projectile_defs import (
    WEAPON_CONFIGS,
    WEAPON_DISPLAY_COLORS,
    WEAPON_NAMES,
    WEAPON_UNLOCK_ORDER,
)
