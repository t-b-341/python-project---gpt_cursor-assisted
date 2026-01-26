"""Centralized game configuration: difficulty, player class, options toggles.

All scalar config and toggles that are chosen in menus or at startup live here.
Passed via AppContext.config so systems use ctx.config.<field>.
"""
from __future__ import annotations

from dataclasses import dataclass

from constants import (
    AIM_MOUSE,
    DIFFICULTY_NORMAL,
    PLAYER_CLASS_BALANCED,
)


@dataclass
class GameConfig:
    """Difficulty, player class, aim mode, and option toggles.

    Replaces scattered flags on AppContext. Built at startup and when
    the user changes options in menus; attach to ctx.config.
    """
    difficulty: str = DIFFICULTY_NORMAL
    player_class: str = PLAYER_CLASS_BALANCED
    aim_mode: str = AIM_MOUSE
    enable_telemetry: bool = False
    show_metrics: bool = True
    show_hud: bool = True
    show_health_bars: bool = True
    show_player_health_bar: bool = True
    profile_enabled: bool = False
    testing_mode: bool = False
    invulnerability_mode: bool = False
    default_weapon_mode: str = "giant"
