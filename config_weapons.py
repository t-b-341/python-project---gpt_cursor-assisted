"""
Weapon configuration data - weapon properties, multipliers, and visual settings.
These are pure data structures that define weapon behavior and appearance.
"""

# ----------------------------
# Weapon Properties
# ----------------------------
# Base properties for each weapon mode
WEAPON_CONFIGS = {
    "basic": {
        "damage_multiplier": 1.0,
        "size_multiplier": 1.0,
        "speed_multiplier": 1.0,
        "cooldown_multiplier": 1.0,  # Applied to base player_shoot_cooldown
        "spread_angle_deg": 30.0,  # Triple shot pattern (3 beams)
        "num_projectiles": 3,  # Fires 3 beams
        "color": (10, 200, 200),  # Default player_bullets_color
        "explosion_radius": 0.0,
        "max_bounces": 0,
        "is_rocket": False,
    },
    "rocket": {
        "damage_multiplier": 2.5,  # 2.5x damage
        "size_multiplier": 2.5,  # Rockets are bigger
        "speed_multiplier": 1.0,
        "cooldown_multiplier": 3.5,  # Slower fire rate (3.5x cooldown)
        "spread_angle_deg": 0.0,
        "num_projectiles": 1,
        "color": (255, 100, 0),  # Orange
        "explosion_radius": 120.0,  # Base AOE radius (increased from 80px)
        "max_bounces": 0,
        "is_rocket": True,
    },
    "triple": {
        "damage_multiplier": 1.0,
        "size_multiplier": 3.0,  # 3x size multiplier
        "speed_multiplier": 1.0,
        "cooldown_multiplier": 1.0,
        "spread_angle_deg": 30.0,  # 30 degrees each side = 60 degree total arc
        "num_projectiles": 3,  # Three beams
        "color": (200, 100, 255),  # Purple
        "explosion_radius": 0.0,
        "max_bounces": 0,
        "is_rocket": False,
    },
    "bouncing": {
        "damage_multiplier": 1.0,
        "size_multiplier": 2.0,  # Twice the size
        "speed_multiplier": 1.0,
        "cooldown_multiplier": 1.0,
        "spread_angle_deg": 0.0,
        "num_projectiles": 1,
        "color": (255, 165, 0),  # Orange
        "explosion_radius": 0.0,
        "max_bounces": 10,  # Max bounces off walls
        "is_rocket": False,
    },
    "giant": {
        "damage_multiplier": 1.0,
        "size_multiplier": 10.0,  # 10x size multiplier
        "speed_multiplier": 1.0,
        "cooldown_multiplier": 1.0,
        "spread_angle_deg": 0.0,
        "num_projectiles": 1,
        "color": (10, 200, 200),  # Default player_bullets_color
        "explosion_radius": 0.0,
        "max_bounces": 0,
        "is_rocket": False,
    },
    "laser": {
        "damage_multiplier": 1.0,  # Damage per frame (laser_damage constant)
        "size_multiplier": 1.0,  # Not applicable (beam weapon)
        "speed_multiplier": 1.0,  # Not applicable (beam weapon)
        "cooldown_multiplier": 1.0,  # Uses laser_cooldown constant
        "spread_angle_deg": 0.0,
        "num_projectiles": 0,  # Beam weapon, not projectiles
        "color": (255, 50, 50),  # Red
        "explosion_radius": 0.0,
        "max_bounces": 0,
        "is_rocket": False,
    },
    "wave_beam": {
        "damage_multiplier": 1.0,  # Damage per frame (wave_beam_damage constant)
        "size_multiplier": 1.0,  # Not applicable (beam weapon)
        "speed_multiplier": 1.0,  # Not applicable (beam weapon)
        "cooldown_multiplier": 1.0,  # Uses wave_beam_cooldown constant
        "spread_angle_deg": 0.0,
        "num_projectiles": 0,  # Beam weapon, not projectiles
        "color": (50, 255, 50),  # Lime green
        "explosion_radius": 0.0,
        "max_bounces": 0,
        "is_rocket": False,
    },
}

# ----------------------------
# Weapon Names and Display Colors
# ----------------------------
WEAPON_NAMES = {
    "giant": "GIANT BULLETS",
    "triple": "TRIPLE SHOT",
    "bouncing": "BOUNCING BULLETS",
    "rocket": "ROCKET LAUNCHER",
    "laser": "LASER BEAM",
    "basic": "BASIC FIRE",
    "wave_beam": "WAVE BEAM",
}

WEAPON_DISPLAY_COLORS = {
    "giant": (255, 200, 0),
    "triple": (100, 200, 255),
    "bouncing": (100, 255, 100),
    "rocket": (255, 100, 0),
    "laser": (255, 50, 50),
    "basic": (200, 200, 200),
    "wave_beam": (50, 255, 50),
}

# ----------------------------
# Weapon Unlock Order
# ----------------------------
# Weapons unlock in order when bosses are defeated
WEAPON_UNLOCK_ORDER = {
    1: "rocket",
    2: "triple",
    3: "wave_beam",
    4: "giant",
}

# Note: "basic" is available from start, "laser" and "bouncing" are pickup-only
