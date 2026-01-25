"""
Game constants - immutable configuration values.
These are extracted from game.py for better organization.
"""

# ----------------------------
# File paths
# ----------------------------
CONTROLS_PATH = "controls.json"
HIGH_SCORES_DB = "high_scores.db"

# ----------------------------
# Default controls
# ----------------------------
# Sentinel for "right mouse button" in direct_allies binding (not a pygame key)
MOUSE_BUTTON_RIGHT = -1

DEFAULT_CONTROLS = {
    "move_left": "a",
    "move_right": "d",
    "move_up": "w",
    "move_down": "s",
    "boost": "left shift",
    "slow": "left ctrl",
    "dash": "space",
    "ally_drop": "q",
    "direct_allies": "right mouse",
}

# ----------------------------
# Game state constants
# ----------------------------
STATE_TITLE = "TITLE"
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_CONTINUE = "CONTINUE"
STATE_ENDURANCE = "ENDURANCE"
STATE_GAME_OVER = "GAME_OVER"
STATE_NAME_INPUT = "NAME_INPUT"
STATE_HIGH_SCORES = "HIGH_SCORES"
STATE_VICTORY = "VICTORY"
STATE_MODS = "MODS"
STATE_WAVE_BUILDER = "WAVE_BUILDER"
STATE_CONTROLS = "CONTROLS"

# ----------------------------
# Difficulty constants
# ----------------------------
DIFFICULTY_EASY = "EASY"
DIFFICULTY_NORMAL = "NORMAL"
DIFFICULTY_HARD = "HARD"

difficulty_options = [DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD]

difficulty_multipliers = {
    DIFFICULTY_EASY: {"enemy_hp": 0.7, "enemy_speed": 0.8, "enemy_spawn": 0.8, "pickup_spawn": 1.3},
    DIFFICULTY_NORMAL: {"enemy_hp": 1.0, "enemy_speed": 1.0, "enemy_spawn": 1.0, "pickup_spawn": 1.0},
    DIFFICULTY_HARD: {"enemy_hp": 1.5, "enemy_speed": 1.3, "enemy_spawn": 1.5, "pickup_spawn": 0.7},
}

# ----------------------------
# Aiming mode constants
# ----------------------------
AIM_MOUSE = "MOUSE"
AIM_ARROWS = "ARROWS"

# ----------------------------
# Player class constants
# ----------------------------
PLAYER_CLASS_TANK = "TANK"
PLAYER_CLASS_SPEEDSTER = "SPEEDSTER"
PLAYER_CLASS_SNIPER = "SNIPER"
PLAYER_CLASS_BALANCED = "BALANCED"

player_class_options = [PLAYER_CLASS_BALANCED, PLAYER_CLASS_TANK, PLAYER_CLASS_SPEEDSTER, PLAYER_CLASS_SNIPER]

player_class_stats = {
    PLAYER_CLASS_BALANCED: {"hp_mult": 1.0, "speed_mult": 1.0, "damage_mult": 1.0, "firerate_mult": 1.0},
    PLAYER_CLASS_TANK: {"hp_mult": 2.0, "speed_mult": 0.7, "damage_mult": 1.2, "firerate_mult": 0.8},
    PLAYER_CLASS_SPEEDSTER: {"hp_mult": 0.7, "speed_mult": 1.5, "damage_mult": 0.9, "firerate_mult": 1.3},
    PLAYER_CLASS_SNIPER: {"hp_mult": 0.8, "speed_mult": 0.9, "damage_mult": 1.5, "firerate_mult": 0.7},
}

# ----------------------------
# Level system
# ----------------------------
level_themes = {
    1: {"name": "Forest", "bg_color": (20, 60, 20), "block_color_shift": (0, 0, 0)},
    2: {"name": "Desert", "bg_color": (60, 50, 20), "block_color_shift": (20, 10, -10)},
    3: {"name": "Ice", "bg_color": (20, 40, 60), "block_color_shift": (-20, -10, 20)},
    4: {"name": "Volcano", "bg_color": (60, 20, 20), "block_color_shift": (30, -10, -20)},
    5: {"name": "Void", "bg_color": (10, 10, 20), "block_color_shift": (-30, -30, 10)},
}

# ----------------------------
# Character profile constants
# ----------------------------
character_profile_options = ["Premade Profiles", "Create Custom Profile"]
custom_profile_stats_list = ["HP Multiplier", "Speed Multiplier", "Damage Multiplier", "Fire Rate Multiplier"]
custom_profile_stats_keys = ["hp_mult", "speed_mult", "damage_mult", "firerate_mult"]

# ----------------------------
# UI constants
# ----------------------------
pause_options = ["Continue", "Restart (Wave 1)", "Exit to main menu", "Quit"]
controls_actions = ["move_left", "move_right", "move_up", "move_down", "boost", "slow", "dash", "ally_drop", "direct_allies"]

# ----------------------------
# Weapon constants
# ----------------------------
weapon_selection_options = ["rocket", "bouncing", "laser", "triple", "giant", "basic"]

# Note: WEAPON_KEY_MAP uses pygame constants and must remain in game.py

player_bullet_shapes = ["circle", "square", "diamond"]
player_bullets_color = (10, 200, 200)
player_bullet_size = (8, 8)
player_bullet_speed = 900
player_bullet_damage = 20
player_shoot_cooldown = 0.12

# Laser beam constants
laser_length = 800
laser_damage = 50
laser_cooldown = 0.3

# ----------------------------
# Physics constants
# ----------------------------
LIVES_START = 10

# Dash/jump constants
jump_cooldown = 0.5
jump_speed = 600
jump_duration = 0.15

# Boost/slow constants
boost_meter_max = 100.0
boost_drain_per_s = 45.0
boost_regen_per_s = 25.0
boost_speed_mult = 1.7
slow_speed_mult = 0.45

# Fire rate buff
fire_rate_buff_duration = 10.0
fire_rate_mult = 0.55

# Shield constants (half alt-r shield cooldown)
shield_duration = 5.0
shield_recharge_cooldown = 5.0  # 0.5 * 10.0

# Overshield constants (armor 0.75x)
overshield_max = 37  # 50 * 0.75
overshield_recharge_cooldown = 45.0

# Grenade constants
grenade_cooldown = 2.0
grenade_damage = 1500

# Missile constants
missile_cooldown = 3.0
missile_damage = 800

# Ally drop constants
ally_drop_cooldown = 3.0

# ----------------------------
# Scoring constants
# ----------------------------
SCORE_BASE_POINTS = 100
SCORE_WAVE_MULTIPLIER = 50
SCORE_TIME_MULTIPLIER = 2

# ----------------------------
# Game timing constants
# ----------------------------
POS_SAMPLE_INTERVAL = 0.25
PICKUP_SPAWN_INTERVAL = 7.5

# ----------------------------
# Enemy appearance (all enemies use same color)
# ----------------------------
ENEMY_COLOR = (200, 50, 50)  # Single color for all enemy types

# ----------------------------
# Enemy projectile constants
# ----------------------------
ENEMY_PROJECTILE_SIZE = (10, 10)
ENEMY_PROJECTILE_DAMAGE = 11  # 110% of base 10 damage
ENEMY_PROJECTILES_COLOR = (200, 200, 200)
