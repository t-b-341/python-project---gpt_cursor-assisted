#FEATURES TO ADD
#--------------------------------------------------------
#change player bullet color
#change enemy bullet colors
#enemy movement
#enemy respawn timer
#survival timer, waves, multiple levels
#movement direction overwrites to most recent move direction
#player path prediction
#different shapes for shots (circle, squares, etc., like 2hu)
#--------------------------------------------------------
#add boost mechanic using shift, and slow down mechanic using ctrl
#add a control mapping system, so the player can map the keys to the actions
#add a pickup for boost
#add a pickup for more firing speed
#add a pickup for enemies spawn more often, that enemies can pick up, and that you have to shoot to destroy the pickup
#--------------------------------------------------------
#make pickups bigger, add in another pickup that increases the player's max health 
#add a pickup that increases the player's speed
#add a pickup that increases the player's firing rate
#add a pickup that increases the player's bullet size
#add a pickup that increases the player's bullet speed
#add a pickup that increases the player's bullet damage
#add a pickup that increases the player's bullet knockback
#add a pickup that increases the player's bullet penetration
#add a pickup that increases the player's bullet explosion radius
#randomize the pickups, so that the player never knows what they will get
#--------------------------------------------------------
#make pickup that increases the shot size to 10x regular size, and another pickup that increase the shot beams to 3 beams
#--------------------------------------------------------
#add a pickup that bounces shots around on the walls
#add an enemy that shoots shots that bounce around on the walls
#stack pickups so that the player can get a combo of pickups
#add in more squares and rectangles that can be moved around, but have health bars that enemies can shoot at to destroy them
#--------------------------------------------------------
#add a pickup timer, and effects around the pickup, and an effect when the player picks up the pickup
#add a pickup that functions like a rocket launcher with a longer rate of fire, but the shots do more damage with an area of effect
#--------------------------------------------------------
#add a map to key 1 for the basic fire, then key 2 for the rocket launcher, then key 3 for the triple shot, then key 4 for the bouncing bullets, then key 5 for the giant bullets
#--------------------------------------------------------
#make the map bigger, and add in more geometry, with areas of health recovery, and overshields (extra health bar that can be used to block damage)
#--------------------------------------------------------
#add a pickup that increases the player's overshield
#FUTURE
#SMALL FEATURES TO ADD; integrate C++ for the physics and collision detection?
#multiple levels, with different themes and enemies, and pickups, and powerups
#more weapons; start with basic weapons (weapon 1 = peashooter, weapon 2 = rocket launcher, weapon 3 = triple shot, weapon 4 = bouncing bullets, weapon 5 = giant bullets)
#pick up weapons as levels progress, and as the player kills enemies, then enemies drop the weapons they use (so there's an enemy that does peashooters, and another that does rocket launchers, etc.)
#final boss, with a unique weapon that the player has to defeat (combo of all weapons), multiple phases, and a unique weapon for each phase
#add a special pickup that adds a laser beam weapon that the player can use to destroy enemies from a distance, that's a long ray, but doesn't cut through solid blocks, but breaks temporary barriers
#continue? after game is done, to add an endurance mode for postgame
#add a score counter and survival wave amount/time survived
#add a difficulty selector, so the player can choose the difficulty of the game, which impacts enemy spawns (more, harder enemies, fewer pickups?)
#by end of game it's a bullet hell with the player having all their tools
#add space bar to jump in direction of movement?
#--------------------------------------------------------
#add friendly AI, about 1-2 per every 3-5 enemies that move independently, and attack the enemies, and help the player, with a health bar and various spawn classes and behavior patterns
#--------------------------------------------------------
#make the friendly AI move, and make the enemy AI focus on the player, and the friendly, and move in response to the player and the friendly's bullets, and position
#--------------------------------------------------------
#make weapons drop in the center of the screen, and the player has to pick them up to use them, adding one with each level completed
#make each level 3 waves, increasing in difficulty, with the last wave being the boss
#make 3 different levels, with the final level being a boss with 10,000 health
#--------------------------------------------------------
#make the rockets shot size bigger
#--------------------------------------------------------
#add a shield for use with left alt key that lasts 2 seconds, and takes 10-15 seconds to recharge
#--------------------------------------------------------
#make the player turn red while the shield is active, and a text displays in the hud SHIELD ACTIVU (spelled like that)
#--------------------------------------------------------
#Game; add enemy with shield that is a line across the front of the enemy, which the player must flank to damage; 
#add one shield enemy with reflective shield, which takes damage done to the shield and fires back at the player; enemy does not fire, enemy turns at speed player can flank 
#Game; controls; add in arrows for shooting, and an option to choose between mouse and arrow keys
#Game; classes to play as, custom mod setting to change enemy spawn amount, custom wave builder
#;enable or disable stats and any UI elements like health; take away health bars for destructible blocks, add in texture that shows block is breakable, give texture to unbreakable blocks; 
#clean up UI
#Game.py; change aiming mechanic
#Arrow keys: Add it as an option in the menu to use either mouse or arrow aiming
#Game.py; large shapes that bounce around the map, destroying what's in their path, and the enemies avoid them
#--------------------------------------------------------
#add a health bar for the player
#make the metrics optional in the menu
#--------------------------------------------------------
#put the health bar on the bottom of the screen
#--------------------------------------------------------
#start game fullscreen
#--------------------------------------------------------
#in telemetry.py, track the player's position and velocity, and the enemy's position and velocity, and which enemy types spawned that wave; do the wave's tracking for the enemies as its own table
#--------------------------------------------------------
#add more enemies, and friendly ai, and give the ai more health (50-100), with their bar being full and green at the beginning of the waves
#--------------------------------------------------------
#add in more moveable blocks
#add in moveable blocks that can be destroyed by the player's, and enemy's bullets
#--------------------------------------------------------
#make only one health area, and have it move around the map, and the player has to move to it to heal
#add a pickup that increases the player's health regeneration rate
#add in more geometry (moveable blocks, unmovable blocks, destructible blocks, indestructible blocks) to fill up the map more
#once there are 5 enemies remaining, have them move towards the player, and the player has to move to avoid them, and the player has to shoot them to kill them
#--------------------------------------------------------
#add in trapezoids that hang off the top, bottom, and sides of the screen, that are unmovable, and indestructible
#--------------------------------------------------------
#let the enemies move the blocks out of the way as well, to chase the player
#--------------------------------------------------------








import math
import warnings

# Suppress pygame's pkg_resources deprecation warning
# This is a pygame internal issue, not our code
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
import random
import json
import os

import pygame
from datetime import datetime, timezone

# Try to import C extension for performance, fallback to Python if not available
# Note: game_physics module is built from game_physics.c - see BUILD_INSTRUCTIONS.md
try:
    import game_physics  # type: ignore
    USE_C_EXTENSION = True
except ImportError:
    USE_C_EXTENSION = False
    print("Note: C extension not available, using Python fallback (slower)")

from telemetry import (
    Telemetry,
    EnemySpawnEvent,
    PlayerPosEvent,
    ShotEvent,
    EnemyHitEvent,
    PlayerDamageEvent,
    PlayerDeathEvent,
    WaveEvent,
    WaveEnemyTypeEvent,
    EnemyPositionEvent,
    PlayerVelocityEvent,
    BulletMetadataEvent,
    PlayerActionEvent,
    ZoneVisitEvent,
    FriendlyAISpawnEvent,
    FriendlyAIPositionEvent,
    FriendlyAIShotEvent,
    FriendlyAIDeathEvent,
)

pygame.init()

# ----------------------------
# Controls (remappable)
# ----------------------------
CONTROLS_PATH = "controls.json"
DEFAULT_CONTROLS = {
    "move_left": "a",
    "move_right": "d",
    "move_up": "w",
    "move_down": "s",
    "boost": "left shift",
    "slow": "left ctrl",
}


def _key_name_to_code(name: str) -> int:
    name = (name or "").lower().strip()
    try:
        return pygame.key.key_code(name)
    except Exception:
        return pygame.K_UNKNOWN


def load_controls() -> dict[str, int]:
    data = {}
    if os.path.exists(CONTROLS_PATH):
        try:
            with open(CONTROLS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
        except Exception:
            data = {}

    merged = {**DEFAULT_CONTROLS, **{k: v for k, v in data.items() if isinstance(v, str)}}
    return {action: _key_name_to_code(key_name) for action, key_name in merged.items()}


def save_controls(controls: dict[str, int]) -> None:
    # Persist as human-readable key names so players can edit the file too
    out: dict[str, str] = {}
    for action, key_code in controls.items():
        try:
            out[action] = pygame.key.name(key_code)
        except Exception:
            out[action] = "unknown"
    with open(CONTROLS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)


controls = load_controls()

# ----------------------------
# Window / timing
# ----------------------------
# Start in fullscreen mode
pygame.display.init()
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Mouse Aim Shooter + Telemetry (SQLite)")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 56)

# ----------------------------
# Telemetry
# ----------------------------
telemetry = Telemetry(db_path="game_telemetry.db", flush_interval_s=0.5, max_buffer=700)
run_started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

# ----------------------------
# Game state
# ----------------------------
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_CONTINUE = "CONTINUE"
STATE_ENDURANCE = "ENDURANCE"
STATE_GAME_OVER = "GAME_OVER"
STATE_VICTORY = "VICTORY"  # Game completed - all levels cleared
STATE_MODS = "MODS"  # Mod settings menu
STATE_WAVE_BUILDER = "WAVE_BUILDER"  # Custom wave builder

state = STATE_MENU
menu_section = 0  # 0 = difficulty, 1 = aiming, 2 = class, 3 = options, 4 = start
ui_show_metrics_selected = 0  # 0 = Show, 1 = Hide

# Level system - 3 levels, each with 3 waves (boss on wave 3)
current_level = 1
max_level = 3
wave_in_level = 1  # Track which wave within current level (1, 2, or 3)
level_themes = {
    1: {"name": "Forest", "bg_color": (20, 60, 20), "block_color_shift": (0, 0, 0)},
    2: {"name": "Desert", "bg_color": (60, 50, 20), "block_color_shift": (20, 10, -10)},
    3: {"name": "Ice", "bg_color": (20, 40, 60), "block_color_shift": (-20, -10, 20)},
    4: {"name": "Volcano", "bg_color": (60, 20, 20), "block_color_shift": (30, -10, -20)},
    5: {"name": "Void", "bg_color": (10, 10, 20), "block_color_shift": (-30, -30, 10)},
}

# Difficulty settings
DIFFICULTY_EASY = "EASY"
DIFFICULTY_NORMAL = "NORMAL"
DIFFICULTY_HARD = "HARD"
difficulty = DIFFICULTY_NORMAL
difficulty_selected = 1  # 0 = Easy, 1 = Normal, 2 = Hard
difficulty_options = [DIFFICULTY_EASY, DIFFICULTY_NORMAL, DIFFICULTY_HARD]

# Aiming mode selection
AIM_MOUSE = "MOUSE"
AIM_ARROWS = "ARROWS"
aiming_mode = AIM_MOUSE
aiming_mode_selected = 0  # 0 = Mouse, 1 = Arrows

# Player classes
PLAYER_CLASS_TANK = "TANK"
PLAYER_CLASS_SPEEDSTER = "SPEEDSTER"
PLAYER_CLASS_SNIPER = "SNIPER"
PLAYER_CLASS_BALANCED = "BALANCED"
player_class = PLAYER_CLASS_BALANCED
player_class_selected = 0  # 0 = Balanced, 1 = Tank, 2 = Speedster, 3 = Sniper
player_class_options = [PLAYER_CLASS_BALANCED, PLAYER_CLASS_TANK, PLAYER_CLASS_SPEEDSTER, PLAYER_CLASS_SNIPER]

# Mod settings
mod_enemy_spawn_multiplier = 1.0  # Custom enemy spawn multiplier
mod_custom_waves_enabled = False
custom_waves: list[dict] = []  # Custom wave definitions

# UI customization settings
ui_show_health_bars = True
ui_show_stats = True
ui_show_all_ui = True
ui_show_block_health_bars = False  # Health bars for destructible blocks
ui_show_player_health_bar = True  # Health bar above player character
ui_show_metrics = True  # Show metrics/stats in HUD

# Alternative aiming mechanics
aiming_mechanic = "mouse"  # "mouse", "lockon", "predictive", "directional", "hybrid"

# Difficulty multipliers
difficulty_multipliers = {
    DIFFICULTY_EASY: {"enemy_hp": 0.7, "enemy_speed": 0.8, "enemy_spawn": 0.8, "pickup_spawn": 1.3},
    DIFFICULTY_NORMAL: {"enemy_hp": 1.0, "enemy_speed": 1.0, "enemy_spawn": 1.0, "pickup_spawn": 1.0},
    DIFFICULTY_HARD: {"enemy_hp": 1.5, "enemy_speed": 1.3, "enemy_spawn": 1.5, "pickup_spawn": 0.7},
}

pause_options = ["Continue", "Quit"]
pause_selected = 0
continue_blink_t = 0.0

# Controls menu state
STATE_CONTROLS = "CONTROLS"
controls_actions = ["move_left", "move_right", "move_up", "move_down", "boost", "slow"]
controls_selected = 0
controls_rebinding = False

# ----------------------------
# Player
# ----------------------------
player = pygame.Rect((WIDTH - 25) // 2, (HEIGHT - 25) // 2, 25, 25)
player_speed = 300  # px/s (base speed, modified by class)
player_max_hp = 100  # base HP (modified by class)
player_hp = player_max_hp

# Player class stat modifiers
player_class_stats = {
    PLAYER_CLASS_BALANCED: {"hp_mult": 1.0, "speed_mult": 1.0, "damage_mult": 1.0, "firerate_mult": 1.0},
    PLAYER_CLASS_TANK: {"hp_mult": 2.0, "speed_mult": 0.7, "damage_mult": 1.2, "firerate_mult": 0.8},
    PLAYER_CLASS_SPEEDSTER: {"hp_mult": 0.7, "speed_mult": 1.5, "damage_mult": 0.9, "firerate_mult": 1.3},
    PLAYER_CLASS_SNIPER: {"hp_mult": 0.8, "speed_mult": 0.9, "damage_mult": 1.5, "firerate_mult": 0.7},
}
overshield_max = 50  # Maximum overshield capacity
overshield = 0  # Current overshield amount
pygame.mouse.set_visible(True)

LIVES_START = 10
lives = LIVES_START

# Track most recent movement keys so latest press wins on conflicts
last_horizontal_key = None  # keycode of current "latest" horizontal key
last_vertical_key = None  # keycode of current "latest" vertical key
last_move_velocity = pygame.Vector2(0, 0)

# Jump/Dash mechanic (space bar)
jump_cooldown = 0.5  # seconds between jumps
jump_cooldown_timer = 0.0
jump_velocity = pygame.Vector2(0, 0)  # Current jump velocity
jump_speed = 600  # pixels per second
jump_duration = 0.15  # seconds
jump_timer = 0.0
is_jumping = False

# Boost / slow
previous_boost_state = False  # Track for telemetry
previous_slow_state = False  # Track for telemetry

boost_meter_max = 100.0
boost_meter = boost_meter_max
boost_drain_per_s = 45.0
boost_regen_per_s = 25.0
boost_speed_mult = 1.7
slow_speed_mult = 0.45

# Fire-rate pickup buff
fire_rate_buff_t = 0.0
fire_rate_buff_duration = 10.0
fire_rate_mult = 0.55  # reduces cooldown while active

# Shield system (Left Alt key)
shield_active = False
shield_duration = 2.0  # Shield lasts 2 seconds
shield_duration_remaining = 0.0
shield_cooldown = random.uniform(10.0, 15.0)  # 10-15 seconds cooldown
shield_cooldown_remaining = 0.0

# Permanent player stat multipliers (from pickups)
player_stat_multipliers = {
    "speed": 1.0,
    "firerate": 1.0,  # permanent firerate boost (stacks with temporary buff)
    "bullet_size": 1.0,
    "bullet_speed": 1.0,
    "bullet_damage": 1.0,
    "bullet_knockback": 1.0,
    "bullet_penetration": 0,  # number of enemies bullet can pierce through
    "bullet_explosion_radius": 0.0,  # explosion radius in pixels (0 = no explosion)
}

# Weapon mode system (keys 1-6 to switch)
# "basic" = normal bullets, "rocket" = rocket launcher, "triple" = triple shot,
# "bouncing" = bouncing bullets, "giant" = giant bullets, "laser" = laser beam
current_weapon_mode = "basic"
previous_weapon_mode = "basic"  # Track for telemetry
unlocked_weapons: set[str] = {"basic"}  # Weapons player has unlocked (starts with basic)

# Laser beam system
laser_beams: list[dict] = []  # List of active laser beams
laser_length = 800  # Maximum laser length in pixels
laser_damage = 50  # Damage per frame while on target
laser_cooldown = 0.3  # Cooldown between laser shots
laser_time_since_shot = 999.0

# ----------------------------
# World blocks
# ----------------------------
blocks = [
    {"rect": pygame.Rect(100, 100, 100, 100), "color": (80, 140, 220), "hp": None, "max_hp": None},  # indestructible
    {"rect": pygame.Rect(180, 180, 60, 30), "color": (30, 30, 30), "hp": None, "max_hp": None},  # indestructible
    {"rect": pygame.Rect(550, 420, 70, 70), "color": (200, 200, 200), "hp": None, "max_hp": None},  # indestructible
    {"rect": pygame.Rect(700, 420, 70, 70), "color": (220, 200, 10), "hp": None, "max_hp": None},  # indestructible
    # Add more moveable blocks
    {"rect": pygame.Rect(250, 300, 80, 80), "color": (120, 160, 200), "hp": None, "max_hp": None},  # indestructible, moveable
    {"rect": pygame.Rect(900, 200, 60, 60), "color": (180, 180, 200), "hp": None, "max_hp": None},  # indestructible, moveable
    {"rect": pygame.Rect(600, 700, 90, 50), "color": (200, 180, 140), "hp": None, "max_hp": None},  # indestructible, moveable
    {"rect": pygame.Rect(1150, 400, 70, 70), "color": (160, 200, 160), "hp": None, "max_hp": None},  # indestructible, moveable
    {"rect": pygame.Rect(500, 900, 50, 50), "color": (220, 160, 120), "hp": None, "max_hp": None},  # indestructible, moveable
    {"rect": pygame.Rect(1350, 800, 80, 40), "color": (140, 140, 220), "hp": None, "max_hp": None},  # indestructible, moveable
]

# Add more destructible blocks (scattered across larger map)
destructible_blocks = [
    {"rect": pygame.Rect(300, 200, 80, 80), "color": (150, 100, 200), "hp": 50, "max_hp": 50, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(450, 300, 60, 60), "color": (100, 200, 150), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(200, 500, 90, 50), "color": (200, 150, 100), "hp": 60, "max_hp": 60, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(750, 600, 70, 70), "color": (150, 150, 200), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(150, 700, 100, 40), "color": (200, 200, 100), "hp": 55, "max_hp": 55, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1100, 300, 90, 90), "color": (180, 120, 180), "hp": 55, "max_hp": 55, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1300, 500, 70, 70), "color": (120, 180, 120), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1000, 800, 80, 60), "color": (200, 120, 100), "hp": 50, "max_hp": 50, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(400, 1000, 100, 50), "color": (150, 150, 220), "hp": 60, "max_hp": 60, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(800, 1200, 70, 70), "color": (220, 200, 120), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1200, 1000, 90, 40), "color": (200, 150, 200), "hp": 55, "max_hp": 55, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1400, 700, 60, 60), "color": (100, 200, 200), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0},
]

