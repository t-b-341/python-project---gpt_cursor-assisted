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
    "triple": {
        "damage_multiplier": 1.0,
        "size_multiplier": 3.0,  # 3x size multiplier
        "speed_multiplier": 1.0,
        "cooldown_multiplier": 1.0,
        "spread_angle_deg": 30.0,  # 30 degrees each side = 60 degree total arc
        "num_projectiles": 3,  # Three beams
        "color": (255, 105, 180),  # Pink
        "explosion_radius": 0.0,
        "max_bounces": 0,
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
}

# ----------------------------
# Weapon Names and Display Colors
# ----------------------------
WEAPON_NAMES = {
    "giant": "GIANT BULLETS",
    "triple": "TRIPLE SHOT",
    "laser": "LASER BEAM",
    "basic": "BASIC FIRE",
}

WEAPON_DISPLAY_COLORS = {
    "giant": (255, 200, 0),
    "triple": (255, 105, 180),
    "laser": (255, 50, 50),
    "basic": (200, 200, 200),
}

# ----------------------------
# Weapon Unlock Order
# ----------------------------
# Weapons unlock in order when bosses are defeated (only giant is dropped)
WEAPON_UNLOCK_ORDER = {
    1: "giant",
    2: "giant",
}

# Note: triple/laser/basic are not dropped; only giant. Key 1 = triple, 2 = giant, 3 = laser.
