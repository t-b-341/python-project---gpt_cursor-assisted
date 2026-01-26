"""Centralized game configuration: difficulty, player class, options toggles, feel, and juice.

All scalar config and toggles that are chosen in menus or at startup live here.
Passed via AppContext.config so systems use ctx.config.<field>.

Tuning guide (which values to tweak for feel):
- More floaty vs tight movement: player_base_speed, movement_smoothing (0=instant, 1=full smoothing).
- Faster vs slower weapons: player_base_shoot_cooldown, per-weapon cooldown_multiplier in config_weapons.
- Easier vs harder early waves: base_enemies_per_wave, enemy_spawn_multiplier, difficulty multiplers in constants.
- Feel profiles: use FEEL_PROFILE_CASUAL / FEEL_PROFILE_ARCADE to apply preset overrides (see apply_feel_profile).
"""
from __future__ import annotations

from dataclasses import dataclass

from constants import (
    AIM_MOUSE,
    DIFFICULTY_NORMAL,
    PLAYER_CLASS_BALANCED,
)


# Preset feel profiles for manual testing (casual = floatier, easier; arcade = snappier, harder).
FEEL_PROFILE_CASUAL = "casual"
FEEL_PROFILE_ARCADE = "arcade"
FEEL_PROFILES = {
    FEEL_PROFILE_CASUAL: {
        "player_base_speed": 380,
        "player_base_shoot_cooldown": 0.10,
        "base_enemies_per_wave": 10,
        "enemy_spawn_multiplier": 3.0,
        "movement_smoothing": 0.0,
    },
    FEEL_PROFILE_ARCADE: {
        "player_base_speed": 500,
        "player_base_shoot_cooldown": 0.08,
        "base_enemies_per_wave": 14,
        "enemy_spawn_multiplier": 4.0,
        "movement_smoothing": 0.0,
    },
}


@dataclass
class GameConfig:
    """Difficulty, player class, aim mode, feel tuning, difficulty pacing, juice, and option toggles.

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
    # Audio (used by systems.audio_system)
    sfx_volume: float = 1.0
    music_volume: float = 1.0
    mute_sfx: bool = False
    mute_music: bool = False

    # --- Feel: movement (used when applying class stats and in movement/input) ---
    player_base_speed: int = 300  # Base px/s before class multiplier (e.g. 300 * 1.5 = 450 for balanced)
    player_base_damage: int = 20   # Base damage before class multiplier
    player_base_shoot_cooldown: float = 0.12  # Base seconds between shots before class multiplier
    movement_dead_zone: float = 0.0   # 0–1; for future analog stick support; digital keys ignore
    movement_smoothing: float = 0.0   # 0 = instant (current); >0 = optional smoothing (hook only)

    # --- Feel: difficulty / pacing (spawn_system uses these if set; else uses config_enemies/constants) ---
    base_enemies_per_wave: int = 12
    enemy_spawn_multiplier: float = 3.5

    # --- Juice: visual feedback (durations in seconds; magnitudes 0–1 or alpha 0–255) ---
    enable_damage_flash: bool = True
    damage_flash_duration: float = 0.12
    damage_flash_brightness: float = 1.0   # 1.0 = full white tint when hit
    enable_screen_flash: bool = True
    screen_flash_duration: float = 0.25
    screen_flash_max_alpha: int = 100
    enable_wave_banner: bool = True
    wave_banner_duration: float = 1.5


def apply_feel_profile(config: GameConfig, profile: str) -> None:
    """Apply a preset feel profile (FEEL_PROFILE_CASUAL or FEEL_PROFILE_ARCADE) to config. In-place."""
    presets = FEEL_PROFILES.get(profile)
    if not presets:
        return
    for k, v in presets.items():
        if hasattr(config, k):
            setattr(config, k, v)