# Moveable destructible blocks (can be pushed by player AND destroyed by player/enemy bullets)
moveable_destructible_blocks = [
    {"rect": pygame.Rect(350, 400, 70, 70), "color": (200, 100, 100), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(850, 500, 60, 60), "color": (100, 200, 100), "hp": 35, "max_hp": 35, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(650, 300, 80, 50), "color": (200, 150, 100), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(1050, 600, 60, 60), "color": (150, 100, 200), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(450, 800, 70, 50), "color": (200, 180, 120), "hp": 50, "max_hp": 50, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(1250, 900, 80, 40), "color": (100, 150, 200), "hp": 35, "max_hp": 35, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(550, 1100, 60, 60), "color": (180, 200, 100), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(950, 1100, 70, 50), "color": (200, 120, 150), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    # Add more moveable destructible blocks to fill the map
    {"rect": pygame.Rect(200, 600, 60, 60), "color": (150, 150, 200), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(300, 800, 70, 50), "color": (200, 100, 150), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(700, 900, 60, 60), "color": (100, 200, 150), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(1150, 700, 70, 50), "color": (200, 150, 100), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(1350, 400, 60, 60), "color": (150, 200, 100), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0, "is_moveable": True},
    {"rect": pygame.Rect(500, 500, 70, 50), "color": (200, 100, 200), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0, "is_moveable": True},
]

# Add more indestructible blocks to fill the map
blocks.extend([
    {"rect": pygame.Rect(320, 320, 80, 80), "color": (90, 130, 210), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(480, 480, 60, 60), "color": (40, 40, 50), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(720, 320, 70, 70), "color": (210, 210, 220), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(880, 480, 60, 60), "color": (230, 210, 20), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(1120, 320, 80, 50), "color": (130, 170, 210), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(1280, 480, 60, 60), "color": (190, 190, 210), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(160, 640, 70, 70), "color": (200, 190, 150), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(320, 800, 60, 60), "color": (170, 210, 170), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(480, 960, 80, 50), "color": (220, 170, 130), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(640, 1120, 70, 70), "color": (140, 140, 230), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(800, 1280, 60, 60), "color": (230, 210, 130), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(960, 1120, 80, 50), "color": (200, 160, 210), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(1120, 960, 70, 70), "color": (100, 210, 210), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(1280, 800, 60, 60), "color": (210, 200, 120), "hp": None, "max_hp": None},
    {"rect": pygame.Rect(1440, 640, 80, 50), "color": (150, 150, 220), "hp": None, "max_hp": None},
])

# Trapezoids hanging off screen edges (unmovable, indestructible)
# These use polygon points for drawing but bounding rects for collision
trapezoid_blocks = [
    # Top edge - trapezoid hanging down (wider at top, narrower at bottom)
    {
        "points": [(0, -60), (WIDTH, -60), (WIDTH - 100, 80), (100, 80)],
        "bounding_rect": pygame.Rect(0, -60, WIDTH, 140),
        "color": (100, 120, 180),
        "hp": None,
        "max_hp": None,
        "side": "top"
    },
    # Bottom edge - trapezoid hanging up (wider at bottom, narrower at top)
    {
        "points": [(100, HEIGHT - 80), (WIDTH - 100, HEIGHT - 80), (WIDTH, HEIGHT + 60), (0, HEIGHT + 60)],
        "bounding_rect": pygame.Rect(0, HEIGHT - 80, WIDTH, 140),
        "color": (120, 100, 160),
        "hp": None,
        "max_hp": None,
        "side": "bottom"
    },
    # Left edge - trapezoid hanging right (wider at left, narrower at right)
    {
        "points": [(-60, 0), (80, 100), (80, HEIGHT - 100), (-60, HEIGHT)],
        "bounding_rect": pygame.Rect(-60, 0, 140, HEIGHT),
        "color": (140, 110, 170),
        "hp": None,
        "max_hp": None,
        "side": "left"
    },
    # Right edge - trapezoid hanging left (wider at right, narrower at left)
    {
        "points": [(WIDTH - 80, 100), (WIDTH + 60, 0), (WIDTH + 60, HEIGHT), (WIDTH - 80, HEIGHT - 100)],
        "bounding_rect": pygame.Rect(WIDTH - 80, 0, 140, HEIGHT),
        "color": (110, 130, 190),
        "hp": None,
        "max_hp": None,
        "side": "right"
    },
]

# Add more destructible blocks to fill the map
destructible_blocks.extend([
    {"rect": pygame.Rect(240, 360, 70, 70), "color": (160, 110, 210), "hp": 50, "max_hp": 50, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(400, 520, 60, 60), "color": (110, 210, 160), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(560, 680, 80, 50), "color": (210, 160, 110), "hp": 60, "max_hp": 60, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(720, 840, 70, 70), "color": (160, 160, 210), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(880, 1000, 60, 60), "color": (210, 210, 110), "hp": 55, "max_hp": 55, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1040, 1160, 80, 50), "color": (190, 130, 190), "hp": 55, "max_hp": 55, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1200, 1320, 70, 70), "color": (130, 190, 130), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1360, 1160, 60, 60), "color": (210, 130, 110), "hp": 50, "max_hp": 50, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1520, 1000, 80, 50), "color": (160, 160, 230), "hp": 60, "max_hp": 60, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1680, 840, 70, 70), "color": (230, 210, 130), "hp": 45, "max_hp": 45, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(1840, 680, 60, 60), "color": (200, 160, 210), "hp": 55, "max_hp": 55, "is_destructible": True, "crack_level": 0},
    {"rect": pygame.Rect(200, 840, 80, 50), "color": (110, 210, 210), "hp": 40, "max_hp": 40, "is_destructible": True, "crack_level": 0},
])

# Single moving health recovery zone
moving_health_zone = {
    "rect": pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 75, 150, 150),
    "heal_rate": 20.0,
    "color": (100, 255, 100, 80),
    "name": "Moving Healing Zone",
    "zone_id": 1,
    "velocity": 30.0,  # Movement speed in pixels per second (scalar)
    "target": None,  # Target position to move towards
}

# Track which zones player is currently in (for telemetry)
player_current_zones = set()  # Set of zone names player is in

# Player health regeneration rate (can be increased by pickups)
player_health_regen_rate = 0.0  # Base regeneration rate (0 = no regen)

# Bouncing destructor shapes (line 79)
destructor_shapes: list[dict] = []  # Large shapes that bounce around destroying things

# ----------------------------
# Player bullets
# ----------------------------
player_bullets: list[dict] = []
player_bullet_speed = 900
player_bullet_size = (8, 8)
player_bullet_damage = 20
player_shoot_cooldown = 0.12
player_time_since_shot = 999.0
player_bullets_color = (10, 200, 200)
player_bullet_shapes = ["circle", "square", "diamond"]
player_bullet_shape_index = 0

# ----------------------------
# Enemy templates + cloning
# ----------------------------
enemy_templates: list[dict] = [
    {
        "type": "grunt",
        "rect": pygame.Rect(120, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "projectile_speed": 320,
        "projectile_color": (180, 220, 255),
        "projectile_shape": "square",
        "speed": 90,
    },
    {
        "type": "heavy",
        "rect": pygame.Rect(650, 120, 32, 32),
        "color": (220, 120, 80),
        "hp": 80,
        "max_hp": 80,
        "shoot_cooldown": 1.2,
        "projectile_speed": 280,
        "projectile_color": (255, 190, 120),
        "projectile_shape": "circle",
        "speed": 70,
    },
    {
        "type": "stinky",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "projectile_speed": 320,
        "projectile_color": (180, 220, 255),
        "projectile_shape": "diamond",
        "speed": 110,
    },
    {
        "type": "baka",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (100, 80, 80),
        "hp": 400,
        "max_hp": 400,
        "shoot_cooldown": 0.1,
        "projectile_speed": 500,
        "projectile_color": (255, 120, 180),
        "projectile_shape": "square",
        "speed": 150,
    },
    {
        "type": "neko neko desu",
        "rect": pygame.Rect(100, 450, 28, 28),
        "color": (100, 80, 0),
        "hp": 20,
        "max_hp": 20,
        "shoot_cooldown": 0.01,
        "projectile_speed": 500,
        "projectile_color": (200, 255, 140),
        "projectile_shape": "circle",
        "speed": 160,
    },
    {
        "type": "BIG NEKU",
        "rect": pygame.Rect(400, 450, 28, 28),
        "color": (100, 200, 0),
        "hp": 1000,
        "max_hp": 1000,
        "shoot_cooldown": 1,
        "projectile_speed": 700,
        "projectile_color": (160, 200, 255),
        "projectile_shape": "diamond",
        "speed": 60,
    },
    {
        "type": "bouncer",
        "rect": pygame.Rect(500, 500, 30, 30),
        "color": (255, 100, 100),
        "hp": 70,
        "max_hp": 70,
        "shoot_cooldown": 1.5,
        "projectile_speed": 350,
        "projectile_color": (255, 150, 150),
        "projectile_shape": "square",
        "speed": 85,
        "bouncing_projectiles": True,  # shoots bouncing projectiles
    },
    {
        "type": "shielded",
        "rect": pygame.Rect(300, 300, 32, 32),
        "color": (100, 150, 200),
        "hp": 100,
        "max_hp": 100,
        "shoot_cooldown": 1.0,
        "projectile_speed": 300,
        "projectile_color": (150, 200, 255),
        "projectile_shape": "circle",
        "speed": 60,
        "has_shield": True,  # Has directional shield
        "shield_angle": 0.0,  # Direction shield is facing (radians)
        "shield_length": 50,  # Length of shield line
    },
    {
        "type": "reflector",
        "rect": pygame.Rect(400, 400, 36, 36),
        "color": (200, 150, 100),
        "hp": 150,
        "max_hp": 150,
        "shoot_cooldown": 999.0,  # Doesn't shoot
        "projectile_speed": 0,
        "projectile_color": (255, 200, 100),
        "projectile_shape": "circle",
        "speed": 40,  # Slow turn speed
        "has_reflective_shield": True,  # Has reflective shield
        "shield_angle": 0.0,  # Direction shield is facing (radians)
        "shield_length": 60,  # Length of shield
        "shield_hp": 0,  # Damage absorbed by shield (fires back)
        "turn_speed": 0.5,  # Radians per second turn speed
    },

]

# Boss enemy template (spawned at specific waves)
boss_template = {
    "type": "FINAL_BOSS",
    "rect": pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100),
    "color": (255, 0, 0),
    "hp": 5000,
    "max_hp": 5000,
    "shoot_cooldown": 0.5,
    "projectile_speed": 400,
    "projectile_color": (255, 50, 50),
    "projectile_shape": "circle",
    "speed": 50,
    "is_boss": True,
    "phase": 1,  # Boss has 3 phases
    "phase_hp_thresholds": [0.66, 0.33],  # Phase 2 at 66% HP, Phase 3 at 33% HP
    "time_since_shot": 0.0,
}


def clone_enemies_from_templates() -> list[dict]:
    # Kept for compatibility but waves use start_wave() instead.
    return [make_enemy_from_template(t, 1.0, 1.0) for t in enemy_templates]


enemies: list[dict] = []

# ----------------------------
# Friendly AI
# ----------------------------
friendly_ai_templates: list[dict] = [
    {
        "type": "scout",
        "rect": pygame.Rect(0, 0, 24, 24),
        "color": (100, 200, 255),  # Light blue
        "hp": 40,
        "max_hp": 40,
        "shoot_cooldown": 0.4,
        "projectile_speed": 600,
        "projectile_color": (150, 220, 255),
        "projectile_shape": "circle",
        "speed": 180,
        "behavior": "aggressive",  # Charges nearest enemy
        "damage": 15,
    },
    {
        "type": "guardian",
        "rect": pygame.Rect(0, 0, 28, 28),
        "color": (100, 255, 150),  # Light green
        "hp": 80,
        "max_hp": 80,
        "shoot_cooldown": 0.6,
        "projectile_speed": 500,
        "projectile_color": (150, 255, 200),
        "projectile_shape": "square",
        "speed": 120,
        "behavior": "defensive",  # Stays near player, attacks nearby enemies
        "damage": 20,
    },
    {
        "type": "sniper",
        "rect": pygame.Rect(0, 0, 22, 22),
        "color": (255, 200, 100),  # Orange
        "hp": 30,
        "max_hp": 30,
        "shoot_cooldown": 1.2,
        "projectile_speed": 800,
        "projectile_color": (255, 220, 150),
        "projectile_shape": "diamond",
        "speed": 100,
        "behavior": "ranged",  # Keeps distance, snipes enemies
        "damage": 35,
    },
    {
        "type": "tank",
        "rect": pygame.Rect(0, 0, 32, 32),
        "color": (200, 150, 255),  # Purple
        "hp": 150,
        "max_hp": 150,
        "shoot_cooldown": 0.8,
        "projectile_speed": 400,
        "projectile_color": (220, 180, 255),
        "projectile_shape": "square",
        "speed": 80,
        "behavior": "tank",  # Slow, high HP, draws enemy fire
        "damage": 25,
    },
]

friendly_ai: list[dict] = []
friendly_projectiles: list[dict] = []

# ----------------------------
# Enemy projectiles
# ----------------------------
enemy_projectiles: list[dict] = []
enemy_projectile_size = (10, 10)
enemy_projectile_damage = 10
enemy_projectiles_color = (200, 200, 200)
enemy_projectile_shapes = ["circle", "square", "diamond"]

# ----------------------------
# Run counters (runs table)
# ----------------------------
running = True
run_time = 0.0

shots_fired = 0
hits = 0

damage_taken = 0
damage_dealt = 0

enemies_spawned = 0
enemies_killed = 0
deaths = 0
score = 0
survival_time = 0.0  # Total time survived in seconds

POS_SAMPLE_INTERVAL = 0.25  # Reduced frequency for better performance (was 0.10)
pos_timer = 0.0

# Waves / progression
wave_number = 1
wave_in_level = 1  # Wave within current level (1, 2, or 3)
wave_respawn_delay = 2.5  # seconds between waves
time_to_next_wave = 0.0
wave_active = True
base_enemies_per_wave = 9  # Increased for more enemies (was 6)
max_enemies_per_wave = 54  # Increased for more enemies (was 36)
boss_active = False

# Pickups
pickups: list[dict] = []
pickup_spawn_timer = 0.0
PICKUP_SPAWN_INTERVAL = 7.5

# Scoring constants
SCORE_BASE_POINTS = 100
SCORE_WAVE_MULTIPLIER = 50
SCORE_TIME_MULTIPLIER = 2

# Weapon key mapping
WEAPON_KEY_MAP = {
    pygame.K_1: "basic",
    pygame.K_2: "rocket",
    pygame.K_3: "triple",
    pygame.K_4: "bouncing",
    pygame.K_5: "giant",
    pygame.K_6: "laser",
}
enemy_spawn_boost_level = 0  # enemies can increase this by collecting "spawn_boost" pickups

# Visual effects for pickups
pickup_particles: list[dict] = []  # particles around pickups
collection_effects: list[dict] = []  # effects when pickups are collected


# ----------------------------
# Helpers
# ----------------------------
def clamp_rect_to_screen(r: pygame.Rect):
    r.x = max(0, min(r.x, WIDTH - r.w))
    r.y = max(0, min(r.y, HEIGHT - r.h))


def vec_toward(ax, ay, bx, by) -> pygame.Vector2:
    if USE_C_EXTENSION:
        x, y = game_physics.vec_toward(ax, ay, bx, by)
        return pygame.Vector2(x, y)
    else:
        v = pygame.Vector2(bx - ax, by - ay)
        if v.length_squared() == 0:
            return pygame.Vector2(1, 0)
        return v.normalize()


def line_rect_intersection(start: pygame.Vector2, end: pygame.Vector2, rect: pygame.Rect) -> pygame.Vector2 | None:
    """Find the closest intersection point between a line and a rectangle."""
    # Check if line intersects with rectangle
    clipped = rect.clipline(start, end)
    if not clipped:
        return None
    # Return the point closest to start
    p1, p2 = clipped
    dist1 = (pygame.Vector2(p1) - start).length_squared()
    dist2 = (pygame.Vector2(p2) - start).length_squared()
    return pygame.Vector2(p1) if dist1 < dist2 else pygame.Vector2(p2)


def can_move_rect(rect: pygame.Rect, dx: int, dy: int, other_rects: list[pygame.Rect]) -> bool:
    if USE_C_EXTENSION:
        return game_physics.can_move_rect(
            rect.x, rect.y, rect.w, rect.h, dx, dy, other_rects, WIDTH, HEIGHT
        )
    else:
        test = rect.move(dx, dy)
        if test.left < 0 or test.right > WIDTH or test.top < 0 or test.bottom > HEIGHT:
            return False
        for o in other_rects:
            if test.colliderect(o):
                return False
        return True


def move_player_with_push(player_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict]):
    """Solid collision + pushing blocks (single block push; no chain pushing)."""
    block_rects = [b["rect"] for b in block_list]
    # Also include moveable destructible blocks and trapezoid bounding rects
    moveable_destructible_rects = [b["rect"] for b in moveable_destructible_blocks]
    trapezoid_rects = [tb["bounding_rect"] for tb in trapezoid_blocks]
    all_collision_rects = block_rects + moveable_destructible_rects + trapezoid_rects

    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        player_rect.x += axis_dx
        player_rect.y += axis_dy

        hit_block = None
        hit_is_trapezoid = False
        # Check regular blocks first
        for b in block_list:
            if player_rect.colliderect(b["rect"]):
                hit_block = b
                break
        # Check moveable destructible blocks
        if hit_block is None:
            for b in moveable_destructible_blocks:
                if player_rect.colliderect(b["rect"]):
                    hit_block = b
                    break
        # Check trapezoid blocks (unmovable, so player can't push them)
        if hit_block is None:
            for tb in trapezoid_blocks:
                if player_rect.colliderect(tb["bounding_rect"]):
                    hit_block = tb
                    hit_is_trapezoid = True
                    break

        if hit_block is None:
            continue

        # Trapezoids are unmovable, so just block player movement
        if hit_is_trapezoid:
            player_rect.x -= axis_dx
            player_rect.y -= axis_dy
            continue

        hit_rect = hit_block["rect"]
        other_rects = [r for r in all_collision_rects if r is not hit_rect]

        if can_move_rect(hit_rect, axis_dx, axis_dy, other_rects):
            hit_rect.x += axis_dx
            hit_rect.y += axis_dy
        else:
            player_rect.x -= axis_dx
            player_rect.y -= axis_dy

    clamp_rect_to_screen(player_rect)


