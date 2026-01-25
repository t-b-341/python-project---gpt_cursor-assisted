"""Game state container for all mutable game state."""
from dataclasses import dataclass, field
from typing import Any, Optional
import pygame


@dataclass
class GameState:
    """Container for all mutable game state.
    
    This centralizes all game state that changes during gameplay,
    replacing module-level globals for better organization and testability.
    """
    # Core game entity lists
    enemies: list = field(default_factory=list)
    player_bullets: list = field(default_factory=list)
    enemy_projectiles: list = field(default_factory=list)
    friendly_projectiles: list = field(default_factory=list)
    friendly_ai: list = field(default_factory=list)
    pickups: list = field(default_factory=list)
    grenade_explosions: list = field(default_factory=list)
    missiles: list = field(default_factory=list)
    laser_beams: list = field(default_factory=list)
    wave_beams: list = field(default_factory=list)
    damage_numbers: list = field(default_factory=list)
    weapon_pickup_messages: list = field(default_factory=list)
    pickup_particles: list = field(default_factory=list)
    collection_effects: list = field(default_factory=list)
    enemy_defeat_messages: list = field(default_factory=list)
    
    # Player state
    player_hp: int = 7500
    player_max_hp: int = 7500
    player_speed: int = 450
    player_bullet_damage: int = 20
    player_shoot_cooldown: float = 0.12
    player_time_since_shot: float = 999.0
    player_bullet_shape_index: int = 0
    overshield: int = 0
    overshield_recharge_timer: float = 0.0
    shield_active: bool = False
    shield_duration_remaining: float = 0.0
    shield_cooldown: float = 10.0
    shield_cooldown_remaining: float = 0.0
    shield_recharge_timer: float = 0.0
    shield_recharge_cooldown: float = 10.0
    lives: int = 10
    player_health_regen_rate: float = 0.0
    player_current_zones: set = field(default_factory=set)
    
    # Player movement and abilities
    last_horizontal_key: Optional[int] = None
    last_vertical_key: Optional[int] = None
    last_move_velocity: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0))
    # Per-frame movement input (set by game loop before movement_system.update)
    move_input_x: int = 0
    move_input_y: int = 0
    speed_mult: float = 1.0
    jump_cooldown_timer: float = 0.0
    jump_velocity: pygame.Vector2 = field(default_factory=lambda: pygame.Vector2(0, 0))
    jump_timer: float = 0.0
    is_jumping: bool = False
    previous_boost_state: bool = False
    previous_slow_state: bool = False
    boost_meter: float = 100.0
    
    # Weapon and combat state
    current_weapon_mode: str = "basic"
    previous_weapon_mode: str = "basic"
    unlocked_weapons: set = field(default_factory=lambda: {"basic"})
    laser_time_since_shot: float = 999.0
    wave_beam_time_since_shot: float = 999.0
    wave_beam_pattern_index: int = 0
    grenade_time_since_used: float = 999.0
    missile_time_since_used: float = 999.0
    ally_drop_timer: float = 0.0
    dropped_ally: Optional[dict] = None
    
    # Player stat multipliers (from pickups)
    player_stat_multipliers: dict = field(default_factory=lambda: {
        "speed": 1.0,
        "firerate": 1.0,
        "bullet_size": 1.0,
        "bullet_speed": 1.0,
        "bullet_damage": 1.0,
        "bullet_knockback": 1.0,
        "bullet_penetration": 0,
        "bullet_explosion_radius": 0.0,
    })
    random_damage_multiplier: float = 1.0
    fire_rate_buff_t: float = 0.0
    
    # Game progression and scoring
    score: int = 0
    wave_number: int = 1
    wave_in_level: int = 1
    current_level: int = 1
    max_level: int = 3
    wave_active: bool = True
    time_to_next_wave: float = 0.0
    boss_active: bool = False
    pickup_spawn_timer: float = 0.0
    
    # Run statistics
    run_time: float = 0.0
    survival_time: float = 0.0
    shots_fired: int = 0
    hits: int = 0
    damage_taken: int = 0
    damage_dealt: int = 0
    enemies_spawned: int = 0
    enemies_killed: int = 0
    deaths: int = 0
    pos_timer: float = 0.0
    
    # Side quests
    side_quests: dict = field(default_factory=lambda: {
        "no_hit_wave": {
            "name": "Perfect Wave",
            "description": "Complete wave without getting hit",
            "bonus_points": 10000,
            "active": False,
            "completed": False,
        }
    })
    wave_damage_taken: int = 0
    
    # High score system
    player_name_input: str = ""
    name_input_active: bool = False
    final_score_for_high_score: int = 0

    # Player rect (position/size on screen; created in main() after display init)
    player_rect: Optional[pygame.Rect] = None

    # Screen/flow state (which UI state we're in: MENU, PLAYING, PAUSED, etc.)
    current_screen: str = "MENU"
    previous_screen: Optional[str] = None

    # Menu and pause UI state
    menu_section: int = 0
    pause_selected: int = 0
    continue_blink_t: float = 0.0
    controls_selected: int = 0
    controls_rebinding: bool = False

    # Telemetry run tracking
    run_id: Any = None
    run_started_at: str = ""

    # Level context for systems (set by main/game loop): move_player, move_enemy, clamp, blocks, width, height, rect_offscreen, vec_toward, update_friendly_ai
    level_context: Any = None