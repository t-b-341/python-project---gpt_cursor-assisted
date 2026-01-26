"""
Data-driven projectile definitions. Unified lookup by type_id with caching.

Each definition provides: type_id, speed, damage, lifetime, sprite_id (optional),
flags (e.g. "piercing", "explosive"). Player defs also carry weapon-style fields
(size, color, size_multiplier, speed_multiplier, damage_multiplier, num_projectiles,
spread_angle_deg, explosion_radius, max_bounces, is_rocket) so spawn logic can use
one canonical source. Enemy defs use constants for default size/damage/color.
"""
from __future__ import annotations

from typing import Any, Optional

_PROJECTILE_DEF_CACHE: dict[str, Optional[dict[str, Any]]] = {}


def get_projectile_def(type_id: str) -> Optional[dict[str, Any]]:
    """Return the projectile definition for type_id, or None if unknown. Results are cached."""
    if type_id in _PROJECTILE_DEF_CACHE:
        return _PROJECTILE_DEF_CACHE[type_id]

    build = _BUILDERS.get(type_id)
    if build is None:
        _PROJECTILE_DEF_CACHE[type_id] = None
        return None

    out = build()
    _PROJECTILE_DEF_CACHE[type_id] = out
    return out


def _build_player_def(weapon_key: str) -> dict[str, Any]:
    from constants import (
        player_bullet_damage,
        player_bullet_size,
        player_bullet_speed,
        player_bullets_color,
    )
    from config_weapons import WEAPON_CONFIGS

    cfg = WEAPON_CONFIGS.get(weapon_key, WEAPON_CONFIGS["basic"])
    return {
        "type_id": f"player_{weapon_key}",
        "speed": player_bullet_speed * cfg["speed_multiplier"],
        "damage": int(player_bullet_damage * cfg["damage_multiplier"]),
        "lifetime": None,
        "sprite_id": None,
        "flags": frozenset(),
        "size": tuple(player_bullet_size),
        "color": cfg.get("color", player_bullets_color),
        "damage_multiplier": cfg["damage_multiplier"],
        "size_multiplier": cfg["size_multiplier"],
        "speed_multiplier": cfg["speed_multiplier"],
        "num_projectiles": cfg["num_projectiles"],
        "spread_angle_deg": cfg["spread_angle_deg"],
        "explosion_radius": cfg["explosion_radius"],
        "max_bounces": cfg["max_bounces"],
        "is_rocket": cfg["is_rocket"],
    }


def _build_enemy_default() -> dict[str, Any]:
    from constants import (
        ENEMY_PROJECTILE_DAMAGE,
        ENEMY_PROJECTILES_COLOR,
        ENEMY_PROJECTILE_SIZE,
    )

    return {
        "type_id": "enemy_default",
        "speed": 0,  # Per-enemy; this is fallback only
        "damage": ENEMY_PROJECTILE_DAMAGE,
        "lifetime": None,
        "sprite_id": None,
        "flags": frozenset(),
        "size": tuple(ENEMY_PROJECTILE_SIZE),
        "color": ENEMY_PROJECTILES_COLOR,
    }


_BUILDERS: dict[str, Any] = {
    "player_basic": lambda: _build_player_def("basic"),
    "player_triple": lambda: _build_player_def("triple"),
    "player_giant": lambda: _build_player_def("giant"),
    "enemy_default": _build_enemy_default,
}


def clear_projectile_def_cache() -> None:
    """Clear the cache (e.g. for tests or hot-reload)."""
    _PROJECTILE_DEF_CACHE.clear()