def move_enemy_with_push(enemy_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict]):
    """Enemy movement with block pushing (similar to player, but enemies can push blocks to chase player)."""
    block_rects = [b["rect"] for b in block_list]
    # Also include moveable destructible blocks (enemies can push these too)
    moveable_destructible_rects = [b["rect"] for b in moveable_destructible_blocks]
    # Trapezoids are unmovable, so enemies can't push them
    trapezoid_rects = [tb["bounding_rect"] for tb in trapezoid_blocks]
    all_collision_rects = block_rects + moveable_destructible_rects + trapezoid_rects

    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        enemy_rect.x += axis_dx
        enemy_rect.y += axis_dy

        hit_block = None
        hit_is_trapezoid = False
        hit_is_moveable_destructible = False
        # Check regular blocks first
        for b in block_list:
            if enemy_rect.colliderect(b["rect"]):
                hit_block = b
                break
        # Check moveable destructible blocks
        if hit_block is None:
            for b in moveable_destructible_blocks:
                if enemy_rect.colliderect(b["rect"]):
                    hit_block = b
                    hit_is_moveable_destructible = True
                    break
        # Check trapezoid blocks (unmovable, so enemy can't push them)
        if hit_block is None:
            for tb in trapezoid_blocks:
                if enemy_rect.colliderect(tb["bounding_rect"]):
                    hit_block = tb
                    hit_is_trapezoid = True
                    break

        if hit_block is None:
            continue

        # Trapezoids are unmovable, so just block enemy movement
        if hit_is_trapezoid:
            enemy_rect.x -= axis_dx
            enemy_rect.y -= axis_dy
            continue

        hit_rect = hit_block["rect"]
        other_rects = [r for r in all_collision_rects if r is not hit_rect]

        # Try to push the block
        if can_move_rect(hit_rect, axis_dx, axis_dy, other_rects):
            hit_rect.x += axis_dx
            hit_rect.y += axis_dy
        else:
            # Block can't be pushed, so enemy can't move
            enemy_rect.x -= axis_dx
            enemy_rect.y -= axis_dy

    clamp_rect_to_screen(enemy_rect)


def rect_offscreen(r: pygame.Rect) -> bool:
    return r.right < 0 or r.left > WIDTH or r.bottom < 0 or r.top > HEIGHT


def random_spawn_position(size: tuple[int, int], max_attempts: int = 25) -> pygame.Rect:
    """Find a spawn position not overlapping player or blocks."""
    w, h = size
    for _ in range(max_attempts):
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        candidate = pygame.Rect(x, y, w, h)
        if candidate.colliderect(player):
            continue
        if any(candidate.colliderect(b["rect"]) for b in blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in moveable_destructible_blocks):
            continue
        if any(candidate.colliderect(tb["bounding_rect"]) for tb in trapezoid_blocks):
            continue
        if any(candidate.colliderect(p["rect"]) for p in pickups):
            continue
        return candidate
    # fallback: top-left corner inside bounds
    return pygame.Rect(max(0, WIDTH // 2 - w), max(0, HEIGHT // 2 - h), w, h)


def make_enemy_from_template(t: dict, hp_scale: float, speed_scale: float) -> dict:
    hp = int(t["hp"] * hp_scale)
    enemy = {
        "type": t["type"],
        "rect": pygame.Rect(t["rect"].x, t["rect"].y, t["rect"].w, t["rect"].h),
        "color": t["color"],
        "hp": hp,
        "max_hp": hp,
        "shoot_cooldown": t["shoot_cooldown"],
        "time_since_shot": random.uniform(0.0, t["shoot_cooldown"]),
        "projectile_speed": t["projectile_speed"],
        "projectile_color": t.get("projectile_color", enemy_projectiles_color),
        "projectile_shape": t.get("projectile_shape", "circle"),
        "speed": t.get("speed", 80) * speed_scale,
    }
    # Add shield properties if present
    if t.get("has_shield"):
        enemy["has_shield"] = True
        enemy["shield_angle"] = random.uniform(0, 2 * math.pi)
        enemy["shield_length"] = t.get("shield_length", 50)
    if t.get("has_reflective_shield"):
        enemy["has_reflective_shield"] = True
        enemy["shield_angle"] = random.uniform(0, 2 * math.pi)
        enemy["shield_length"] = t.get("shield_length", 60)
        enemy["shield_hp"] = 0
        enemy["turn_speed"] = t.get("turn_speed", 0.5)
    return enemy


def log_enemy_spawns(new_enemies: list[dict]):
    global enemies_spawned
    for e in new_enemies:
        enemies_spawned += 1
        telemetry.log_enemy_spawn(
            EnemySpawnEvent(
                t=run_time,
                enemy_type=e["type"],
                x=e["rect"].x,
                y=e["rect"].y,
                w=e["rect"].w,
                h=e["rect"].h,
                hp=e["hp"],
            )
        )


def make_friendly_from_template(t: dict, hp_scale: float, speed_scale: float) -> dict:
    """Create a friendly AI unit from a template."""
    # Set HP to random 50-100 instead of using hp_scale
    hp = random.randint(50, 100)
    max_hp = hp  # Full health at wave start
    return {
        "type": t["type"],
        "rect": pygame.Rect(t["rect"].x, t["rect"].y, t["rect"].w, t["rect"].h),
        "color": t["color"],
        "hp": hp,
        "max_hp": max_hp,  # Full health, green bar at wave start
        "shoot_cooldown": t["shoot_cooldown"],
        "time_since_shot": random.uniform(0.0, t["shoot_cooldown"]),
        "projectile_speed": t["projectile_speed"],
        "projectile_color": t["projectile_color"],
        "projectile_shape": t["projectile_shape"],
        "speed": t["speed"] * speed_scale,
        "behavior": t["behavior"],
        "damage": t["damage"],
        "target": None,  # Current target enemy
    }


def find_nearest_enemy(friendly_pos: pygame.Vector2) -> dict | None:
    """Find the nearest enemy to a friendly AI unit."""
    if not enemies:
        return None
    nearest = None
    min_dist = float("inf")
    for e in enemies:
        dist = (pygame.Vector2(e["rect"].center) - friendly_pos).length_squared()
        if dist < min_dist:
            min_dist = dist
            nearest = e
    return nearest


def find_nearest_threat(enemy_pos: pygame.Vector2) -> tuple[pygame.Vector2, str] | None:
    """Find the nearest threat (player or friendly AI) to an enemy."""
    threats = []
    player_pos = pygame.Vector2(player.center)
    player_dist = (player_pos - enemy_pos).length_squared()
    threats.append((player_pos, player_dist, "player"))
    
    for f in friendly_ai:
        if f["hp"] <= 0:
            continue
        friendly_pos = pygame.Vector2(f["rect"].center)
        friendly_dist = (friendly_pos - enemy_pos).length_squared()
        threats.append((friendly_pos, friendly_dist, "friendly"))
    
    if not threats:
        return None
    
    # Return the closest threat
    threats.sort(key=lambda x: x[1])
    return (threats[0][0], threats[0][2])


def find_threats_in_dodge_range(enemy_pos: pygame.Vector2, dodge_range: float = 200.0) -> list[pygame.Vector2]:
    """Find bullets (player or friendly) that are close enough to dodge."""
    threats = []
    enemy_v2 = pygame.Vector2(enemy_pos)
    
    # Check player bullets
    for b in player_bullets:
        bullet_pos = pygame.Vector2(b["rect"].center)
        dist = (bullet_pos - enemy_v2).length()
        if dist < dodge_range:
            # Predict where bullet will be
            bullet_vel = b.get("vel", pygame.Vector2(0, 0))
            time_to_reach = dist / bullet_vel.length() if bullet_vel.length() > 0 else 999
            if time_to_reach < 0.5:  # Only dodge if bullet will reach soon
                threats.append(bullet_pos)
    
    # Check friendly projectiles
    for fp in friendly_projectiles:
        bullet_pos = pygame.Vector2(fp["rect"].center)
        dist = (bullet_pos - enemy_v2).length()
        if dist < dodge_range:
            bullet_vel = fp.get("vel", pygame.Vector2(0, 0))
            time_to_reach = dist / bullet_vel.length() if bullet_vel.length() > 0 else 999
            if time_to_reach < 0.5:
                threats.append(bullet_pos)
    
    return threats


def spawn_friendly_ai(count: int, hp_scale: float, speed_scale: float):
    """Spawn friendly AI units."""
    global friendly_ai
    spawned_list = []
    for _ in range(count):
        tmpl = random.choice(friendly_ai_templates)
        friendly = make_friendly_from_template(tmpl, hp_scale, speed_scale)
        # Spawn near player but not too close
        spawn_x = player.centerx + random.randint(-200, 200)
        spawn_y = player.centery + random.randint(-200, 200)
        spawn_x = max(50, min(spawn_x, WIDTH - 50))
        spawn_y = max(50, min(spawn_y, HEIGHT - 50))
        friendly["rect"].center = (spawn_x, spawn_y)
        friendly_ai.append(friendly)
        spawned_list.append(friendly)
    
    # Log friendly AI spawns
    for f in spawned_list:
        telemetry.log_friendly_spawn(
            FriendlyAISpawnEvent(
                t=run_time,
                friendly_type=f["type"],
                x=f["rect"].x,
                y=f["rect"].y,
                w=f["rect"].w,
                h=f["rect"].h,
                hp=f["hp"],
                behavior=f["behavior"],
            )
        )


def spawn_friendly_projectile(friendly: dict, target: dict):
    """Spawn a projectile from friendly AI targeting an enemy."""
    d = vec_toward(
        friendly["rect"].centerx, friendly["rect"].centery,
        target["rect"].centerx, target["rect"].centery
    )
    r = pygame.Rect(
        friendly["rect"].centerx - 6,
        friendly["rect"].centery - 6,
        12, 12
    )
    friendly_projectiles.append({
        "rect": r,
        "vel": d * friendly["projectile_speed"],
        "damage": friendly["damage"],
        "color": friendly["projectile_color"],
        "shape": friendly["projectile_shape"],
        "source_type": friendly["type"],
        "target_enemy_type": target.get("type", "unknown"),  # Store target type for telemetry
    })
    
    # Log friendly AI shot
    telemetry.log_friendly_shot(
        FriendlyAIShotEvent(
            t=run_time,
            friendly_type=friendly["type"],
            origin_x=friendly["rect"].centerx,
            origin_y=friendly["rect"].centery,
            target_x=target["rect"].centerx,
            target_y=target["rect"].centery,
            target_enemy_type=target.get("type", "unknown"),
        )
    )
    telemetry.flush(force=True)


def start_wave(wave_num: int):
    """Spawn a new wave with scaling. Each level has 3 waves, boss on wave 3."""
    global enemies, wave_active, boss_active, wave_in_level, current_level
    enemies = []
    boss_active = False
    
    # Calculate level and wave within level (1-based)
    current_level = min(max_level, (wave_num - 1) // 3 + 1)
    wave_in_level = ((wave_num - 1) % 3) + 1
    
    # Boss appears on wave 3 of each level
    if wave_in_level == 3:
        # Spawn boss
        boss = boss_template.copy()
        boss["rect"] = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
        diff_mult = difficulty_multipliers[difficulty]
        
        # Final level (level 3) boss has 10,000 HP
        if current_level == 3:
            boss["hp"] = 10000
            boss["max_hp"] = 10000
        else:
            # Scale boss HP for levels 1-2
            boss_hp_scale = 1.0 + (current_level - 1) * 0.5
            boss["hp"] = int(boss["max_hp"] * boss_hp_scale * diff_mult["enemy_hp"])
            boss["max_hp"] = boss["hp"]
        
        boss["phase"] = 1
        boss["time_since_shot"] = 0.0
        enemies.append(boss)
        boss_active = True
        log_enemy_spawns([boss])
        # Log boss as enemy type for this wave
        telemetry.log_wave_enemy_types(
            WaveEnemyTypeEvent(
                t=run_time,
                wave_number=wave_num,
                enemy_type=boss["type"],
                count=1,
            )
        )
        wave_active = True
        return
    
    # Normal wave spawning (waves 1 and 2 of each level)
    # Apply difficulty multipliers
    diff_mult = difficulty_multipliers[difficulty]
    # Level-based scaling - increase difficulty with level and wave in level
    level_mult = 1.0 + (current_level - 1) * 0.3
    wave_in_level_mult = 1.0 + (wave_in_level - 1) * 0.15  # Wave 2 is harder than wave 1
    hp_scale = (1.0 + 0.15 * (wave_num - 1)) * diff_mult["enemy_hp"] * level_mult * wave_in_level_mult
    speed_scale = (1.0 + 0.05 * (wave_num - 1)) * diff_mult["enemy_speed"] * level_mult * wave_in_level_mult
    # Apply difficulty to enemy count
    base_count = base_enemies_per_wave + enemy_spawn_boost_level + 2 * (wave_num - 1)
    count = min(int(base_count * diff_mult["enemy_spawn"] * 2.0), max_enemies_per_wave)  # 2.0x multiplier for more enemies

    spawned: list[dict] = []
    # Track enemy types for this wave
    enemy_type_counts: dict[str, int] = {}
    
    for _ in range(count):
        tmpl = random.choice(enemy_templates)
        enemy = make_enemy_from_template(tmpl, hp_scale, speed_scale)
        enemy["rect"] = random_spawn_position((enemy["rect"].w, enemy["rect"].h))
        spawned.append(enemy)
        # Count enemy types
        enemy_type = enemy["type"]
        enemy_type_counts[enemy_type] = enemy_type_counts.get(enemy_type, 0) + 1

    enemies.extend(spawned)
    log_enemy_spawns(spawned)
    
    # Log enemy types for this wave
    for enemy_type, type_count in enemy_type_counts.items():
        telemetry.log_wave_enemy_types(
            WaveEnemyTypeEvent(
                t=run_time,
                wave_number=wave_num,
                enemy_type=enemy_type,
                count=type_count,
            )
        )
    
    # Spawn friendly AI: 2-4 per wave (increased from 1-2)
    # Calculate friendly AI count based on enemy count - more friendly AI
    friendly_count = max(2, min(4, (count + 1) // 2))  # 2-4 friendly per wave
    spawn_friendly_ai(friendly_count, hp_scale, speed_scale)
    
    wave_active = True
    
    # Log wave start event
    telemetry.log_wave(
        WaveEvent(
            t=run_time,
            wave_number=wave_num,
            event_type="start",
            enemies_spawned=count,
            hp_scale=hp_scale,
            speed_scale=speed_scale,
        )
    )


def spawn_pickup(pickup_type: str):
    # Make pickups bigger
    size = (32, 32)
    r = random_spawn_position(size)
    # All pickups look the same (mystery) - randomized color so player doesn't know what they're getting
    mystery_colors = [
        (180, 100, 255),  # purple
        (100, 255, 180),  # green
        (255, 180, 100),  # orange
        (180, 255, 255),  # cyan
        (255, 100, 180),  # pink
        (255, 255, 100),  # yellow
    ]
    color = random.choice(mystery_colors)
    pickups.append({
        "type": pickup_type,
        "rect": r,
        "color": color,
        "timer": 15.0,  # pickup despawns after 15 seconds
        "age": 0.0,  # current age for visual effects
    })


def spawn_weapon_in_center(weapon_type: str):
    """Spawn a weapon pickup in the center of the screen (level completion reward)."""
    weapon_colors_map = {
        "basic": (200, 200, 200),
        "rocket": (255, 100, 0),
        "triple": (100, 200, 255),
        "bouncing": (100, 255, 100),
        "giant": (255, 200, 0),
        "laser": (255, 50, 50),
    }
    weapon_pickup_size = (40, 40)  # Bigger for level completion rewards
    weapon_pickup_rect = pygame.Rect(
        WIDTH // 2 - weapon_pickup_size[0] // 2,
        HEIGHT // 2 - weapon_pickup_size[1] // 2,
        weapon_pickup_size[0],
        weapon_pickup_size[1]
    )
    pickups.append({
        "type": weapon_type,
        "rect": weapon_pickup_rect,
        "color": weapon_colors_map.get(weapon_type, (180, 100, 255)),
        "timer": 30.0,  # Level completion weapons last longer
        "age": 0.0,
        "is_weapon_drop": True,
        "is_level_reward": True,  # Mark as level completion reward
    })


def spawn_weapon_drop(enemy: dict):
    """Spawn a weapon drop from a killed enemy."""
    enemy_type = enemy.get("type", "grunt")
    weapon_drop_map = {
        "grunt": "basic",
        "stinky": "basic",
        "heavy": "rocket",
        "baka": "triple",
        "neko neko desu": "bouncing",
        "BIG NEKU": "giant",
        "bouncer": "bouncing",
    }
    # 30% chance to drop weapon
    if random.random() < 0.3 and enemy_type in weapon_drop_map:
        weapon_type = weapon_drop_map[enemy_type]
        # Spawn weapon pickup at enemy location
        weapon_pickup_size = (28, 28)
        weapon_pickup_rect = pygame.Rect(
            enemy["rect"].centerx - weapon_pickup_size[0] // 2,
            enemy["rect"].centery - weapon_pickup_size[1] // 2,
            weapon_pickup_size[0],
            weapon_pickup_size[1]
        )
        weapon_colors_map = {
            "basic": (200, 200, 200),
            "rocket": (255, 100, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "giant": (255, 200, 0),
            "laser": (255, 50, 50),
        }
        pickups.append({
            "type": weapon_type,
            "rect": weapon_pickup_rect,
            "color": weapon_colors_map.get(weapon_type, (180, 100, 255)),
            "timer": 10.0,  # Weapon pickups last 10 seconds
            "age": 0.0,
            "is_weapon_drop": True,  # Mark as weapon drop
        })


def draw_health_bar(x, y, w, h, hp, max_hp):
    hp = max(0, min(hp, max_hp))
    pygame.draw.rect(screen, (60, 60, 60), (x, y, w, h))
    fill_w = int(w * (hp / max_hp)) if max_hp > 0 else 0
    pygame.draw.rect(screen, (60, 200, 60), (x, y, fill_w, h))
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), 2)


def create_pickup_collection_effect(x: int, y: int, color: tuple[int, int, int]):
    """Create particle effect when pickup is collected."""
    global collection_effects
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 150)
        collection_effects.append({
            "x": float(x),
            "y": float(y),
            "vel_x": math.cos(angle) * speed,
            "vel_y": math.sin(angle) * speed,
            "color": color,
            "life": 0.4,  # particle lifetime
            "size": random.randint(3, 6),
        })


def update_pickup_effects(dt: float):
    """Update pickup particle effects."""
    global pickup_particles, collection_effects
    
    # Update collection effects
    for effect in collection_effects[:]:
        effect["x"] += effect["vel_x"] * dt
        effect["y"] += effect["vel_y"] * dt
        effect["life"] -= dt
        if effect["life"] <= 0:
            collection_effects.remove(effect)
    
    # Generate particles around pickups
    pickup_particles.clear()
    for p in pickups:
        center_x = p["rect"].centerx
        center_y = p["rect"].centery
        age = p.get("age", 0.0)
        # Create pulsing glow effect
        pulse = (math.sin(age * 4.0) + 1.0) / 2.0  # 0 to 1
        glow_radius = 20 + pulse * 10
        glow_alpha = int(100 + pulse * 80)
        
        # Add particles around pickup
        for i in range(8):
            angle = (i / 8.0) * 2 * math.pi + age * 2.0
            dist = glow_radius * 0.7
            px = center_x + math.cos(angle) * dist
            py = center_y + math.sin(angle) * dist
            pickup_particles.append({
                "x": px,
                "y": py,
                "color": p["color"],
                "alpha": int(glow_alpha * 0.6),
                "size": 3,
            })


def draw_centered_text(text: str, y: int, color=(235, 235, 235), use_big=False):
    f = big_font if use_big else font
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)


def draw_projectile(rect: pygame.Rect, color: tuple[int, int, int], shape: str):
    if shape == "circle":
        pygame.draw.circle(screen, color, rect.center, rect.w // 2)
    elif shape == "diamond":
        cx, cy = rect.center
        hw, hh = rect.w // 2, rect.h // 2
        points = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
        pygame.draw.polygon(screen, color, points)
    else:
        pygame.draw.rect(screen, color, rect)


def spawn_player_bullet_and_log():
    global shots_fired, player_bullet_shape_index

    # Determine aiming direction based on aiming mode
    if aiming_mode == AIM_ARROWS:
        # Arrow key aiming
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1
        
        if dx == 0 and dy == 0:
            # No arrow keys pressed, use last movement direction or default
            if last_move_velocity.length_squared() > 0:
                base_dir = last_move_velocity.normalize()
            else:
                base_dir = pygame.Vector2(1, 0)  # Default right
        else:
            base_dir = pygame.Vector2(dx, dy).normalize()
        
        # Calculate target position for telemetry (extend direction from player)
        target_dist = 100  # Distance to calculate target point
        mx = int(player.centerx + base_dir.x * target_dist)
        my = int(player.centery + base_dir.y * target_dist)
    else:
        # Mouse aiming (default)
        mx, my = pygame.mouse.get_pos()
        base_dir = vec_toward(player.centerx, player.centery, mx, my)

    shape = player_bullet_shapes[player_bullet_shape_index % len(player_bullet_shapes)]
    player_bullet_shape_index = (player_bullet_shape_index + 1) % len(player_bullet_shapes)

    # Determine shot pattern based on weapon mode
    if current_weapon_mode == "triple":
        # Triple shot: center + left + right spread
        spread_angle_deg = 8.6  # degrees
        directions = [
            base_dir,  # center
            base_dir.rotate(-spread_angle_deg),  # left
            base_dir.rotate(spread_angle_deg),  # right
        ]
    else:
        directions = [base_dir]

    # Spawn bullets for each direction
    for d in directions:
        # Apply stat multipliers
        size_mult = player_stat_multipliers["bullet_size"]
        if current_weapon_mode == "giant":
            size_mult *= 10.0  # 10x size multiplier
        elif current_weapon_mode == "rocket":
            size_mult *= 2.5  # Rockets are bigger (2.5x size)
        
        effective_size = (
            int(player_bullet_size[0] * size_mult),
            int(player_bullet_size[1] * size_mult),
        )
        effective_speed = player_bullet_speed * player_stat_multipliers["bullet_speed"]
        base_damage = int(player_bullet_damage * player_stat_multipliers["bullet_damage"])
        
        # Rocket launcher: more damage and always has explosion
        if current_weapon_mode == "rocket":
            effective_damage = int(base_damage * 2.5)  # 2.5x damage
            rocket_explosion = max(80.0, player_stat_multipliers["bullet_explosion_radius"] + 60.0)
        else:
            effective_damage = base_damage
            rocket_explosion = 0.0

        r = pygame.Rect(
            player.centerx - effective_size[0] // 2,
            player.centery - effective_size[1] // 2,
            effective_size[0],
            effective_size[1],
        )
        player_bullets.append({
            "rect": r,
            "vel": d * effective_speed,
            "shape": shape,
            "color": (255, 100, 0) if current_weapon_mode == "rocket" else player_bullets_color,  # orange for rockets
            "damage": effective_damage,
            "penetration": int(player_stat_multipliers["bullet_penetration"]),
            "explosion_radius": max(rocket_explosion, player_stat_multipliers["bullet_explosion_radius"]),
            "knockback": player_stat_multipliers["bullet_knockback"],
            "bounces": 10 if current_weapon_mode == "bouncing" else 0,  # max bounces
            "is_rocket": current_weapon_mode == "rocket",
        })
    shots_fired += 1

    telemetry.log_shot(
        ShotEvent(
            t=run_time,
            origin_x=player.centerx,
            origin_y=player.centery,
            target_x=mx,
            target_y=my,
            dir_x=float(d.x),
            dir_y=float(d.y),
        )
    )
    
    # Log bullet metadata
    telemetry.log_bullet_metadata(
        BulletMetadataEvent(
            t=run_time,
            bullet_type="player",
            shape=shape,
            color_r=player_bullets_color[0],
            color_g=player_bullets_color[1],
            color_b=player_bullets_color[2],
        )
    )


def spawn_enemy_projectile(enemy: dict):
    """Spawn projectile from enemy targeting nearest threat (player or friendly AI)."""
    e_pos = pygame.Vector2(enemy["rect"].center)
    threat_result = find_nearest_threat(e_pos)
    
    if threat_result:
        threat_pos, threat_type = threat_result
        d = vec_toward(e_pos.x, e_pos.y, threat_pos.x, threat_pos.y)
    else:
        # Fallback to player if no threats
        d = vec_toward(enemy["rect"].centerx, enemy["rect"].centery, player.centerx, player.centery)
    r = pygame.Rect(
        enemy["rect"].centerx - enemy_projectile_size[0] // 2,
        enemy["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    proj_color = enemy.get("projectile_color", enemy_projectiles_color)
    proj_shape = enemy.get("projectile_shape", "circle")
    bounces = enemy.get("bouncing_projectiles", False)
    enemy_projectiles.append(
        {
            "rect": r,
            "vel": d * enemy["projectile_speed"],
            "enemy_type": enemy["type"],  # attribute damage source
            "color": proj_color,
            "shape": proj_shape,
            "bounces": 10 if bounces else 0,  # max bounces for bouncing enemy type
        }
    )
    
    # Log enemy projectile metadata
    telemetry.log_bullet_metadata(
        BulletMetadataEvent(
                t=run_time,
            bullet_type="enemy",
            shape=proj_shape,
            color_r=proj_color[0],
            color_g=proj_color[1],
            color_b=proj_color[2],
            source_enemy_type=enemy["type"],
        )
    )


def spawn_boss_projectile(boss: dict, direction: pygame.Vector2):
    """Spawn a projectile from the boss in a specific direction."""
    r = pygame.Rect(
        boss["rect"].centerx - enemy_projectile_size[0] // 2,
        boss["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    proj_color = boss.get("projectile_color", enemy_projectiles_color)
    proj_shape = boss.get("projectile_shape", "circle")
    enemy_projectiles.append(
        {
            "rect": r,
            "vel": direction * boss["projectile_speed"],
            "enemy_type": boss["type"],
            "color": proj_color,
            "shape": proj_shape,
            "bounces": 0,
        }
    )


def log_enemy_spawns_for_current_wave():
    log_enemy_spawns(enemies)


def calculate_kill_score(wave_num: int, run_time: float) -> int:
    """Calculate score for killing an enemy."""
    return SCORE_BASE_POINTS + (wave_num * SCORE_WAVE_MULTIPLIER) + int(run_time * SCORE_TIME_MULTIPLIER)


def kill_enemy(enemy: dict):
    """Handle enemy death: drop weapon, update score, remove from list."""
    global enemies_killed, score, current_level
    is_boss = enemy.get("is_boss", False)
    
    # If boss is killed, spawn level completion weapon in center
    if is_boss:
        # Weapons unlock in order: basic (start), rocket (level 1), triple (level 2), laser (level 3)
        weapon_unlock_order = {1: "rocket", 2: "triple", 3: "laser"}
        if current_level in weapon_unlock_order:
            weapon_to_unlock = weapon_unlock_order[current_level]
            if weapon_to_unlock not in unlocked_weapons:
                spawn_weapon_in_center(weapon_to_unlock)
    else:
        # Regular enemies drop weapons randomly
        spawn_weapon_drop(enemy)
    
    try:
        enemies.remove(enemy)
    except ValueError:
        pass  # Already removed
    enemies_killed += 1
    score += calculate_kill_score(wave_number, run_time)


def apply_pickup_effect(pickup_type: str):
    """Apply the effect of a collected pickup."""
    global boost_meter, fire_rate_buff_t, player_max_hp, player_hp
    global player_stat_multipliers, current_weapon_mode, overshield
    
    if pickup_type == "boost":
        boost_meter = min(boost_meter_max, boost_meter + 45.0)
    elif pickup_type == "firerate":
        fire_rate_buff_t = fire_rate_buff_duration
    elif pickup_type == "max_health":
        player_max_hp += 15
        player_hp += 15  # also heal by the same amount
    elif pickup_type == "speed":
        player_stat_multipliers["speed"] += 0.15
    elif pickup_type == "firerate_permanent":
        player_stat_multipliers["firerate"] += 0.12
    elif pickup_type == "bullet_size":
        player_stat_multipliers["bullet_size"] += 0.20
    elif pickup_type == "bullet_speed":
        player_stat_multipliers["bullet_speed"] += 0.15
    elif pickup_type == "bullet_damage":
        player_stat_multipliers["bullet_damage"] += 0.20
    elif pickup_type == "bullet_knockback":
        player_stat_multipliers["bullet_knockback"] += 0.25
    elif pickup_type == "bullet_penetration":
        player_stat_multipliers["bullet_penetration"] += 1
    elif pickup_type == "bullet_explosion":
        player_stat_multipliers["bullet_explosion_radius"] += 25.0
    elif pickup_type == "health_regen":
        # Increase player health regeneration rate
        global player_health_regen_rate
        player_health_regen_rate += 5.0  # Add 5 HP per second regeneration
    # Weapon pickups - unlock and switch to weapon
    elif pickup_type in ["giant_bullets", "giant"]:
        unlocked_weapons.add("giant")
        previous_weapon_mode = current_weapon_mode
        current_weapon_mode = "giant"
        # Log weapon switch from pickup
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type in ["triple_shot", "triple"]:
        unlocked_weapons.add("triple")
        previous_weapon_mode = current_weapon_mode
        current_weapon_mode = "triple"
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type in ["bouncing_bullets", "bouncing"]:
        unlocked_weapons.add("bouncing")
        previous_weapon_mode = current_weapon_mode
        current_weapon_mode = "bouncing"
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type in ["rocket_launcher", "rocket"]:
        unlocked_weapons.add("rocket")
        previous_weapon_mode = current_weapon_mode
        current_weapon_mode = "rocket"
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type == "laser":
        unlocked_weapons.add("laser")
        previous_weapon_mode = current_weapon_mode
        current_weapon_mode = "laser"
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type == "basic":
        unlocked_weapons.add("basic")  # Should already be unlocked, but ensure it
        previous_weapon_mode = current_weapon_mode
        current_weapon_mode = "basic"
        if previous_weapon_mode != current_weapon_mode:
            telemetry.log_player_action(PlayerActionEvent(
                t=run_time,
                action_type="weapon_switch",
                x=player.centerx,
                y=player.centery,
                duration=None,
                success=True
            ))
    elif pickup_type == "overshield":
        overshield = min(overshield_max, overshield + 25)


def render_hud_text(text: str, y: int, color=(230, 230, 230)) -> int:
    """Render HUD text at position and return next Y position."""
    screen.blit(font.render(text, True, color), (10, y))
    return y + 24


def reset_after_death():
    global player_hp, player_time_since_shot, pos_timer, previous_weapon_mode, current_weapon_mode
    global previous_boost_state, previous_slow_state, player_current_zones
    global enemies, player_bullets, enemy_projectiles, wave_number, time_to_next_wave, wave_active
    global current_weapon_mode, overshield, unlocked_weapons, wave_in_level, current_level
    global jump_cooldown_timer, jump_timer, is_jumping, jump_velocity
    global laser_beams, laser_time_since_shot
    global shield_active, shield_duration_remaining, shield_cooldown_remaining
    global player_health_regen_rate, moving_health_zone

    player_hp = player_max_hp
    player_health_regen_rate = 0.0  # Reset health regeneration rate
    # Reset moving health zone to center
    moving_health_zone["rect"].center = (WIDTH // 2, HEIGHT // 2)
    moving_health_zone["target"] = None
    overshield = 0  # Reset overshield
    player_time_since_shot = 999.0
    laser_time_since_shot = 999.0
    pos_timer = 0.0
    wave_number = 1
    wave_in_level = 1
    current_level = 1
    unlocked_weapons = {"basic"}  # Reset to only basic weapon unlocked
    current_weapon_mode = "basic"  # Reset to basic weapon
    previous_weapon_mode = "basic"
    previous_boost_state = False
    previous_slow_state = False
    player_current_zones = set()
    jump_cooldown_timer = 0.0
    jump_timer = 0.0
    is_jumping = False
    jump_velocity = pygame.Vector2(0, 0)
    laser_beams.clear()
    # Reset shield
    shield_active = False
    shield_duration_remaining = 0.0
    shield_cooldown_remaining = 0.0

    player.x = (WIDTH - player.w) // 2
    player.y = (HEIGHT - player.h) // 2
    clamp_rect_to_screen(player)

    player_bullets.clear()
    enemy_projectiles.clear()
    friendly_ai.clear()
    friendly_projectiles.clear()

    wave_number = 1
    time_to_next_wave = 0.0
    start_wave(wave_number)


# ----------------------------
# Start run + log initial spawns
# ----------------------------
run_id = None  # Will be set when game starts
# Don't start wave automatically - wait for menu selection


# ----------------------------
# Main loop with safe shutdown
# ----------------------------
try:
    while running:
        # Allow uncapped FPS for better performance, or cap at 60
        dt_real = clock.tick(0) / 1000.0  # 0 = uncapped, use 60 for capped
        # Cap dt to prevent large jumps
        dt = min(dt_real if state == STATE_PLAYING else 0.0, 0.033)  # Max 30ms = ~30 FPS minimum

        if state == STATE_PLAYING:
            run_time += dt
            survival_time += dt  # Track total survival time
            player_time_since_shot += dt

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Controls rebinding mode
                if state == STATE_CONTROLS and controls_rebinding:
                    action = controls_actions[controls_selected]
                    controls[action] = event.key
                    save_controls(controls)
                    controls_rebinding = False
                    continue

                # Update last-pressed direction for conflict resolution
                if event.key in (controls["move_left"], controls["move_right"]):
                    last_horizontal_key = event.key
                if event.key in (controls["move_up"], controls["move_down"]):
                    last_vertical_key = event.key

                # Weapon switching (keys 1-6) - only works if weapon is unlocked
                if state == STATE_PLAYING:
                    if event.key in WEAPON_KEY_MAP:
                        requested_weapon = WEAPON_KEY_MAP[event.key]
                        # Only switch if weapon is unlocked
                        if requested_weapon in unlocked_weapons:
                            previous_weapon_mode = current_weapon_mode
                            current_weapon_mode = requested_weapon
                            # Log weapon switch
                            if previous_weapon_mode != current_weapon_mode:
                                telemetry.log_player_action(PlayerActionEvent(
                                    t=run_time,
                                    action_type="weapon_switch",
                                    x=player.centerx,
                                    y=player.centery,
                                    duration=None,
                                    success=True
                                ))
                    # Space bar jump/dash in direction of movement
                    elif event.key == pygame.K_SPACE and jump_cooldown_timer <= 0.0 and not is_jumping:
                        jump_success = False
                        if last_move_velocity.length_squared() > 0:
                            # Jump in direction of movement
                            jump_dir = last_move_velocity.normalize()
                            jump_velocity = jump_dir * jump_speed
                            jump_timer = jump_duration
                            is_jumping = True
                            jump_cooldown_timer = jump_cooldown
                            jump_success = True
                        elif move_dir.length_squared() > 0:
                            # Fallback: use current move direction
                            jump_dir = move_dir.normalize()
                            jump_velocity = jump_dir * jump_speed
                            jump_timer = jump_duration
                            is_jumping = True
                            jump_cooldown_timer = jump_cooldown
                            jump_success = True
                        
                        # Log jump action
                        if jump_success:
                            telemetry.log_player_action(PlayerActionEvent(
                                t=run_time,
                                action_type="jump",
                                x=player.centerx,
                                y=player.centery,
                                duration=jump_duration,
                                success=True
                            ))

                # Menu navigation
                if state == STATE_MENU:
                    if menu_section == 0:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            difficulty_selected = (difficulty_selected - 1) % len(difficulty_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            difficulty_selected = (difficulty_selected + 1) % len(difficulty_options)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            menu_section = 1
                    elif menu_section == 1:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            aiming_mode_selected = (aiming_mode_selected - 1) % 2
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            aiming_mode_selected = (aiming_mode_selected + 1) % 2
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            menu_section = 2
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 0
                    elif menu_section == 2:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            player_class_selected = (player_class_selected - 1) % len(player_class_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            player_class_selected = (player_class_selected + 1) % len(player_class_options)
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            menu_section = 3
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 1
                    elif menu_section == 3:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            ui_show_metrics_selected = (ui_show_metrics_selected - 1) % 2
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            ui_show_metrics_selected = (ui_show_metrics_selected + 1) % 2
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            menu_section = 4
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 2
                    elif menu_section == 4:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            # Start game with selected settings
                            difficulty = difficulty_options[difficulty_selected]
                            aiming_mode = AIM_MOUSE if aiming_mode_selected == 0 else AIM_ARROWS
                            player_class = player_class_options[player_class_selected]
                            ui_show_metrics = ui_show_metrics_selected == 0
                            # Apply class stats
                            stats = player_class_stats[player_class]
                            player_max_hp = int(100 * stats["hp_mult"])
                            player_hp = player_max_hp
                            player_speed = int(300 * stats["speed_mult"])
                            player_bullet_damage = int(20 * stats["damage_mult"])
                            player_shoot_cooldown = 0.12 / stats["firerate_mult"]
                            state = STATE_PLAYING
                            run_id = telemetry.start_run(run_started_at, player_max_hp)
                            start_wave(wave_number)
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            menu_section = 3
                
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_PLAYING:
                        state = STATE_PAUSED
                        pause_selected = 0
                    elif state == STATE_PAUSED:
                        state = STATE_PLAYING
                    elif state == STATE_CONTINUE:
                        running = False
                    elif state == STATE_CONTROLS:
                        state = STATE_PAUSED
                    elif state == STATE_MENU:
                        running = False
                    elif state == STATE_VICTORY or state == STATE_GAME_OVER:
                        running = False  # Quit from victory/game over screens

                if event.key == pygame.K_p:
                    if state == STATE_PLAYING:
                        state = STATE_PAUSED
                        pause_selected = 0
                    elif state == STATE_PAUSED:
                        state = STATE_PLAYING

                # Pause menu
                if state == STATE_PAUSED:
                    if event.key == pygame.K_UP:
                        pause_selected = (pause_selected - 1) % len(pause_options)
                    elif event.key == pygame.K_DOWN:
                        pause_selected = (pause_selected + 1) % len(pause_options)
                    elif event.key == pygame.K_RETURN:
                        choice = pause_options[pause_selected]
                        if choice == "Continue":
                            state = STATE_PLAYING
                        elif choice == "Quit":
                            running = False
                    elif event.key == pygame.K_c:
                        state = STATE_CONTROLS
                        controls_selected = 0
                        controls_rebinding = False

                # Controls menu
                if state == STATE_CONTROLS and not controls_rebinding:
                    if event.key == pygame.K_UP:
                        controls_selected = (controls_selected - 1) % len(controls_actions)
                    elif event.key == pygame.K_DOWN:
                        controls_selected = (controls_selected + 1) % len(controls_actions)
                    elif event.key == pygame.K_RETURN:
                        controls_rebinding = True

                # Shield activation (Left Alt key)
                if state == STATE_PLAYING:
                    if event.key == pygame.K_LALT:
                        # Activate shield if cooldown is ready
                        if shield_cooldown_remaining <= 0.0 and not shield_active:
                            shield_active = True
                            shield_duration_remaining = shield_duration
                            # Random cooldown between 10-15 seconds
                            shield_cooldown = random.uniform(10.0, 15.0)
                
                # Victory screen
                if state == STATE_VICTORY:
                    if event.key == pygame.K_e:
                        # Enter endurance mode after victory
                        state = STATE_ENDURANCE
                        lives = 999  # Infinite lives in endurance mode
                        wave_number += 1  # Continue from next wave
                        start_wave(wave_number)
                
                # Game Over screen
                if state == STATE_GAME_OVER:
                    if event.key == pygame.K_e:
                        # Enter endurance mode
                        state = STATE_ENDURANCE
                        lives = 999  # Infinite lives in endurance mode
                        wave_number += 1  # Continue from next wave
                        start_wave(wave_number)

                # Continue screen
                if state == STATE_CONTINUE:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        reset_after_death()
                        state = STATE_PLAYING

            if event.type == pygame.KEYUP:
                keys_now = pygame.key.get_pressed()
                if event.key in (controls["move_left"], controls["move_right"]):
                    if last_horizontal_key == event.key:
                        left_k = controls["move_left"]
                        right_k = controls["move_right"]
                        if keys_now[left_k] and not keys_now[right_k]:
                            last_horizontal_key = left_k
                        elif keys_now[right_k] and not keys_now[left_k]:
                            last_horizontal_key = right_k
                        else:
                            last_horizontal_key = None
                if event.key in (controls["move_up"], controls["move_down"]):
                    if last_vertical_key == event.key:
                        up_k = controls["move_up"]
                        down_k = controls["move_down"]
                        if keys_now[up_k] and not keys_now[down_k]:
                            last_vertical_key = up_k
                        elif keys_now[down_k] and not keys_now[up_k]:
                            last_vertical_key = down_k
                        else:
                            last_vertical_key = None

        # --- Simulation ---
        if state == STATE_PLAYING:
            # Movement
            if not enemies and wave_active:
                wave_active = False
                time_to_next_wave = max(0.5, wave_respawn_delay - 0.25 * enemy_spawn_boost_level)
                # Log wave end event
                telemetry.log_wave(
                    WaveEvent(
                        t=run_time,
                        wave_number=wave_number,
                        event_type="end",
                        enemies_spawned=0,
                        hp_scale=1.0 + 0.15 * (wave_number - 1),
                        speed_scale=1.0 + 0.05 * (wave_number - 1),
                    )
                )

            if not wave_active:
                time_to_next_wave = max(0.0, time_to_next_wave - dt)
                if time_to_next_wave <= 0.0:
                    # Check if all levels are complete (wave 9 = level 3, wave 3)
                    if wave_number >= max_level * 3:
                        # All levels completed - victory!
                        state = STATE_VICTORY
                    else:
                        wave_number += 1
                        # Level progression is now handled in start_wave() (3 waves per level)
                        start_wave(wave_number)

            keys = pygame.key.get_pressed()
            dx = dy = 0
            left_k = controls["move_left"]
            right_k = controls["move_right"]
            up_k = controls["move_up"]
            down_k = controls["move_down"]
            boost_k = controls["boost"]
            slow_k = controls["slow"]

            left = keys[left_k]
            right = keys[right_k]
            up = keys[up_k]
            down = keys[down_k]
            wants_boost = keys[boost_k]
            wants_slow = keys[slow_k]

            if left and right:
                dx = -1 if last_horizontal_key == left_k else 1
            elif left:
                dx = -1
            elif right:
                dx = 1

            if up and down:
                dy = -1 if last_vertical_key == up_k else 1
            elif up:
                dy = -1
            elif down:
                dy = 1

            move_dir = pygame.Vector2(dx, dy)
            speed_mult = player_stat_multipliers["speed"]  # Apply permanent speed multiplier
            if wants_slow:
                speed_mult *= slow_speed_mult
            boosting = wants_boost and boost_meter > 0.0 and not wants_slow
            
            # Log boost/slow state changes
            if boosting != previous_boost_state:
                if boosting:
                    telemetry.log_player_action(PlayerActionEvent(
                        t=run_time,
                        action_type="boost",
                        x=player.centerx,
                        y=player.centery,
                        duration=None,
                        success=True
                    ))
                previous_boost_state = boosting
            
            if wants_slow != previous_slow_state:
                if wants_slow:
                    telemetry.log_player_action(PlayerActionEvent(
                        t=run_time,
                        action_type="slow",
                        x=player.centerx,
                        y=player.centery,
                        duration=None,
                        success=True
                    ))
                previous_slow_state = wants_slow
            
            if boosting:
                speed_mult *= boost_speed_mult
                boost_meter = max(0.0, boost_meter - boost_drain_per_s * dt)
            else:
                boost_meter = min(boost_meter_max, boost_meter + boost_regen_per_s * dt)
            
            # Shield update logic
            if shield_active:
                shield_duration_remaining -= dt
                if shield_duration_remaining <= 0.0:
                    shield_active = False
                    shield_cooldown_remaining = shield_cooldown
            else:
                # Shield is on cooldown
                if shield_cooldown_remaining > 0.0:
                    shield_cooldown_remaining = max(0.0, shield_cooldown_remaining - dt)

            if move_dir.length_squared() > 0:
                move_dir = move_dir.normalize()
                last_move_velocity = move_dir * player_speed * speed_mult
            else:
                last_move_velocity = pygame.Vector2(0, 0)

            # Update jump timers
            if jump_cooldown_timer > 0.0:
                jump_cooldown_timer -= dt
            if is_jumping:
                jump_timer -= dt
                if jump_timer <= 0.0:
                    is_jumping = False
                    jump_velocity = pygame.Vector2(0, 0)

            # Apply jump velocity if jumping
            total_velocity = last_move_velocity.copy()
            if is_jumping:
                # Apply jump velocity (decay over time)
                jump_factor = jump_timer / jump_duration
                total_velocity += jump_velocity * jump_factor

            move_x = int(total_velocity.x * dt)
            move_y = int(total_velocity.y * dt)

            # Shooting
            laser_time_since_shot += dt
            if current_weapon_mode == "laser":
                # Laser beam weapon - continuous beam while mouse is held
                if pygame.mouse.get_pressed(3)[0] and laser_time_since_shot >= laser_cooldown:
                    # Create or update laser beam
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    player_center = pygame.Vector2(player.center)
                    mouse_pos = pygame.Vector2(mouse_x, mouse_y)
                    direction = (mouse_pos - player_center)
                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                        # Calculate laser end point (stops at blocks or enemies)
                        laser_end = player_center + direction * laser_length
                        closest_hit = None
                        closest_dist = laser_length
                        
                        # Check collision with blocks first (solid blocks stop laser)
                        for blk in blocks:
                            hit = line_rect_intersection(player_center, laser_end, blk["rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                        
                        # Check collision with trapezoid blocks
                        for tb in trapezoid_blocks:
                            hit = line_rect_intersection(player_center, laser_end, tb["bounding_rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                        
                        # Check collision with destructible blocks (can damage them)
                        for db in destructible_blocks[:]:
                            hit = line_rect_intersection(player_center, laser_end, db["rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                                # Damage destructible block
                                db["hp"] -= laser_damage * dt * 60  # Damage per second
                                if db["hp"] <= 0:
                                    destructible_blocks.remove(db)
                        
                        # Check collision with moveable destructible blocks (can damage them)
                        for mdb in moveable_destructible_blocks[:]:
                            hit = line_rect_intersection(player_center, laser_end, mdb["rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                                # Damage moveable destructible block
                                mdb["hp"] -= laser_damage * dt * 60  # Damage per second
                                if mdb["hp"] <= 0:
                                    moveable_destructible_blocks.remove(mdb)
                        
                        # Check collision with enemies (can damage them)
                        for e in enemies[:]:
                            hit = line_rect_intersection(player_center, laser_end, e["rect"])
                            if hit:
                                dist = (hit - player_center).length()
                                if dist < closest_dist:
                                    closest_dist = dist
                                    closest_hit = hit
                                    laser_end = hit
                                # Damage enemy continuously
                                e["hp"] -= laser_damage * dt * 60
                                damage_dealt += int(laser_damage * dt * 60)
                                if e["hp"] <= 0:
                                    kill_enemy(e)
                        # Store laser beam for drawing
                        if len(laser_beams) == 0:
                            laser_beams.append({
                                "start": player_center,
                                "end": laser_end,
                                "color": (255, 50, 50),  # Bright red
                                "width": 8,
                            })
                        else:
                            laser_beams[0]["start"] = player_center
                            laser_beams[0]["end"] = laser_end
                else:
                    # Clear laser when not shooting
                    laser_beams.clear()
            else:
                # Normal shooting for other weapons
                # Apply both temporary and permanent fire rate multipliers
                temp_mult = fire_rate_mult if fire_rate_buff_t > 0 else 1.0
                perm_mult = 1.0 / player_stat_multipliers["firerate"] if player_stat_multipliers["firerate"] > 1.0 else 1.0
                # Rocket launcher has slower fire rate
                rocket_mult = 3.5 if current_weapon_mode == "rocket" else 1.0
                effective_cooldown = player_shoot_cooldown * temp_mult * perm_mult * rocket_mult
                
                # Check for shooting input based on aiming mode
                should_shoot = False
                if aiming_mode == AIM_ARROWS:
                    # Arrow key aiming: shoot with spacebar or any arrow key held
                    keys = pygame.key.get_pressed()
                    should_shoot = (keys[pygame.K_SPACE] or 
                                   keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or 
                                   keys[pygame.K_UP] or keys[pygame.K_DOWN])
                else:
                    # Mouse aiming: shoot with mouse button
                    should_shoot = pygame.mouse.get_pressed(3)[0]
                
                if should_shoot and player_time_since_shot >= effective_cooldown:
                    spawn_player_bullet_and_log()
                    player_time_since_shot = 0.0
                player_time_since_shot += dt

            # Update bouncing destructor shapes
            for ds in destructor_shapes[:]:
                ds["vel"].x += int(ds["vel"].x * dt)
                ds["vel"].y += int(ds["vel"].y * dt)
                ds["rect"].x += int(ds["vel"].x * dt)
                ds["rect"].y += int(ds["vel"].y * dt)
                
                # Bounce off walls
                if ds["rect"].left < 0 or ds["rect"].right > WIDTH:
                    ds["vel"].x = -ds["vel"].x
                if ds["rect"].top < 0 or ds["rect"].bottom > HEIGHT:
                    ds["vel"].y = -ds["vel"].y
                
                # Clamp to screen
                ds["rect"].x = max(0, min(ds["rect"].x, WIDTH - ds["rect"].w))
                ds["rect"].y = max(0, min(ds["rect"].y, HEIGHT - ds["rect"].h))
                
                # Check collision with destructible blocks
                for db in destructible_blocks[:]:
                    if ds["rect"].colliderect(db["rect"]):
                        db["hp"] -= ds.get("damage", 50) * dt * 60
                        if db["hp"] <= 0:
                            destructible_blocks.remove(db)
                
                # Check collision with moveable destructible blocks
                for mdb in moveable_destructible_blocks[:]:
                    if ds["rect"].colliderect(mdb["rect"]):
                        mdb["hp"] -= ds.get("damage", 50) * dt * 60
                        if mdb["hp"] <= 0:
                            moveable_destructible_blocks.remove(mdb)
                
                # Check collision with enemies
                for e in enemies[:]:
                    if ds["rect"].colliderect(e["rect"]):
                        e["hp"] -= ds.get("damage", 50) * dt * 60
                        if e["hp"] <= 0:
                            kill_enemy(e)
                
                # Check collision with player
                if ds["rect"].colliderect(player):
                    player_hp -= ds.get("damage", 50) * dt * 60
                    if player_hp <= 0:
                        deaths += 1
                        lives -= 1
                        if lives > 0:
                            state = STATE_CONTINUE
                        else:
                            state = STATE_GAME_OVER

            move_player_with_push(player, move_x, move_y, blocks)

            # Update moving health zone position
            zone = moving_health_zone
            if zone["target"] is None or (pygame.Vector2(zone["rect"].center) - zone["target"]).length() < 10:
                # Pick a new random target position
                zone["target"] = pygame.Vector2(
                    random.randint(100, WIDTH - 100),
                    random.randint(100, HEIGHT - 100)
                )
            
            # Move zone towards target
            zone_center = pygame.Vector2(zone["rect"].center)
            direction = (zone["target"] - zone_center)
            if direction.length() > 0:
                direction = direction.normalize()
                move_amount = zone["velocity"] * dt  # velocity is a scalar (float)
                move_vector = direction * move_amount  # direction is Vector2, move_amount is float, result is Vector2
                new_center = zone_center + move_vector
                zone["rect"].centerx = int(new_center.x)
                zone["rect"].centery = int(new_center.y)
                # Keep zone on screen
                zone["rect"].left = max(0, min(zone["rect"].left, WIDTH - zone["rect"].w))
                zone["rect"].top = max(0, min(zone["rect"].top, HEIGHT - zone["rect"].h))
            
            # Health recovery zone - heal player when inside
            current_frame_zones = set()
            if player.colliderect(zone["rect"]):
                zone_name = zone["name"]
                current_frame_zones.add(zone_name)
                
                # Log zone entry if just entered
                if zone_name not in player_current_zones:
                    telemetry.log_zone_visit(ZoneVisitEvent(
                        t=run_time,
                        zone_id=zone.get("zone_id"),
                        zone_name=zone_name,
                        zone_type="health_recovery",
                        event_type="enter",
                        x=player.centerx,
                        y=player.centery
                    ))
                
                heal_amount = zone["heal_rate"] * dt
                player_hp = min(player_max_hp, player_hp + heal_amount)
            
            # Log zone exits
            for zone_name in player_current_zones - current_frame_zones:
                telemetry.log_zone_visit(ZoneVisitEvent(
                    t=run_time,
                    zone_id=zone.get("zone_id"),
                    zone_name=zone_name,
                    zone_type="health_recovery",
                    event_type="exit",
                    x=player.centerx,
                    y=player.centery
                ))
            player_current_zones = current_frame_zones
            
            # Apply passive health regeneration (from pickups)
            if player_health_regen_rate > 0:
                regen_amount = player_health_regen_rate * dt
                player_hp = min(player_max_hp, player_hp + regen_amount)

            # Update timed buffs
            if fire_rate_buff_t > 0:
                fire_rate_buff_t = max(0.0, fire_rate_buff_t - dt)
            
            # Update pickup visual effects
            update_pickup_effects(dt)

            block_rects = [b["rect"] for b in blocks] + [b["rect"] for b in moveable_destructible_blocks] + [tb["bounding_rect"] for tb in trapezoid_blocks]
            # Cache player position to avoid recalculating
            player_pos_cached = pygame.Vector2(player.center)
            
            for e in enemies:
                e_pos = pygame.Vector2(e["rect"].center)
                
                # When 5 or fewer enemies remain, they move directly towards player
                if len(enemies) <= 5:
                    # Direct movement towards player (aggressive pursuit)
                    toward_threat = (pygame.Vector2(player.center) - e_pos)
                    if toward_threat.length_squared() > 0:
                        toward_threat = toward_threat.normalize()
                    else:
                        toward_threat = pygame.Vector2(0, 0)
                else:
                    # Find nearest threat (player or friendly AI)
                    threat_result = find_nearest_threat(e_pos)
                    if not threat_result:
                        continue
                    threat_pos, threat_type = threat_result
                    
                    # Base movement toward threat
                    toward_threat = (threat_pos - e_pos)
                    if toward_threat.length_squared() > 0:
                        toward_threat = toward_threat.normalize()
                    else:
                        toward_threat = pygame.Vector2(0, 0)
                
                # Check for nearby bullets to dodge (only check every other frame for performance)
                dodge_vector = pygame.Vector2(0, 0)
                # Only check dodge every other frame to improve performance
                if len(enemies) % 2 == 0 or enemies.index(e) % 2 == 0:
                    nearby_bullets = find_threats_in_dodge_range(e_pos, dodge_range=250.0)
                else:
                    nearby_bullets = []
                
                if nearby_bullets:
                    # Calculate dodge direction (away from nearest bullet)
                    closest_bullet = None
                    closest_dist = float("inf")
                    for bullet_pos in nearby_bullets:
                        dist = (bullet_pos - e_pos).length_squared()
                        if dist < closest_dist:
                            closest_dist = dist
                            closest_bullet = bullet_pos
                    
                    if closest_bullet:
                        # Move perpendicular to bullet direction
                        away_from_bullet = (e_pos - pygame.Vector2(closest_bullet))
                        if away_from_bullet.length_squared() > 0:
                            away_from_bullet = away_from_bullet.normalize()
                            # Add perpendicular component for better dodging
                            perp = pygame.Vector2(-away_from_bullet.y, away_from_bullet.x)
                            # Combine away + perpendicular for better dodge
                            dodge_vector = (away_from_bullet * 0.6 + perp * 0.4).normalize()
                
                # Combine threat pursuit with dodging (prioritize dodging if bullets are very close)
                if nearby_bullets and closest_dist < 15000:  # ~122 pixels squared
                    # Heavy dodge when bullet is very close
                    final_dir = dodge_vector * 1.5 + toward_threat * 0.3
                else:
                    # Normal pursuit with light dodging
                    final_dir = toward_threat * 0.9 + dodge_vector * 0.1
                
                if final_dir.length_squared() > 0:
                    final_dir = final_dir.normalize()
                
                # Update shield angle for shield enemies
                if e.get("has_shield"):
                    # Shield faces toward threat
                    if toward_threat.length_squared() > 0:
                        e["shield_angle"] = math.atan2(toward_threat.y, toward_threat.x)
                elif e.get("has_reflective_shield"):
                    # Reflective shield turns slowly toward threat
                    if toward_threat.length_squared() > 0:
                        target_angle = math.atan2(toward_threat.y, toward_threat.x)
                        current_angle = e.get("shield_angle", 0.0)
                        # Normalize angles
                        angle_diff = target_angle - current_angle
                        while angle_diff > math.pi:
                            angle_diff -= 2 * math.pi
                        while angle_diff < -math.pi:
                            angle_diff += 2 * math.pi
                        # Turn at limited speed
                        turn_speed = e.get("turn_speed", 0.5)
                        max_turn = turn_speed * dt
                        if abs(angle_diff) > max_turn:
                            e["shield_angle"] = current_angle + (max_turn if angle_diff > 0 else -max_turn)
                        else:
                            e["shield_angle"] = target_angle
                
                move_vec = final_dir * e["speed"] * dt
                dx_e = int(move_vec.x)
                dy_e = int(move_vec.y)
                
                if dx_e or dy_e:
                    # Enemies can push blocks out of the way to chase the player
                    move_enemy_with_push(e["rect"], dx_e, dy_e, blocks)

            # Friendly AI movement and behavior
            # Reuse block_rects from enemy movement (already computed above)
            for f in friendly_ai[:]:
                if f["hp"] <= 0:
                    friendly_ai.remove(f)
                    continue
                
                # Find target based on behavior
                f_pos = pygame.Vector2(f["rect"].center)
                target_enemy = find_nearest_enemy(f_pos)
                
                if target_enemy:
                    f["target"] = target_enemy
                    target_pos = pygame.Vector2(target_enemy["rect"].center)
                    dist_to_target = (target_pos - f_pos).length()
                    
                    # Behavior patterns
                    if f["behavior"] == "aggressive":
                        # Charge nearest enemy
                        move_dir = (target_pos - f_pos)
                        if move_dir.length_squared() > 0:
                            move_dir = move_dir.normalize()
                    elif f["behavior"] == "defensive":
                        # Stay near player, attack nearby enemies
                        player_pos = pygame.Vector2(player.center)
                        dist_to_player = (player_pos - f_pos).length()
                        if dist_to_target < 300 and dist_to_player < 200:
                            # Close to player and enemy nearby - attack
                            move_dir = (target_pos - f_pos)
                            if move_dir.length_squared() > 0:
                                move_dir = move_dir.normalize()
                        else:
                            # Return to player
                            move_dir = (player_pos - f_pos)
                            if move_dir.length_squared() > 0:
                                move_dir = move_dir.normalize() * 0.5  # Slower return
                    elif f["behavior"] == "ranged":
                        # Keep distance, snipe
                        if dist_to_target < 400:
                            # Too close, back away
                            move_dir = (f_pos - target_pos)
                            if move_dir.length_squared() > 0:
                                move_dir = move_dir.normalize()
                        else:
                            # Good distance, approach slowly
                            move_dir = (target_pos - f_pos)
                            if move_dir.length_squared() > 0:
                                move_dir = move_dir.normalize() * 0.3
                    elif f["behavior"] == "tank":
                        # Slow advance toward nearest enemy
                        move_dir = (target_pos - f_pos)
                        if move_dir.length_squared() > 0:
                            move_dir = move_dir.normalize() * 0.6
                    else:
                        # Default: follow player
                        player_pos = pygame.Vector2(player.center)
                        move_dir = (player_pos - f_pos)
                        if move_dir.length_squared() > 0:
                            move_dir = move_dir.normalize()
                else:
                    # No enemies, follow player
                    f["target"] = None
                    player_pos = pygame.Vector2(player.center)
                    move_dir = (player_pos - f_pos)
                    if move_dir.length_squared() > 0:
                        move_dir = move_dir.normalize() * 0.5
                
                # Apply movement
                if move_dir.length_squared() > 0:
                    move_vec = move_dir * f["speed"] * dt
                    dx_f = int(move_vec.x)
                    dy_f = int(move_vec.y)
                    if dx_f or dy_f:
                        if can_move_rect(f["rect"], dx_f, dy_f, block_rects):
                            f["rect"].x += dx_f
                            f["rect"].y += dy_f
                        else:
                            if dx_f and can_move_rect(f["rect"], dx_f, 0, block_rects):
                                f["rect"].x += dx_f
                            if dy_f and can_move_rect(f["rect"], 0, dy_f, block_rects):
                                f["rect"].y += dy_f
                        clamp_rect_to_screen(f["rect"])

            # Position sampling
            pos_timer += dt
            if pos_timer >= POS_SAMPLE_INTERVAL:
                pos_timer -= POS_SAMPLE_INTERVAL
                telemetry.log_player_position(PlayerPosEvent(t=run_time, x=player.x, y=player.y))
                
                # Log player velocity
                telemetry.log_player_velocity(
                    PlayerVelocityEvent(
                        t=run_time,
                        x=player.x,
                        y=player.y,
                        vel_x=float(last_move_velocity.x),
                        vel_y=float(last_move_velocity.y),
                        speed=float(last_move_velocity.length()),
                    )
                )
                
                # Log enemy positions (reduced frequency for performance)
                # Only log every 3rd enemy to reduce telemetry overhead
                for i, e in enumerate(enemies):
                    if i % 3 == 0:  # Sample every 3rd enemy
                        e_pos = pygame.Vector2(e["rect"].center)
                        # Use cached player position
                        dir_vec = vec_toward(e["rect"].centerx, e["rect"].centery, player_pos_cached.x, player_pos_cached.y)
                        vel_vec = dir_vec * e["speed"]
                        telemetry.log_enemy_position(
                            EnemyPositionEvent(
                                t=run_time,
                                enemy_type=e["type"],
                                x=e["rect"].x,
                                y=e["rect"].y,
                                speed=float(e["speed"]),
                                vel_x=float(vel_vec.x),
                                vel_y=float(vel_vec.y),
                            )
                        )
                
                # Log friendly AI positions (reduced frequency for performance)
                # Only log every 2nd friendly to reduce telemetry overhead
                for i, f in enumerate(friendly_ai):
                    if i % 2 == 0:  # Sample every 2nd friendly
                        if f["target"]:
                            target_type = f["target"].get("type")
                            vel_vec = vec_toward(f["rect"].centerx, f["rect"].centery, f["target"]["rect"].centerx, f["target"]["rect"].centery) * f["speed"]
                        else:
                            target_type = None
                            vel_vec = pygame.Vector2(0, 0)
                        telemetry.log_friendly_position(
                            FriendlyAIPositionEvent(
                                t=run_time,
                                friendly_type=f["type"],
                                x=f["rect"].x,
                                y=f["rect"].y,
                                speed=float(f["speed"]),
                                vel_x=float(vel_vec.x),
                                vel_y=float(vel_vec.y),
                                target_enemy_type=target_type,
                            )
                        )

            # Friendly AI shooting
            for f in friendly_ai:
                f["time_since_shot"] += dt
                if f["target"] and f["time_since_shot"] >= f["shoot_cooldown"]:
                    # Check if target is still alive and in range
                    if f["target"] in enemies:
                        target_pos = pygame.Vector2(f["target"]["rect"].center)
                        f_pos = pygame.Vector2(f["rect"].center)
                        dist = (target_pos - f_pos).length()
                        # Shoot if in range (varies by behavior)
                        max_range = 600 if f["behavior"] == "ranged" else 400
                        if dist <= max_range:
                            spawn_friendly_projectile(f, f["target"])
                            f["time_since_shot"] = 0.0
                    else:
                        f["target"] = None

            # Enemy shooting
            for e in enemies:
                e["time_since_shot"] += dt
                
                # Boss phase detection and special shooting
                if e.get("is_boss", False):
                    hp_ratio = e["hp"] / e["max_hp"]
                    # Check phase transitions
                    if e["phase"] == 1 and hp_ratio <= e["phase_hp_thresholds"][0]:
                        e["phase"] = 2
                        e["shoot_cooldown"] = 0.3  # Faster shooting in phase 2
                        e["color"] = (255, 100, 0)  # Orange
                    elif e["phase"] == 2 and hp_ratio <= e["phase_hp_thresholds"][1]:
                        e["phase"] = 3
                        e["shoot_cooldown"] = 0.15  # Very fast shooting in phase 3
                        e["color"] = (255, 0, 255)  # Magenta
                    
                    # Boss shooting patterns based on phase
                    if e["time_since_shot"] >= e["shoot_cooldown"]:
                        if e["phase"] == 1:
                            # Phase 1: Single shots
                            spawn_enemy_projectile(e)
                        elif e["phase"] == 2:
                            # Phase 2: Triple shot spread at nearest threat
                            e_pos = pygame.Vector2(e["rect"].center)
                            threat_result = find_nearest_threat(e_pos)
                            if threat_result:
                                threat_pos, _ = threat_result
                                base_dir = vec_toward(e_pos.x, e_pos.y, threat_pos.x, threat_pos.y)
                            else:
                                base_dir = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                            for angle in [-15, 0, 15]:
                                dir_vec = base_dir.rotate(angle)
                                spawn_boss_projectile(e, dir_vec)
                        elif e["phase"] == 3:
                            # Phase 3: 8-way spread (still targets nearest threat for base direction)
                            e_pos = pygame.Vector2(e["rect"].center)
                            threat_result = find_nearest_threat(e_pos)
                            if threat_result:
                                threat_pos, _ = threat_result
                                base_dir = vec_toward(e_pos.x, e_pos.y, threat_pos.x, threat_pos.y)
                            else:
                                base_dir = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                            for angle in range(0, 360, 45):
                                dir_vec = base_dir.rotate(angle)
                                spawn_boss_projectile(e, dir_vec)
                        e["time_since_shot"] = 0.0
                elif e["time_since_shot"] >= e["shoot_cooldown"]:
                    # Reflective shield enemies don't shoot
                    if not e.get("has_reflective_shield", False):
                        spawn_enemy_projectile(e)
                    e["time_since_shot"] = 0.0

            # Pickup spawning (affected by difficulty)
            if state == STATE_PLAYING or state == STATE_ENDURANCE:
                # Use cached multiplier if available, otherwise calculate
                if 'diff_mult' in locals():
                    effective_spawn_interval = PICKUP_SPAWN_INTERVAL / diff_mult["pickup_spawn"]
                else:
                    diff_mult = difficulty_multipliers[difficulty]
                    effective_spawn_interval = PICKUP_SPAWN_INTERVAL / diff_mult["pickup_spawn"]
            else:
                effective_spawn_interval = PICKUP_SPAWN_INTERVAL
            pickup_spawn_timer += dt
            if pickup_spawn_timer >= effective_spawn_interval:
                pickup_spawn_timer = 0.0
                # Randomize pickup type - player never knows what they'll get
                pickup_types = [
                    "boost",  # temporary boost meter refill
                    "firerate",  # temporary fire rate buff
                    "spawn_boost",  # enemy can grab, player can shoot
                    "max_health",  # permanent max HP increase
                    "health_regen",  # increases health regeneration rate
                    "speed",  # permanent speed increase
                    "firerate_permanent",  # permanent fire rate increase
                    "bullet_size",  # permanent bullet size increase
                    "bullet_speed",  # permanent bullet speed increase
                    "bullet_damage",  # permanent bullet damage increase
                    "bullet_knockback",  # permanent knockback increase
                    "bullet_penetration",  # permanent penetration increase
                    "bullet_explosion",  # permanent explosion radius increase
                    "giant_bullets",  # 10x bullet size
                    "triple_shot",  # shoot 3 beams
                    "bouncing_bullets",  # bullets bounce off walls
                    "rocket_launcher",  # slower fire rate, more damage, AOE
                    "overshield",  # adds overshield (extra health bar)
                ]
                spawn_pickup(random.choice(pickup_types))

            # Update pickup timers and remove expired pickups
            for p in pickups[:]:
                p["timer"] = p.get("timer", 15.0) - dt
                p["age"] = p.get("age", 0.0) + dt
                if p.get("timer", 15.0) <= 0.0:
                    pickups.remove(p)
                    continue

            # Pickup interactions
            for p in pickups[:]:
                pr = p["rect"]
                ptype = p["type"]

                # Player collects beneficial pickups
                if ptype != "spawn_boost" and pr.colliderect(player):
                    apply_pickup_effect(ptype)
                    # Create pickup collection effect (particles)
                    create_pickup_collection_effect(pr.centerx, pr.centery, p["color"])
                    pickups.remove(p)
                    continue

                # Enemies can collect spawn boost pickup
                if ptype == "spawn_boost":
                    grabbed = False
                    for e in enemies:
                        if pr.colliderect(e["rect"]):
                            enemy_spawn_boost_level = min(10, enemy_spawn_boost_level + 1)
                            # also make current wave a bit scarier by slightly reducing remaining respawn delay
                            wave_respawn_delay = max(0.8, wave_respawn_delay - 0.15)
                            grabbed = True
                            break
                    if grabbed:
                        pickups.remove(p)
                        continue

            # Friendly projectiles update
            for fp in friendly_projectiles[:]:
                fp["rect"].x += int(fp["vel"].x * dt)
                fp["rect"].y += int(fp["vel"].y * dt)
                
                if rect_offscreen(fp["rect"]):
                    friendly_projectiles.remove(fp)
                    continue
                
                # Check collision with enemies
                hit_enemy = None
                for e in enemies:
                    if fp["rect"].colliderect(e["rect"]):
                        hit_enemy = e
                        break
                
                if hit_enemy:
                    hit_enemy["hp"] -= fp["damage"]
                    damage_dealt += fp["damage"]
                    # Log friendly AI hit
                    telemetry.log_enemy_hit(
                        EnemyHitEvent(
                            t=run_time,
                            enemy_type=hit_enemy["type"],
                            enemy_x=hit_enemy["rect"].x,
                            enemy_y=hit_enemy["rect"].y,
                            damage=fp["damage"],
                            enemy_hp_after=hit_enemy["hp"],
                            killed=hit_enemy["hp"] <= 0,
                        )
                    )
                    if hit_enemy["hp"] <= 0:
                        kill_enemy(hit_enemy)
                    friendly_projectiles.remove(fp)
                    continue
                
                # Check collision with blocks
                for blk in blocks:
                    if fp["rect"].colliderect(blk["rect"]):
                        friendly_projectiles.remove(fp)
                        break
                
                # Check collision with trapezoid blocks
                for tb in trapezoid_blocks:
                    if fp["rect"].colliderect(tb["bounding_rect"]):
                        friendly_projectiles.remove(fp)
                        break
                
                # Check collision with moveable destructible blocks
                for mdb in moveable_destructible_blocks:
                    if fp["rect"].colliderect(mdb["rect"]):
                        friendly_projectiles.remove(fp)
                        break

            # Player bullets update
            for b in player_bullets[:]:
                r = b["rect"]
                v = b["vel"]
                r.x += int(v.x * dt)
                r.y += int(v.y * dt)

                # Handle bouncing bullets
                bounces_left = b.get("bounces", 0)
                if bounces_left > 0:
                    bounced = False
                    if r.left < 0:
                        v.x = abs(v.x)
                        bounced = True
                    elif r.right > WIDTH:
                        v.x = -abs(v.x)
                        bounced = True
                    if r.top < 0:
                        v.y = abs(v.y)
                        bounced = True
                    elif r.bottom > HEIGHT:
                        v.y = -abs(v.y)
                        bounced = True
                    if bounced:
                        b["bounces"] = bounces_left - 1
                        b["vel"] = v
                        # Keep bullet on screen
                        r.x = max(0, min(r.x, WIDTH - r.w))
                        r.y = max(0, min(r.y, HEIGHT - r.h))

                if rect_offscreen(r) and bounces_left == 0:
                    if b in player_bullets:
                        player_bullets.remove(b)
                    continue

                # bullets can destroy spawn_boost pickups
                hit_pickup = None
                for p in pickups:
                    if p["type"] == "spawn_boost" and r.colliderect(p["rect"]):
                        hit_pickup = p
                        break
                if hit_pickup is not None:
                    try:
                        pickups.remove(hit_pickup)
                    except ValueError:
                        pass
                    if b in player_bullets:
                        player_bullets.remove(b)
                    continue

                # bullet hits enemy
                hit_enemy_index = None
                for i, e in enumerate(enemies):
                    if r.colliderect(e["rect"]):
                        hit_enemy_index = i
                        break

                if hit_enemy_index is not None:
                    hits += 1
                    e = enemies[hit_enemy_index]
                    bullet_damage = b.get("damage", player_bullet_damage)
                    
                    # Check for shield enemies
                    if e.get("has_shield"):
                        # Check if bullet hit the shield (front-facing line)
                        shield_angle = e.get("shield_angle", 0.0)
                        shield_length = e.get("shield_length", 50)
                        enemy_center = pygame.Vector2(e["rect"].center)
                        bullet_pos = pygame.Vector2(r.center)
                        
                        # Calculate shield line endpoints
                        shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                        shield_start = enemy_center + shield_dir * (e["rect"].w // 2)
                        shield_end = enemy_center + shield_dir * (e["rect"].w // 2 + shield_length)
                        
                        # Check if bullet is in front of enemy (shield side)
                        to_bullet = bullet_pos - enemy_center
                        dot_product = to_bullet.dot(shield_dir)
                        
                        if dot_product > 0:  # Bullet is in front
                            # Check distance to shield line
                            line_vec = shield_end - shield_start
                            if line_vec.length_squared() > 0:
                                t = max(0, min(1, (bullet_pos - shield_start).dot(line_vec) / line_vec.length_squared()))
                                closest_point = shield_start + line_vec * t
                                dist_to_shield = (bullet_pos - closest_point).length()
                                
                                if dist_to_shield < 15:  # Bullet hit shield
                                    # Shield blocks damage, remove bullet
                                    if b in player_bullets:
                                        player_bullets.remove(b)
                                    continue
                        
                        # Bullet hit from behind/side, apply damage normally
                        e["hp"] -= bullet_damage
                        damage_dealt += bullet_damage
                    elif e.get("has_reflective_shield"):
                        # Reflective shield - check if hit shield
                        shield_angle = e.get("shield_angle", 0.0)
                        shield_length = e.get("shield_length", 60)
                        enemy_center = pygame.Vector2(e["rect"].center)
                        bullet_pos = pygame.Vector2(r.center)
                        
                        shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                        shield_start = enemy_center + shield_dir * (e["rect"].w // 2)
                        shield_end = enemy_center + shield_dir * (e["rect"].w // 2 + shield_length)
                        
                        to_bullet = bullet_pos - enemy_center
                        dot_product = to_bullet.dot(shield_dir)
                        
                        if dot_product > 0:  # Bullet is in front
                            line_vec = shield_end - shield_start
                            if line_vec.length_squared() > 0:
                                t = max(0, min(1, (bullet_pos - shield_start).dot(line_vec) / line_vec.length_squared()))
                                closest_point = shield_start + line_vec * t
                                dist_to_shield = (bullet_pos - closest_point).length()
                                
                                if dist_to_shield < 20:  # Bullet hit reflective shield
                                    # Reflect bullet back at player
                                    e["shield_hp"] += bullet_damage
                                    # Calculate reflection direction
                                    normal = -shield_dir  # Normal to shield
                                    incoming = b["vel"].normalize()
                                    reflected = incoming - 2 * incoming.dot(normal) * normal
                                    
                                    # Spawn reflected projectile
                                    reflected_proj = {
                                        "rect": pygame.Rect(r.x, r.y, r.w, r.h),
                                        "vel": reflected * b["vel"].length(),
                                        "enemy_type": "reflector",
                                        "color": (255, 200, 100),
                                        "shape": "circle",
                                        "bounces": 0,
                                    }
                                    enemy_projectiles.append(reflected_proj)
                                    if b in player_bullets:
                                        player_bullets.remove(b)
                                    continue
                        
                        # Bullet hit from behind/side, apply damage normally
                        e["hp"] -= bullet_damage
                        damage_dealt += bullet_damage
                    else:
                        # Normal enemy, apply damage
                        e["hp"] -= bullet_damage
                        damage_dealt += bullet_damage

                    # Apply knockback if available
                    knockback = b.get("knockback", 0.0)
                    if knockback > 0.0:
                        knockback_vec = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                        e["rect"].x += int(knockback_vec.x * knockback * 5)
                        e["rect"].y += int(knockback_vec.y * knockback * 5)
                        clamp_rect_to_screen(e["rect"])

                    # Handle explosion if available
                    explosion_radius = b.get("explosion_radius", 0.0)
                    if explosion_radius > 0.0:
                        exp_center = pygame.Vector2(b["rect"].center)
                        for other_e in enemies:
                            if other_e is e:
                                continue
                            dist = pygame.Vector2(other_e["rect"].center).distance_to(exp_center)
                            if dist <= explosion_radius:
                                # Damage falls off with distance
                                exp_damage = int(bullet_damage * (1.0 - dist / explosion_radius) * 0.6)
                                if exp_damage > 0:
                                    other_e["hp"] -= exp_damage
                                    damage_dealt += exp_damage
                                    # Log explosion hit
                                    telemetry.log_enemy_hit(
                                        EnemyHitEvent(
                                            t=run_time,
                                            enemy_type=other_e["type"],
                                            enemy_x=other_e["rect"].x,
                                            enemy_y=other_e["rect"].y,
                                            damage=exp_damage,
                                            enemy_hp_after=max(0, other_e["hp"]),
                                            killed=other_e["hp"] <= 0,
                                        )
                                    )
                                    if other_e["hp"] <= 0:
                                        kill_enemy(other_e)

                    killed = e["hp"] <= 0
                    hp_after = max(0, e["hp"])

                    telemetry.log_enemy_hit(
                        EnemyHitEvent(
                            t=run_time,
                            enemy_type=e["type"],
                            enemy_x=e["rect"].x,
                            enemy_y=e["rect"].y,
                            damage=bullet_damage,
                            enemy_hp_after=hp_after,
                            killed=killed,
                        )
                    )

                    # Handle penetration
                    penetration = b.get("penetration", 0)
                    if penetration > 0:
                        # Bullet can pierce through
                        b["penetration"] = penetration - 1
                        # Continue to next enemy if penetration remains
                        if b["penetration"] > 0:
                            continue
                    else:
                        # No penetration left, remove bullet
                        if b in player_bullets:
                            player_bullets.remove(b)

                    if killed:
                        kill_enemy(e)

                    # If bullet was removed, continue to next bullet
                    if b not in player_bullets:
                        continue

                # bullets interact with indestructible blocks
                for blk in blocks:
                    if r.colliderect(blk["rect"]):
                        # Bouncing bullets can bounce off blocks too
                        if b.get("bounces", 0) > 0:
                            # Simple bounce: reverse velocity
                            b["vel"] = -b["vel"]
                            b["bounces"] = b.get("bounces", 0) - 1
                        else:
                            if b in player_bullets:
                                player_bullets.remove(b)
                            break
                
                # Bullets interact with trapezoid blocks
                for tb in trapezoid_blocks:
                    if r.colliderect(tb["bounding_rect"]):
                        # Bouncing bullets can bounce off trapezoids too
                        if b.get("bounces", 0) > 0:
                            # Simple bounce: reverse velocity
                            b["vel"] = -b["vel"]
                            b["bounces"] = b.get("bounces", 0) - 1
                        else:
                            if b in player_bullets:
                                player_bullets.remove(b)
                            break
                
                # Player bullets can destroy destructible blocks
                for db in destructible_blocks[:]:
                    if r.colliderect(db["rect"]):
                        bullet_damage = b.get("damage", player_bullet_damage)
                        db["hp"] -= bullet_damage
                        if db["hp"] <= 0:
                            destructible_blocks.remove(db)
                        # Remove bullet unless it has penetration
                        if b.get("penetration", 0) == 0 and b in player_bullets:
                            player_bullets.remove(b)
                        break
                
                # Player bullets can destroy moveable destructible blocks
                for mdb in moveable_destructible_blocks[:]:
                    if r.colliderect(mdb["rect"]):
                        bullet_damage = b.get("damage", player_bullet_damage)
                        mdb["hp"] -= bullet_damage
                        if mdb["hp"] <= 0:
                            moveable_destructible_blocks.remove(mdb)
                        # Remove bullet unless it has penetration
                        if b.get("penetration", 0) == 0 and b in player_bullets:
                            player_bullets.remove(b)
                        break
                if b not in player_bullets:
                    continue

            # Enemy projectiles update
            for p in enemy_projectiles[:]:
                r = p["rect"]
                v = p["vel"]
                r.x += int(v.x * dt)
                r.y += int(v.y * dt)

                # Handle bouncing enemy projectiles
                bounces_left = p.get("bounces", 0)
                if bounces_left > 0:
                    bounced = False
                    if r.left < 0:
                        v.x = abs(v.x)
                        bounced = True
                    elif r.right > WIDTH:
                        v.x = -abs(v.x)
                        bounced = True
                    if r.top < 0:
                        v.y = abs(v.y)
                        bounced = True
                    elif r.bottom > HEIGHT:
                        v.y = -abs(v.y)
                        bounced = True
                    if bounced:
                        p["bounces"] = bounces_left - 1
                        p["vel"] = v
                        # Keep projectile on screen
                        r.x = max(0, min(r.x, WIDTH - r.w))
                        r.y = max(0, min(r.y, HEIGHT - r.h))

                if rect_offscreen(r) and bounces_left == 0:
                    enemy_projectiles.remove(p)
                    continue

                # Enemy projectiles can damage destructible blocks
                for db in destructible_blocks[:]:
                    if r.colliderect(db["rect"]):
                        db["hp"] -= enemy_projectile_damage
                        if db["hp"] <= 0:
                            destructible_blocks.remove(db)
                        enemy_projectiles.remove(p)
                        break
                if p not in enemy_projectiles:
                    continue
                
                # Enemy projectiles can damage moveable destructible blocks
                for mdb in moveable_destructible_blocks[:]:
                    if r.colliderect(mdb["rect"]):
                        mdb["hp"] -= enemy_projectile_damage
                        if mdb["hp"] <= 0:
                            moveable_destructible_blocks.remove(mdb)
                        enemy_projectiles.remove(p)
                        break
                if p not in enemy_projectiles:
                    continue

                # Check collision with friendly AI first
                hit_friendly = None
                for f in friendly_ai:
                    if r.colliderect(f["rect"]):
                        hit_friendly = f
                        break
                
                if hit_friendly:
                    hit_friendly["hp"] -= enemy_projectile_damage
                    if hit_friendly["hp"] <= 0:
                        # Log friendly AI death
                        telemetry.log_friendly_death(
                            FriendlyAIDeathEvent(
                                t=run_time,
                                friendly_type=hit_friendly["type"],
                                x=hit_friendly["rect"].x,
                                y=hit_friendly["rect"].y,
                                killed_by="enemy_projectile",
                            )
                        )
                        friendly_ai.remove(hit_friendly)
                    enemy_projectiles.remove(p)
                    continue

                if r.colliderect(player):
                    # Check if shield is active - shield blocks all damage
                    if shield_active:
                        # Shield blocks the projectile
                        enemy_projectiles.remove(p)
                        continue
                    
                    # apply damage - overshield absorbs damage first
                    remaining_damage = enemy_projectile_damage
                    if overshield > 0:
                        if overshield >= remaining_damage:
                            overshield -= remaining_damage
                            remaining_damage = 0
                        else:
                            remaining_damage -= overshield
                            overshield = 0
                    
                    # Apply remaining damage to player HP
                    if remaining_damage > 0:
                        player_hp -= remaining_damage
                    damage_taken += enemy_projectile_damage

                    if player_hp < 0:
                        player_hp = 0

                    telemetry.log_player_damage(
                        PlayerDamageEvent(
                            t=run_time,
                            amount=enemy_projectile_damage,
                            source_type="enemy_projectile",
                            source_enemy_type=p.get("enemy_type"),
                            player_x=player.x,
                            player_y=player.y,
                            player_hp_after=player_hp,
                        )
                    )

                    enemy_projectiles.remove(p)

                    # death handling
                    if player_hp <= 0:
                        deaths += 1
                        lives -= 1

                        telemetry.log_player_death(
                            PlayerDeathEvent(
                                t=run_time,
                                player_x=player.x,
                                player_y=player.y,
                                lives_left=lives,
                            )
                        )

                        if lives > 0:
                            state = STATE_CONTINUE
                            continue_blink_t = 0.0
                            continue
                        else:
                            # Game over - offer endurance mode
                            state = STATE_GAME_OVER

                    continue

                # projectiles collide with blocks
                for blk in blocks:
                    if r.colliderect(blk["rect"]):
                        if p in enemy_projectiles:
                            enemy_projectiles.remove(p)
                        break
                
                # Enemy projectiles collide with trapezoid blocks
                for tb in trapezoid_blocks:
                    if r.colliderect(tb["bounding_rect"]):
                        if p in enemy_projectiles:
                            enemy_projectiles.remove(p)
                        break
                
                # Enemy projectiles also collide with moveable destructible blocks (non-bouncing only)
                if bounces_left == 0:
                    for mdb in moveable_destructible_blocks:
                        if r.colliderect(mdb["rect"]):
                            if p in enemy_projectiles:
                                enemy_projectiles.remove(p)
                            break

            telemetry.tick(dt)

        else:
            # allow background flush timing while paused/continue screen
            telemetry.tick(dt_real)

        # --- Draw ---
        # Apply level theme
        theme = level_themes.get(current_level, level_themes[1])
        screen.fill(theme["bg_color"])
        
        # Victory screen - all levels completed!
        if state == STATE_VICTORY:
            theme = level_themes.get(current_level, level_themes[1])
            screen.fill(theme["bg_color"])
            draw_centered_text("VICTORY!", 200, (100, 255, 100), use_big=True)
            draw_centered_text("All Levels Completed!", 280, (150, 255, 150))
            draw_centered_text(f"Final Score: {score:,}", 350, (255, 255, 100))
            draw_centered_text(f"Levels Completed: {max_level}", 400, (200, 200, 255))
            draw_centered_text(f"Time Survived: {int(survival_time//60)}m {int(survival_time%60)}s", 450, (200, 200, 255))
            draw_centered_text("Press E for Endurance Mode", 550, (100, 255, 100))
            draw_centered_text("Press ESC to Quit", 600, (200, 200, 200))
            pygame.display.flip()
            continue
        
        # Game Over screen
        if state == STATE_GAME_OVER:
            theme = level_themes.get(current_level, level_themes[1])
            screen.fill(theme["bg_color"])
            draw_centered_text("GAME OVER", 200, (255, 100, 100), use_big=True)
            draw_centered_text(f"Final Score: {score:,}", 300, (255, 255, 100))
            draw_centered_text(f"Waves Survived: {wave_number - 1}", 350, (200, 200, 255))
            draw_centered_text(f"Time Survived: {int(survival_time//60)}m {int(survival_time%60)}s", 400, (200, 200, 255))
            draw_centered_text("Press E for Endurance Mode", 550, (100, 255, 100))
            draw_centered_text("Press ESC to Quit", 600, (200, 200, 200))
            pygame.display.flip()
            continue
        
        # Menu screen
        if state == STATE_MENU:
            draw_centered_text("MOUSE AIM SHOOTER", 150, (255, 255, 255), use_big=True)
            
            # Menu sections: 0 = difficulty, 1 = aiming, 2 = class, 3 = options, 4 = start
            if menu_section == 0:
                draw_centered_text("Select Difficulty", 250, (200, 200, 200))
                y_start = 350
                for i, diff_option in enumerate(difficulty_options):
                    color = (255, 255, 100) if i == difficulty_selected else (150, 150, 150)
                    prefix = "> " if i == difficulty_selected else "  "
                    draw_centered_text(f"{prefix}{diff_option}", y_start + i * 50, color)
                draw_centered_text("Press UP/DOWN to select, RIGHT to continue", 600, (150, 150, 150))
            elif menu_section == 1:
                draw_centered_text("Select Aiming Mode", 250, (200, 200, 200))
                aiming_options = ["Mouse", "Arrow Keys"]
                y_start = 350
                for i, aim_option in enumerate(aiming_options):
                    color = (255, 255, 100) if i == aiming_mode_selected else (150, 150, 150)
                    prefix = "> " if i == aiming_mode_selected else "  "
                    draw_centered_text(f"{prefix}{aim_option}", y_start + i * 50, color)
                draw_centered_text("Press UP/DOWN to select, RIGHT to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 2:
                draw_centered_text("Select Player Class", 250, (200, 200, 200))
                class_names = ["Balanced", "Tank", "Speedster", "Sniper"]
                y_start = 350
                for i, class_name in enumerate(class_names):
                    color = (255, 255, 100) if i == player_class_selected else (150, 150, 150)
                    prefix = "> " if i == player_class_selected else "  "
                    draw_centered_text(f"{prefix}{class_name}", y_start + i * 50, color)
                # Show class stats
                selected_class = player_class_options[player_class_selected]
                stats = player_class_stats[selected_class]
                draw_centered_text(f"HP: {stats['hp_mult']:.1f}x | Speed: {stats['speed_mult']:.1f}x | Damage: {stats['damage_mult']:.1f}x | Fire Rate: {stats['firerate_mult']:.1f}x", 550, (150, 150, 255))
                draw_centered_text("Press UP/DOWN to select, RIGHT to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 3:
                draw_centered_text("Options", 250, (200, 200, 200))
                metrics_options = ["Show Metrics", "Hide Metrics"]
                y_start = 350
                for i, opt in enumerate(metrics_options):
                    color = (255, 255, 100) if i == ui_show_metrics_selected else (150, 150, 150)
                    prefix = "> " if i == ui_show_metrics_selected else "  "
                    draw_centered_text(f"{prefix}{opt}", y_start + i * 50, color)
                draw_centered_text("Press UP/DOWN to select, RIGHT to continue, LEFT to go back", 600, (150, 150, 150))
            elif menu_section == 4:
                draw_centered_text("Ready to Start", 300, (100, 255, 100))
                draw_centered_text(f"Difficulty: {difficulty_options[difficulty_selected]}", 400, (200, 200, 200))
                draw_centered_text(f"Aiming: {['Mouse', 'Arrow Keys'][aiming_mode_selected]}", 450, (200, 200, 200))
                draw_centered_text(f"Class: {['Balanced', 'Tank', 'Speedster', 'Sniper'][player_class_selected]}", 500, (200, 200, 200))
                draw_centered_text(f"Metrics: {['Show', 'Hide'][ui_show_metrics_selected]}", 550, (200, 200, 200))
                draw_centered_text("Press ENTER to Start", 600, (100, 255, 100))
                draw_centered_text("Press LEFT to go back, ESC to Quit", 650, (150, 150, 150))
            
            pygame.display.flip()
            continue

        # Draw trapezoid blocks hanging off screen edges (draw first so they appear behind other blocks)
        for tb in trapezoid_blocks:
            # Draw trapezoid as polygon
            pygame.draw.polygon(screen, tb["color"], tb["points"])
            # Draw border to indicate indestructible
            pygame.draw.polygon(screen, (255, 255, 255), tb["points"], 3)
            # Draw pattern lines on visible portion (only draw lines within screen bounds)
            visible_points = [(x, y) for x, y in tb["points"] if 0 <= x <= WIDTH and 0 <= y <= HEIGHT]
            if len(visible_points) >= 2:
                # Draw some pattern lines on the visible portion
                for i in range(0, len(visible_points) - 1):
                    pygame.draw.line(screen, (tb["color"][0] + 20, tb["color"][1] + 20, tb["color"][2] + 20),
                                    visible_points[i], visible_points[i + 1], 2)
        
        # Indestructible blocks drawn with destructible blocks (see below)
        
        # Draw moving health recovery zone (semi-transparent green)
        zone = moving_health_zone
        zone_surf = pygame.Surface((zone["rect"].w, zone["rect"].h), pygame.SRCALPHA)
        pygame.draw.rect(zone_surf, zone["color"], (0, 0, zone["rect"].w, zone["rect"].h))
        screen.blit(zone_surf, zone["rect"].topleft)
        # Draw border with pulsing effect
        pulse = 0.5 + 0.5 * math.sin(run_time * 3.0)
        border_alpha = int(150 + 100 * pulse)
        border_color = (50, 255, 50)
        pygame.draw.rect(screen, border_color, zone["rect"], 3)
        
        # Draw destructible blocks with textures (cracked appearance)
        for db in destructible_blocks:
            # Calculate crack level based on HP
            hp_ratio = db["hp"] / db["max_hp"]
            if hp_ratio < 0.33:
                crack_level = 3  # Heavily cracked
            elif hp_ratio < 0.66:
                crack_level = 2  # Moderately cracked
            else:
                crack_level = 1  # Slightly cracked
            
            # Base color with cracks
            base_color = db["color"]
            pygame.draw.rect(screen, base_color, db["rect"])
            
            # Draw crack texture
            if crack_level >= 2:
                # Draw crack lines
                crack_color = (50, 50, 50)
                center = db["rect"].center
                # Random crack pattern
                for i in range(crack_level):
                    angle = (i * 2.4) * math.pi / 3
                    end_x = center[0] + math.cos(angle) * (db["rect"].w // 2)
                    end_y = center[1] + math.sin(angle) * (db["rect"].h // 2)
                    pygame.draw.line(screen, crack_color, center, (end_x, end_y), 2)
            
            # Health bar only if enabled
            if ui_show_block_health_bars:
                draw_health_bar(db["rect"].x, db["rect"].y - 10, db["rect"].w, 6, db["hp"], db["max_hp"])
        
        # Draw moveable destructible blocks (can be pushed and destroyed)
        for mdb in moveable_destructible_blocks:
            # Calculate crack level based on HP
            hp_ratio = mdb["hp"] / mdb["max_hp"]
            if hp_ratio < 0.33:
                crack_level = 3  # Heavily cracked
            elif hp_ratio < 0.66:
                crack_level = 2  # Moderately cracked
            else:
                crack_level = 1  # Slightly cracked
            
            # Base color with cracks
            base_color = mdb["color"]
            pygame.draw.rect(screen, base_color, mdb["rect"])
            
            # Draw crack texture
            if crack_level >= 2:
                # Draw crack lines
                crack_color = (50, 50, 50)
                center = mdb["rect"].center
                # Random crack pattern
                for i in range(crack_level):
                    angle = (i * 2.4) * math.pi / 3
                    end_x = center[0] + math.cos(angle) * (mdb["rect"].w // 2)
                    end_y = center[1] + math.sin(angle) * (mdb["rect"].h // 2)
                    pygame.draw.line(screen, crack_color, center, (end_x, end_y), 2)
            
            # Draw border to indicate it's moveable (different from regular destructible)
            pygame.draw.rect(screen, (255, 200, 100), mdb["rect"], 2)  # Orange border for moveable
            
            # Health bar only if enabled
            if ui_show_block_health_bars:
                draw_health_bar(mdb["rect"].x, mdb["rect"].y - 10, mdb["rect"].w, 6, mdb["hp"], mdb["max_hp"])
        
        # Draw indestructible blocks with texture (solid appearance)
        for blk in blocks:
            # Draw with pattern/texture to show it's indestructible
            pygame.draw.rect(screen, blk["color"], blk["rect"])
            # Draw border to indicate indestructible
            pygame.draw.rect(screen, (255, 255, 255), blk["rect"], 3)
            # Draw pattern lines
            for i in range(0, blk["rect"].w, 10):
                pygame.draw.line(screen, (blk["color"][0] + 20, blk["color"][1] + 20, blk["color"][2] + 20),
                                (blk["rect"].x + i, blk["rect"].y),
                                (blk["rect"].x + i, blk["rect"].y + blk["rect"].h), 1)

        # Draw pickup particles (glow effect)
        for particle in pickup_particles:
            particle_surf = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
            color_with_alpha = (*particle["color"], particle["alpha"])
            pygame.draw.circle(particle_surf, color_with_alpha, (particle["size"], particle["size"]), particle["size"])
            screen.blit(particle_surf, (particle["x"] - particle["size"], particle["y"] - particle["size"]))
        
        # Draw pickups with pulsing effect
        for pu in pickups:
            age = pu.get("age", 0.0)
            pulse = (math.sin(age * 4.0) + 1.0) / 2.0
            # Draw glow ring
            glow_surf = pygame.Surface((pu["rect"].w + 20, pu["rect"].h + 20), pygame.SRCALPHA)
            glow_alpha = int(80 + pulse * 60)
            glow_color = (*pu["color"], glow_alpha)
            pygame.draw.ellipse(glow_surf, glow_color, (0, 0, pu["rect"].w + 20, pu["rect"].h + 20))
            screen.blit(glow_surf, (pu["rect"].x - 10, pu["rect"].y - 10))
            # Draw pickup
            pygame.draw.rect(screen, pu["color"], pu["rect"])
            # Draw timer bar
            timer_ratio = pu.get("timer", 15.0) / 15.0
            timer_bar_y = pu["rect"].bottom + 2
            timer_bar_w = pu["rect"].w
            timer_bar_h = 3
            pygame.draw.rect(screen, (60, 60, 60), (pu["rect"].x, timer_bar_y, timer_bar_w, timer_bar_h))
            pygame.draw.rect(screen, (255, 200, 0), (pu["rect"].x, timer_bar_y, int(timer_bar_w * timer_ratio), timer_bar_h))
        
        # Draw collection effects
        for effect in collection_effects:
            alpha = int(255 * (effect["life"] / 0.4))
            effect_surf = pygame.Surface((effect["size"] * 2, effect["size"] * 2), pygame.SRCALPHA)
            color_with_alpha = (*effect["color"], alpha)
            pygame.draw.circle(effect_surf, color_with_alpha, (effect["size"], effect["size"]), effect["size"])
            screen.blit(effect_surf, (effect["x"] - effect["size"], effect["y"] - effect["size"]))

        # Draw friendly AI
        for f in friendly_ai:
            pygame.draw.rect(screen, f["color"], f["rect"])
            # Draw health bar above friendly AI (green when full)
            bar_x = f["rect"].x
            bar_y = f["rect"].y - 8
            bar_w = f["rect"].w
            bar_h = 4
            # Use bright green for friendly AI health bars
            hp_ratio = f["hp"] / f["max_hp"] if f["max_hp"] > 0 else 0
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))  # Background
            fill_w = int(bar_w * hp_ratio)
            # Bright green for full health, slightly darker when damaged
            green_intensity = int(60 + (200 - 60) * hp_ratio)
            pygame.draw.rect(screen, (60, green_intensity, 60), (bar_x, bar_y, fill_w, bar_h))
            pygame.draw.rect(screen, (20, 20, 20), (bar_x, bar_y, bar_w, bar_h), 2)  # Border
        
        # Draw friendly projectiles
        for fp in friendly_projectiles:
            draw_projectile(fp["rect"], fp["color"], fp["shape"])

        for e in enemies:
            pygame.draw.rect(screen, e["color"], e["rect"])
            if ui_show_health_bars:
                draw_health_bar(e["rect"].x, e["rect"].y - 10, e["rect"].w, 6, e["hp"], e["max_hp"])

            # Draw shield for shielded enemies
            if e.get("has_shield"):
                shield_angle = e.get("shield_angle", 0.0)
                shield_length = e.get("shield_length", 50)
                enemy_center = pygame.Vector2(e["rect"].center)
                shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                shield_start = enemy_center + shield_dir * (e["rect"].w // 2)
                shield_end = enemy_center + shield_dir * (e["rect"].w // 2 + shield_length)
                # Draw shield line
                pygame.draw.line(screen, (100, 200, 255), shield_start, shield_end, 4)
                # Draw shield indicator
                pygame.draw.circle(screen, (150, 220, 255), (int(shield_start.x), int(shield_start.y)), 5)
            
            # Draw reflective shield for reflector enemies
            if e.get("has_reflective_shield"):
                shield_angle = e.get("shield_angle", 0.0)
                shield_length = e.get("shield_length", 60)
                enemy_center = pygame.Vector2(e["rect"].center)
                shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                shield_start = enemy_center + shield_dir * (e["rect"].w // 2)
                shield_end = enemy_center + shield_dir * (e["rect"].w // 2 + shield_length)
                # Draw reflective shield (glowing)
                shield_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.line(shield_surf, (255, 200, 100, 200), shield_start, shield_end, 6)
                pygame.draw.line(shield_surf, (255, 255, 150, 150), shield_start, shield_end, 3)
                screen.blit(shield_surf, (0, 0))
                # Draw shield indicator
                pygame.draw.circle(screen, (255, 220, 100), (int(shield_start.x), int(shield_start.y)), 6)
                # Show absorbed damage
                if e.get("shield_hp", 0) > 0:
                    shield_hp_text = font.render(f"{int(e['shield_hp'])}", True, (255, 255, 100))
                    screen.blit(shield_hp_text, (e["rect"].x, e["rect"].y - 25))

        # Draw bouncing destructor shapes
        for ds in destructor_shapes:
            # Draw with pulsing effect
            pulse = 0.5 + 0.5 * math.sin(run_time * 3.0)
            color = tuple(min(255, int(c * (0.8 + pulse * 0.2))) for c in ds.get("color", (200, 100, 100)))
            pygame.draw.rect(screen, color, ds["rect"])
            # Draw warning border
            pygame.draw.rect(screen, (255, 0, 0), ds["rect"], 3)
        
        # Draw player - red when shield is active, normal color otherwise
        player_color = (255, 50, 50) if shield_active else (200, 60, 60)
        pygame.draw.rect(screen, player_color, player)
        
        # Draw health bar above player character
        if ui_show_player_health_bar:
            health_bar_width = max(player.w, 40)
            health_bar_height = 6
            health_bar_x = player.centerx - health_bar_width // 2
            health_bar_y = player.y - 12
            draw_health_bar(health_bar_x, health_bar_y, health_bar_width, health_bar_height, player_hp, player_max_hp)
        
        # Draw shield visual effect when active
        if shield_active:
            shield_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            # Pulsing effect based on remaining duration
            pulse = 0.5 + 0.5 * math.sin(run_time * 10.0)
            alpha = int(150 + 100 * pulse)
            # Draw shield circle around player
            radius = max(player.w, player.h) + 10
            pygame.draw.circle(shield_surf, (150, 220, 255, alpha), player.center, radius, 3)
            # Inner glow
            pygame.draw.circle(shield_surf, (200, 240, 255, alpha // 2), player.center, radius - 2, 1)
            screen.blit(shield_surf, (0, 0))

        if last_move_velocity.length_squared() > 0:
            path_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            future_times = [0.2, 0.4, 0.6, 0.8, 1.0]
            for idx, t_pred in enumerate(future_times):
                future_pos = pygame.Vector2(player.center) + last_move_velocity * t_pred
                alpha = max(40, 170 - idx * 25)
                pygame.draw.circle(
                    path_overlay,
                    (120, 255, 120, alpha),
                    (int(future_pos.x), int(future_pos.y)),
                    6,
                )
            screen.blit(path_overlay, (0, 0))

        # Draw laser beams
        for laser in laser_beams:
            pygame.draw.line(screen, laser["color"], laser["start"], laser["end"], laser["width"])
            # Draw glow effect
            glow_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(glow_surf, (*laser["color"], 100), laser["start"], laser["end"], laser["width"] + 4)
            screen.blit(glow_surf, (0, 0))

        for b in player_bullets:
            draw_projectile(b["rect"], b.get("color", player_bullets_color), b.get("shape", "square"))
            # Draw explosion radius indicator if bullet has explosion
            if b.get("explosion_radius", 0.0) > 0.0:
                exp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                radius = int(b["explosion_radius"])
                pygame.draw.circle(exp_surf, (255, 200, 0, 30), b["rect"].center, radius, 2)
                screen.blit(exp_surf, (0, 0))
        for p in enemy_projectiles:
            draw_projectile(p["rect"], p.get("color", enemy_projectiles_color), p.get("shape", "circle"))

        # HUD (only if UI is enabled)
        if ui_show_all_ui:
            # Draw health bar at the bottom of the screen
            hp_bar_width = 400
            hp_bar_height = 30
            hp_bar_x = (WIDTH - hp_bar_width) // 2  # Center horizontally
            hp_bar_y = HEIGHT - hp_bar_height - 20  # 20 pixels from bottom
            
            # Draw overshield bar (above HP bar at bottom)
            if overshield > 0:
                overshield_bar_w = hp_bar_width
                overshield_bar_h = 12
                overshield_bar_x = hp_bar_x
                overshield_bar_y = hp_bar_y - 18  # Above HP bar
                overshield_ratio = overshield / overshield_max
                # Background
                pygame.draw.rect(screen, (40, 40, 40), (overshield_bar_x, overshield_bar_y, overshield_bar_w, overshield_bar_h))
                # Overshield (cyan/blue color)
                pygame.draw.rect(screen, (100, 200, 255), (overshield_bar_x, overshield_bar_y, int(overshield_bar_w * overshield_ratio), overshield_bar_h))
                # Border
                pygame.draw.rect(screen, (150, 220, 255), (overshield_bar_x, overshield_bar_y, overshield_bar_w, overshield_bar_h), 2)
                # Text
                shield_text = font.render(f"Shield: {int(overshield)}/{int(overshield_max)}", True, (150, 220, 255))
                shield_text_x = overshield_bar_x + (overshield_bar_w - shield_text.get_width()) // 2
                screen.blit(shield_text, (shield_text_x, overshield_bar_y - 1))
            
            # Draw HP bar at bottom
            draw_health_bar(hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height, player_hp, player_max_hp)
            # HP text centered above the bar
            hp_text = font.render(f"HP: {player_hp}/{player_max_hp}", True, (230, 230, 230))
            hp_text_x = hp_bar_x + (hp_bar_width - hp_text.get_width()) // 2
            screen.blit(hp_text, (hp_text_x, hp_bar_y - 24))
            
            # Other HUD elements remain at top-left
            lives_y = 10
            # Render HUD using helper function
            y = render_hud_text(f"Lives: {lives}", lives_y)
            y = render_hud_text(f"Level: {current_level} - {level_themes[current_level]['name']}", y, (255, 200, 100))
            y = render_hud_text(f"Wave: {wave_number} (Wave {wave_in_level}/3)", y)
            if wave_active:
                wave_text = f"Enemies: {len(enemies)}"
            else:
                wave_text = f"Next wave in: {time_to_next_wave:.1f}s"
            y = render_hud_text(wave_text, y)
            y = render_hud_text(f"Damage dealt: {damage_dealt}", y)
            y = render_hud_text(f"Damage taken: {damage_taken}", y)
            y = render_hud_text(f"Score: {score:,}", y, (255, 255, 100))
            y = render_hud_text(f"Time: {int(survival_time//60)}m {int(survival_time%60)}s", y, (200, 200, 255))
            if state == STATE_ENDURANCE:
                y = render_hud_text("ENDURANCE MODE", y, (255, 100, 100))
            y = render_hud_text(f"Boost: {int(boost_meter)}/{int(boost_meter_max)}", y)
            # Shield status
            if shield_active:
                y = render_hud_text("SHIELD ACTIVU", y, (150, 220, 255))
            elif shield_cooldown_remaining > 0.0:
                y = render_hud_text(f"Shield CD: {shield_cooldown_remaining:.1f}s", y, (200, 150, 150))
            else:
                y = render_hud_text("Shield: Ready (Left Alt)", y, (100, 255, 100))
            if fire_rate_buff_t > 0:
                y = render_hud_text(f"Firerate buff: {fire_rate_buff_t:.1f}s", y, (255, 220, 120))
            if enemy_spawn_boost_level > 0:
                y = render_hud_text(f"Enemy spawn boost: +{enemy_spawn_boost_level}", y, (255, 140, 220))
            
            # Display permanent stat upgrades
            y_offset = y
            if player_stat_multipliers["speed"] > 1.0:
                y_offset = render_hud_text(f"Speed: +{int((player_stat_multipliers['speed']-1.0)*100)}%", y_offset, (150, 255, 150))
            if player_stat_multipliers["firerate"] > 1.0:
                y_offset = render_hud_text(f"Fire Rate: +{int((player_stat_multipliers['firerate']-1.0)*100)}%", y_offset, (150, 255, 150))
            if player_stat_multipliers["bullet_damage"] > 1.0:
                y_offset = render_hud_text(f"Damage: +{int((player_stat_multipliers['bullet_damage']-1.0)*100)}%", y_offset, (150, 255, 150))
            if player_stat_multipliers["bullet_penetration"] > 0:
                y_offset = render_hud_text(f"Penetration: {int(player_stat_multipliers['bullet_penetration'])}", y_offset, (150, 255, 150))
            if player_stat_multipliers["bullet_explosion_radius"] > 0:
                y_offset = render_hud_text(f"Explosion: {int(player_stat_multipliers['bullet_explosion_radius'])}px", y_offset, (150, 255, 150))
            # Display current weapon mode
            weapon_names = {
                "basic": "BASIC FIRE",
                "rocket": "ROCKET LAUNCHER",
                "triple": "TRIPLE SHOT",
                "bouncing": "BOUNCING BULLETS",
                "giant": "GIANT BULLETS (10x)",
                "laser": "LASER BEAM"
            }
            weapon_colors = {
                "basic": (200, 200, 200),
                "rocket": (255, 100, 0),
                "triple": (100, 200, 255),
                "bouncing": (100, 255, 100),
                "giant": (255, 200, 0),
                "laser": (255, 50, 50)
            }
            screen.blit(font.render(f"Weapon: {weapon_names.get(current_weapon_mode, 'UNKNOWN')}", True, weapon_colors.get(current_weapon_mode, (255, 255, 255))), (10, y_offset))
            y_offset += 22
            # Show unlocked weapons
            unlocked_list = sorted(unlocked_weapons)
            unlocked_str = "Unlocked: " + ", ".join([weapon_names.get(w, w) for w in unlocked_list])
            screen.blit(font.render(unlocked_str, True, (150, 255, 150)), (10, y_offset))
            y_offset += 22
            screen.blit(font.render("Press 1-6 to switch weapons (if unlocked)", True, (150, 150, 150)), (10, y_offset))
            y_offset += 22
            
            # Only show metrics if enabled
            if ui_show_metrics:
                screen.blit(
                    font.render(
                        f"Run: {run_time:.1f}s  Shots: {shots_fired}  Hits: {hits}  Kills: {enemies_killed}  Deaths: {deaths}",
                        True,
                        (230, 230, 230),
                    ),
                    (10, 168),
                )

        # Pause overlay
        if state == STATE_PAUSED:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            draw_centered_text("Paused", HEIGHT // 2 - 140, use_big=True)
            draw_centered_text("Press C for Controls", HEIGHT // 2 - 90, color=(190, 190, 190))

            for i, opt in enumerate(pause_options):
                prefix = "> " if i == pause_selected else "  "
                draw_centered_text(prefix + opt, HEIGHT // 2 - 40 + i * 40)

            draw_centered_text("Up/Down + Enter.  P or Esc to resume.", HEIGHT // 2 + 120, color=(190, 190, 190))

        # Controls overlay
        elif state == STATE_CONTROLS:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            draw_centered_text("Controls", HEIGHT // 2 - 200, use_big=True)
            draw_centered_text("Up/Down select  Enter rebind  Esc back", HEIGHT // 2 - 150, color=(190, 190, 190))

            for i, action in enumerate(controls_actions):
                key_name = pygame.key.name(controls.get(action, pygame.K_UNKNOWN))
                prefix = "> " if i == controls_selected else "  "
                label = f"{action}: {key_name}"
                draw_centered_text(prefix + label, HEIGHT // 2 - 60 + i * 32)

            if controls_rebinding:
                draw_centered_text("Press a key...", HEIGHT // 2 + 160, color=(255, 230, 120))

        # Continue overlay
        elif state == STATE_CONTINUE:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            draw_centered_text("You Died", HEIGHT // 2 - 150, use_big=True)
            draw_centered_text(f"Lives left: {lives}", HEIGHT // 2 - 90)

            continue_blink_t += dt_real
            show = (int(continue_blink_t * 2) % 2) == 0
            if show:
                draw_centered_text("Press Enter or Space to continue", HEIGHT // 2 + 10)
            draw_centered_text("Press Esc to quit", HEIGHT // 2 + 60, color=(190, 190, 190))

        pygame.display.flip()

except KeyboardInterrupt:
    print("Interrupted by user (Ctrl+C). Saving run...")

except Exception as e:
    print("Unhandled exception:", repr(e))
    raise

finally:
    run_ended_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    telemetry.end_run(
        ended_at_iso=run_ended_at,
        seconds_survived=run_time,
        player_hp_end=player_hp,
        shots_fired=shots_fired,
        hits=hits,
        damage_taken=damage_taken,
        damage_dealt=damage_dealt,
        enemies_spawned=enemies_spawned,
        enemies_killed=enemies_killed,
        deaths=deaths,
        max_wave=wave_number,
    )
    telemetry.close()
    pygame.quit()

    print(f"Saved run_id={run_id} to game_telemetry.db")
