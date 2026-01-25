import math
import warnings

# Suppress pygame's pkg_resources deprecation warning
# This is a pygame internal issue, not our code
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")
import random
import json
import os

import pygame
import sqlite3
from datetime import datetime, timezone

# Try to import C extension for performance, fallback to Python if not available
# Note: game_physics module is built from game_physics.c - see BUILD_INSTRUCTIONS.md
try:
    import game_physics  # type: ignore
    USE_C_EXTENSION = True
except ImportError:
    USE_C_EXTENSION = False
    print("Note: C extension not available, using Python fallback (slower)")

# GPU acceleration (optional - falls back to CPU if unavailable)
try:
    from gpu_physics import update_bullets_batch, check_collisions_batch, CUDA_AVAILABLE
    USE_GPU = CUDA_AVAILABLE
    if USE_GPU:
        print("GPU acceleration enabled (CUDA)")
    else:
        print("GPU acceleration available but CUDA not detected (using CPU fallback)")
except ImportError:
    USE_GPU = False
    print("Note: GPU acceleration not available. Install with: pip install numba")

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

# Import constants
from constants import *

# Import config data
from config_enemies import (
    ENEMY_TEMPLATES,
    BOSS_TEMPLATE,
    BASE_ENEMIES_PER_WAVE,
    MAX_ENEMIES_PER_WAVE,
    ENEMY_SPAWN_MULTIPLIER,
    ENEMY_HP_SCALE_MULTIPLIER,
    ENEMY_SPEED_SCALE_MULTIPLIER,
    ENEMY_FIRE_RATE_MULTIPLIER,
    ENEMY_HP_CAP,
    QUEEN_FIXED_HP,
    QUEEN_SPEED_MULTIPLIER,
    FRIENDLY_AI_TEMPLATES,
)
from config_weapons import (
    WEAPON_CONFIGS,
    WEAPON_NAMES,
    WEAPON_DISPLAY_COLORS,
    WEAPON_UNLOCK_ORDER,
)
from rendering import (
    draw_silver_wall_texture,
    draw_cracked_brick_wall_texture,
    draw_projectile,
    draw_health_bar,
    draw_centered_text,
    render_hud_text,
)
from enemies import (
    move_enemy_with_push_cached,
    find_nearest_threat,
    make_enemy_from_template,
    log_enemy_spawns,
    find_threats_in_dodge_range,
)
from allies import (
    find_nearest_enemy,
    make_friendly_from_template,
    spawn_friendly_ai,
    spawn_friendly_projectile,
    update_friendly_ai,
)
from state import GameState


# Placeholder WIDTH/HEIGHT for module-level initialization
# Will be updated in main() after pygame.display.init()
WIDTH = 1920  # Default placeholder
HEIGHT = 1080  # Default placeholder

# ----------------------------
# Rendering cache for performance optimization
# ----------------------------
# Note: Wall texture, HUD text, and health bar caches are now in rendering.py
# Cache for pre-rendered static block surfaces
_cached_trapezoid_surfaces = {}
_cached_triangle_surfaces = {}


def main():
    """Main entry point for the game. All mutable game state lives in the GameState instance."""
    global screen, clock, font, big_font, small_font, WIDTH, HEIGHT
    global telemetry, telemetry_enabled
    global difficulty, aiming_mode, use_character_profile, player_class, custom_profile_stats, custom_profile_stats_keys
    global testing_mode, invulnerability_mode, beam_selection_pattern
    global difficulty_selected, aiming_mode_selected, use_character_profile_selected, character_profile_selected
    global custom_profile_stat_selected, player_class_selected, ui_show_metrics_selected, beam_selection_selected
    global endurance_mode_selected, ui_telemetry_enabled_selected
    global ui_show_metrics, ui_show_hud, ui_show_health_bars, ui_show_player_health_bar
    global weapon_selection_options
    global trapezoid_blocks, triangle_blocks, destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks
    global hazard_obstacles, moving_health_zone
    global _cached_trapezoid_surfaces, _cached_triangle_surfaces
    global boost_meter_max, boost_drain_per_s, boost_regen_per_s, boost_speed_mult
    global friendly_ai_templates, overshield_max, grenade_cooldown, missile_cooldown, ally_drop_cooldown
    global run_started_at

    pygame.init()

    # Welcome message when game launches
    print("welcome to my game! :D")

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
    small_font = pygame.font.SysFont(None, 20)

    # Create GameState as the single source of truth for all mutable game state.
    # Use GameState() defaults; only set values that depend on display/context.
    game_state = GameState()
    game_state.player_rect = pygame.Rect((WIDTH - 28) // 2, (HEIGHT - 28) // 2, 28, 28)
    game_state.current_screen = STATE_MENU
    game_state.run_started_at = run_started_at

    # Local alias for readability where the loop uses "player" frequently.
    # Must stay in sync: player is game_state.player_rect.
    player = game_state.player_rect

    # Initialize pygame mouse visibility
    pygame.mouse.set_visible(True)
    
    # Load controls from file (now that pygame is initialized)
    # This must happen after pygame.init() to avoid warnings
    global controls
    if not controls:  # Only load if not already loaded
        controls = load_controls()
    
    # Filter blocks to prevent overlaps (moved from module level)
    global destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks
    destructible_blocks = filter_blocks_no_overlap(destructible_blocks, [moveable_destructible_blocks, giant_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], game_state.player_rect)
    moveable_destructible_blocks = filter_blocks_no_overlap(moveable_destructible_blocks, [destructible_blocks, giant_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], game_state.player_rect)
    giant_blocks = filter_blocks_no_overlap(giant_blocks, [destructible_blocks, moveable_destructible_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], game_state.player_rect)
    super_giant_blocks = filter_blocks_no_overlap(super_giant_blocks, [destructible_blocks, moveable_destructible_blocks, giant_blocks, trapezoid_blocks, triangle_blocks], game_state.player_rect)

    # ----------------------------
    # Start run + log initial spawns
    # ----------------------------
    game_state.run_id = None  # Will be set when game starts
    # Don't start wave automatically - wait for menu selection

    # ----------------------------
    # Main loop with safe shutdown
    # ----------------------------
    # Note: telemetry_enabled and telemetry are module-level variables,
    # so we can modify them directly without global declaration in the main loop
    # Initialize high scores database
    init_high_scores_db()

    # Main loop with safe shutdown
    running = True
    FPS = 60
    
    try:
        while running:
            dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
            game_state.run_time += dt
            game_state.survival_time += dt

            # Sync flow state from GameState for use in this iteration (single source of truth is game_state)
            state = game_state.current_screen
            previous_game_state = game_state.previous_screen
            menu_section = game_state.menu_section
            pause_selected = game_state.pause_selected
            continue_blink_t = game_state.continue_blink_t
            controls_selected = game_state.controls_selected
            controls_rebinding = game_state.controls_rebinding

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle text input for name input screen
                if state == STATE_NAME_INPUT and event.type == pygame.TEXTINPUT:
                    if len(game_state.player_name_input) < 20:  # Limit name length
                        game_state.player_name_input += event.text
                
                # Handle keyboard events
                if event.type == pygame.KEYDOWN:
                    # Handle name input
                    if state == STATE_NAME_INPUT:
                        if event.key == pygame.K_BACKSPACE:
                            game_state.player_name_input = game_state.player_name_input[:-1]
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            if game_state.player_name_input.strip():
                                save_high_score(
                                    game_state.player_name_input.strip(),
                                    game_state.final_score_for_high_score,
                                    game_state.wave_number - 1,
                                    game_state.survival_time,
                                    game_state.enemies_killed,
                                    difficulty
                                )
                            state = STATE_HIGH_SCORES
                            game_state.name_input_active = False
                    
                    # ESC key handling
                    if event.key == pygame.K_ESCAPE:
                        if state == STATE_PLAYING or state == STATE_ENDURANCE:
                            previous_game_state = state
                            state = STATE_PAUSED
                            pause_selected = 0
                        elif state == STATE_PAUSED:
                            state = previous_game_state if previous_game_state else STATE_PLAYING
                        elif state == STATE_CONTINUE:
                            running = False
                        elif state == STATE_CONTROLS:
                            state = STATE_PAUSED
                        elif state == STATE_MENU:
                            running = False
                        elif state == STATE_VICTORY or state == STATE_GAME_OVER or state == STATE_HIGH_SCORES:
                            running = False
                        elif state == STATE_NAME_INPUT:
                            if game_state.player_name_input.strip():
                                save_high_score(
                                    game_state.player_name_input.strip(),
                                    game_state.final_score_for_high_score,
                                    game_state.wave_number - 1,
                                    game_state.survival_time,
                                    game_state.enemies_killed,
                                    difficulty
                                )
                            state = STATE_HIGH_SCORES
                            game_state.name_input_active = False
                    
                    # P key for pause
                    if event.key == pygame.K_p:
                        if state == STATE_PLAYING or state == STATE_ENDURANCE:
                            previous_game_state = state
                            state = STATE_PAUSED
                            pause_selected = 0
                        elif state == STATE_PAUSED:
                            state = previous_game_state if previous_game_state else STATE_PLAYING
                    
                    # Pause menu navigation
                    if state == STATE_PAUSED:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            pause_selected = (pause_selected - 1) % len(pause_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            pause_selected = (pause_selected + 1) % len(pause_options)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            choice = pause_options[pause_selected]
                            if choice == "Continue":
                                state = previous_game_state if previous_game_state else STATE_PLAYING
                            elif choice == "Restart Game":
                                # Restart game: reset to menu
                                state = STATE_MENU
                                menu_section = 0
                                # Reset game state
                                game_state.enemies.clear()
                                game_state.player_bullets.clear()
                                game_state.enemy_projectiles.clear()
                                game_state.friendly_projectiles.clear()
                                game_state.friendly_ai.clear()
                                game_state.grenade_explosions.clear()
                                game_state.missiles.clear()
                                game_state.wave_number = 1
                                game_state.wave_in_level = 1
                                game_state.current_level = 1
                                game_state.player_hp = game_state.player_max_hp
                                game_state.lives = 3
                                game_state.score = 0
                                game_state.run_time = 0.0
                                game_state.survival_time = 0.0
                                game_state.wave_active = False
                                game_state.time_to_next_wave = 0.0
                                game_state.unlocked_weapons = {"basic"}
                                game_state.current_weapon_mode = "basic"
                            elif choice == "Quit":
                                running = False
                    
                    # Menu navigation
                    if state == STATE_MENU:
                        if menu_section == 0:  # Difficulty selection
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                difficulty_selected = (difficulty_selected - 1) % len(difficulty_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                difficulty_selected = (difficulty_selected + 1) % len(difficulty_options)
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                difficulty = difficulty_options[difficulty_selected]
                                menu_section = 1  # Go to aiming mode
                        elif menu_section == 1:  # Aiming mode
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                aiming_mode_selected = (aiming_mode_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                aiming_mode_selected = (aiming_mode_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 0  # Go back
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                aiming_mode = AIM_MOUSE if aiming_mode_selected == 0 else AIM_ARROWS
                                menu_section = 1.5  # Go to character profile yes/no
                        elif menu_section == 1.5:  # Character profile yes/no
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                use_character_profile_selected = (use_character_profile_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                use_character_profile_selected = (use_character_profile_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 1  # Go back
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                use_character_profile = use_character_profile_selected == 1
                                if use_character_profile:
                                    menu_section = 2  # Go to profile selection
                                else:
                                    menu_section = 3  # Skip to options
                        elif menu_section == 2:  # Character profile selection
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                character_profile_selected = (character_profile_selected - 1) % len(character_profile_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                character_profile_selected = (character_profile_selected + 1) % len(character_profile_options)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 1.5  # Go back
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                if character_profile_selected == 0:
                                    menu_section = 7  # Go to class selection
                                elif character_profile_selected == 1:
                                    menu_section = 6  # Go to custom profile creator
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                if character_profile_selected == 0:
                                    menu_section = 7  # Go to class selection
                                elif character_profile_selected == 1:
                                    menu_section = 6  # Go to custom profile creator
                        elif menu_section == 6:  # Custom profile creator
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                custom_profile_stat_selected = (custom_profile_stat_selected - 1) % len(custom_profile_stats_list)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                custom_profile_stat_selected = (custom_profile_stat_selected + 1) % len(custom_profile_stats_list)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                                custom_profile_stats[stat_key] = max(0.5, custom_profile_stats[stat_key] - 0.1)
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                                menu_section = 3  # Continue to options
                            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                                stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                                custom_profile_stats[stat_key] = min(3.0, custom_profile_stats[stat_key] + 0.1)
                            elif event.key == pygame.K_MINUS:
                                stat_key = custom_profile_stats_keys[custom_profile_stat_selected]
                                custom_profile_stats[stat_key] = max(0.5, custom_profile_stats[stat_key] - 0.1)
                        elif menu_section == 7:  # Class selection
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                player_class_selected = (player_class_selected - 1) % len(player_class_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                player_class_selected = (player_class_selected + 1) % len(player_class_options)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 2  # Go back
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                player_class = player_class_options[player_class_selected]
                                menu_section = 3  # Go to options
                        elif menu_section == 3:  # HUD options
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                ui_show_metrics_selected = (ui_show_metrics_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                ui_show_metrics_selected = (ui_show_metrics_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                if use_character_profile:
                                    menu_section = 7 if character_profile_selected == 0 else 6
                                else:
                                    menu_section = 1.5
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                ui_show_metrics = ui_show_metrics_selected == 0
                                ui_show_hud = ui_show_metrics
                                menu_section = 3.5  # Go to telemetry options
                        elif menu_section == 3.5:  # Telemetry options
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                ui_telemetry_enabled_selected = (ui_telemetry_enabled_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                ui_telemetry_enabled_selected = (ui_telemetry_enabled_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 3  # Go back to HUD options
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                telemetry_enabled = ui_telemetry_enabled_selected == 0
                                if testing_mode:
                                    menu_section = 4  # Go to weapon selection
                                else:
                                    menu_section = 5  # Go to start
                        elif menu_section == 4:  # Weapon selection (testing mode)
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                beam_selection_selected = (beam_selection_selected - 1) % len(weapon_selection_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                beam_selection_selected = (beam_selection_selected + 1) % len(weapon_selection_options)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 3  # Go back
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                selected_weapon = weapon_selection_options[beam_selection_selected]
                                game_state.unlocked_weapons.add(selected_weapon)
                                if game_state.current_weapon_mode == "wave_beam" and selected_weapon != "wave_beam":
                                    game_state.wave_beams.clear()
                                if game_state.current_weapon_mode == "laser" and selected_weapon != "laser":
                                    game_state.laser_beams.clear()
                                game_state.current_weapon_mode = selected_weapon
                                if selected_weapon == "wave_beam":
                                    game_state.wave_beam_pattern_index = 0
                                    beam_selection_pattern = "sine"
                                else:
                                    beam_selection_pattern = selected_weapon
                                if testing_mode:
                                    menu_section = 4.5  # Go to testing options
                                else:
                                    menu_section = 5  # Go to start
                        elif menu_section == 4.5:  # Testing options (testing mode only)
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                invulnerability_mode = not invulnerability_mode
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                invulnerability_mode = not invulnerability_mode
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 4  # Go back to weapon selection
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                menu_section = 5  # Go to start
                        elif menu_section == 5:  # Start game
                            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                if testing_mode:
                                    menu_section = 4.5
                                else:
                                    menu_section = 3.5  # Go back to telemetry options
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                # Initialize game
                                if telemetry_enabled:
                                    telemetry = Telemetry(db_path="game_telemetry.db", flush_interval_s=0.5, max_buffer=700)
                                else:
                                    class NoOpTelemetry:
                                        def __getattr__(self, name):
                                            return lambda *args, **kwargs: None
                                    telemetry = NoOpTelemetry()
                                
                                # Apply class stats
                                stats = player_class_stats[player_class]
                                game_state.player_max_hp = int(1000 * stats["hp_mult"] * 0.75)  # Reduced by 0.75x
                                game_state.player_hp = game_state.player_max_hp
                                game_state.player_speed = int(300 * stats["speed_mult"])
                                game_state.player_bullet_damage = int(20 * stats["damage_mult"])
                                game_state.player_shoot_cooldown = 0.12 / stats["firerate_mult"]
                                
                                # Set state
                                if endurance_mode_selected == 1:
                                    state = STATE_ENDURANCE
                                    game_state.lives = 999
                                    previous_game_state = STATE_ENDURANCE
                                else:
                                    state = STATE_PLAYING
                                    previous_game_state = STATE_PLAYING
                                
                                game_state.run_id = telemetry.start_run(game_state.run_started_at, game_state.player_max_hp) if telemetry_enabled else None
                                start_wave(game_state.wave_number, game_state)
                    
                    # Controls rebinding
                    if state == STATE_CONTROLS and controls_rebinding:
                        if event.key != pygame.K_ESCAPE:
                            action = controls_actions[controls_selected]
                            controls[action] = event.key
                            save_controls(controls)
                            controls_rebinding = False
                        else:
                            controls_rebinding = False
                    
                    # Shield activation (Left Alt) - only activates when recharge bar is full
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_LALT:
                        # Shield can only be activated when recharge bar is full (shield_recharge_timer >= shield_recharge_cooldown)
                        if game_state.shield_recharge_timer >= game_state.shield_recharge_cooldown and not game_state.shield_active:
                            game_state.shield_active = True
                            game_state.shield_duration_remaining = shield_duration
                            game_state.shield_cooldown = 10.0  # Fixed 10 second cooldown
                            game_state.shield_recharge_cooldown = game_state.shield_cooldown
                            game_state.shield_recharge_timer = 0.0  # Reset recharge timer when shield activates
                            game_state.shield_cooldown_remaining = 0.0
                    
                    # Overshield activation (Tab)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_TAB:
                        if game_state.overshield_recharge_timer >= overshield_recharge_cooldown:
                            game_state.overshield = game_state.player_max_hp
                            overshield_max = max(overshield_max, game_state.player_max_hp)
                            game_state.overshield_recharge_timer = 0.0
                    
                    # Grenade (E key)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_e:
                        if game_state.grenade_time_since_used >= grenade_cooldown:
                            grenade_radius = player.w * 10  # 10x player size
                            game_state.grenade_explosions.append({
                                "x": player.centerx,
                                "y": player.centery,
                                "radius": 0,
                                "max_radius": grenade_radius,
                                "timer": 0.3,  # Explosion duration
                                "damage": grenade_damage,
                                "source": "player"  # Mark as player grenade for immunity
                            })
                            game_state.grenade_time_since_used = 0.0
                    
                    # Missile (R key)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_r:
                        if missile_time_since_used >= missile_cooldown:
                            # Find nearest enemy as target
                            target_enemy = None
                            min_dist = float("inf")
                            for enemy in game_state.enemies:
                                dist = (pygame.Vector2(enemy["rect"].center) - pygame.Vector2(player.center)).length_squared()
                                if dist < min_dist:
                                    min_dist = dist
                                    target_enemy = enemy
                            
                            if target_enemy:
                                # Spawn 3 missiles in a burst (spread pattern)
                                burst_offsets = [
                                    (-10, -10),  # Left missile
                                    (0, -15),    # Center missile (slightly ahead)
                                    (10, -10),   # Right missile
                                ]
                                for offset_x, offset_y in burst_offsets:
                                    missile_rect = pygame.Rect(
                                        player.centerx - 8 + offset_x,
                                        player.centery - 8 + offset_y,
                                        16, 16
                                    )
                                    game_state.missiles.append({
                                        "rect": missile_rect,
                                        "vel": pygame.Vector2(0, 0),
                                        "target_enemy": target_enemy,
                                        "speed": 500,
                                        "damage": missile_damage,
                                        "explosion_radius": 150
                                    })
                                game_state.missile_time_since_used = 0.0
                    
                    # Ally drop (Q key)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == controls.get("ally_drop", pygame.K_q):
                        if game_state.ally_drop_timer >= ally_drop_cooldown:
                            if game_state.dropped_ally and game_state.dropped_ally in game_state.friendly_ai:
                                game_state.friendly_ai.remove(game_state.dropped_ally)
                            
                            # Find tank template
                            tank_template = None
                            for tmpl in friendly_ai_templates:
                                if tmpl.get("type") == "tank":
                                    tank_template = tmpl
                                    break
                            
                            if tank_template:
                                player_center = pygame.Vector2(player.center)
                                if game_state.last_move_velocity.length_squared() > 0:
                                    spawn_dir = -game_state.last_move_velocity.normalize()
                                else:
                                    spawn_dir = pygame.Vector2(0, 1)
                                
                                spawn_pos = player_center + spawn_dir * 60  # Spawn 60 pixels behind player
                                friendly = make_friendly_from_template(tank_template, 1.0, 1.0)
                                friendly["rect"].center = (int(spawn_pos.x), int(spawn_pos.y))
                                game_state.friendly_ai.append(friendly)
                                game_state.dropped_ally = friendly
                            
                            game_state.ally_drop_timer = 0.0
                    
                    # Weapon switching (keys 1-6)
                    if state == STATE_PLAYING or state == STATE_ENDURANCE:
                        if event.key == pygame.K_1 and "basic" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            game_state.current_weapon_mode = "basic"
                        elif event.key == pygame.K_2 and "rocket" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "wave_beam":
                                game_state.wave_beams.clear()
                            if game_state.previous_weapon_mode == "laser":
                                game_state.laser_beams.clear()
                            game_state.current_weapon_mode = "rocket"
                        elif event.key == pygame.K_3 and "triple" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "wave_beam":
                                game_state.wave_beams.clear()
                            if game_state.previous_weapon_mode == "laser":
                                game_state.laser_beams.clear()
                            game_state.current_weapon_mode = "triple"
                        elif event.key == pygame.K_4 and "bouncing" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "wave_beam":
                                game_state.wave_beams.clear()
                            if game_state.previous_weapon_mode == "laser":
                                game_state.laser_beams.clear()
                            game_state.current_weapon_mode = "bouncing"
                        elif event.key == pygame.K_5 and "giant" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "wave_beam":
                                game_state.wave_beams.clear()
                            if game_state.previous_weapon_mode == "laser":
                                game_state.laser_beams.clear()
                            game_state.current_weapon_mode = "giant"
                        elif event.key == pygame.K_6 and "laser" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "wave_beam":
                                game_state.wave_beams.clear()
                            game_state.current_weapon_mode = "laser"
                        elif event.key == pygame.K_7 and "wave_beam" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "laser":
                                game_state.laser_beams.clear()
                            game_state.current_weapon_mode = "wave_beam"
                            game_state.wave_beam_pattern_index = 0
                            beam_selection_pattern = "sine"  # beam_selection_pattern is a menu state variable, not game state
            
            # Game state updates (only when playing)
            if state == STATE_PLAYING or state == STATE_ENDURANCE:
                # Update timers
                game_state.player_time_since_shot += dt
                game_state.laser_time_since_shot += dt
                game_state.wave_beam_time_since_shot += dt
                game_state.grenade_time_since_used += dt
                game_state.missile_time_since_used += dt
                game_state.jump_cooldown_timer += dt
                game_state.jump_timer += dt
                game_state.overshield_recharge_timer += dt
                # Only decrement shield duration when shield is active
                if game_state.shield_active:
                    game_state.shield_duration_remaining -= dt
                game_state.shield_cooldown_remaining -= dt
                game_state.shield_recharge_timer += dt
                game_state.ally_drop_timer += dt
                game_state.fire_rate_buff_t += dt
                game_state.pos_timer += dt
                continue_blink_t += dt
                
                # Update damage number timers
                for dmg_num in game_state.damage_numbers[:]:
                    dmg_num["timer"] -= dt
                    if dmg_num["timer"] <= 0:
                        game_state.damage_numbers.remove(dmg_num)
                
                # Update weapon pickup message timers
                for msg in game_state.weapon_pickup_messages[:]:
                    msg["timer"] -= dt
                    if msg["timer"] <= 0:
                        game_state.weapon_pickup_messages.remove(msg)
                
                # Update shield
                if game_state.shield_active:
                    if game_state.shield_duration_remaining <= 0.0:
                        game_state.shield_active = False
                        game_state.shield_cooldown_remaining = game_state.shield_cooldown
                        game_state.shield_recharge_timer = 0.0
                
                # Update jump/dash
                if game_state.is_jumping:
                    game_state.jump_timer += dt
                    if game_state.jump_timer >= jump_duration:
                        game_state.is_jumping = False
                        game_state.jump_velocity = pygame.Vector2(0, 0)
                
                # Update hazard obstacles
                update_hazard_obstacles(dt)
                
                # Check paraboloid/trapezoid hazards for enemy collision and damage
                for hazard in hazard_obstacles:
                    if hazard.get("points") and len(hazard["points"]) > 2:
                        hazard_damage = hazard.get("damage", 10)
                        for enemy in game_state.enemies[:]:
                            enemy_center = pygame.Vector2(enemy["rect"].center)
                            # Check if enemy is inside hazard shape
                            if check_point_in_hazard(enemy_center, hazard["points"], hazard["bounding_rect"]):
                                enemy["hp"] -= hazard_damage * dt  # Damage per second
                                if enemy["hp"] <= 0:
                                    kill_enemy(enemy, game_state)
                
                # Update enemy defeat message timers
                for msg in game_state.enemy_defeat_messages[:]:
                    msg["timer"] -= dt
                    if msg["timer"] <= 0:
                        game_state.enemy_defeat_messages.remove(msg)
                
                # Update pickup effects
                update_pickup_effects(dt, game_state)
                
                # Player movement and input handling
                keys = pygame.key.get_pressed()
                
                # Get movement input
                move_x = 0
                move_y = 0
                
                # Handle movement keys
                if keys[controls.get("move_left", pygame.K_a)]:
                    move_x = -1
                    game_state.last_horizontal_key = controls.get("move_left", pygame.K_a)
                elif keys[controls.get("move_right", pygame.K_d)]:
                    move_x = 1
                    game_state.last_horizontal_key = controls.get("move_right", pygame.K_d)
                
                if keys[controls.get("move_up", pygame.K_w)]:
                    move_y = -1
                    game_state.last_vertical_key = controls.get("move_up", pygame.K_w)
                elif keys[controls.get("move_down", pygame.K_s)]:
                    move_y = 1
                    game_state.last_vertical_key = controls.get("move_down", pygame.K_s)
                
                # Boost/slow mechanics
                is_boosting = keys[controls.get("boost", pygame.K_LSHIFT)] and game_state.boost_meter > 0
                is_slowing = keys[controls.get("slow", pygame.K_LCTRL)]
                
                if is_boosting:
                    game_state.boost_meter = max(0, game_state.boost_meter - boost_drain_per_s * dt)
                    speed_mult = boost_speed_mult
                    game_state.previous_boost_state = True
                else:
                    game_state.boost_meter = min(boost_meter_max, game_state.boost_meter + boost_regen_per_s * dt)
                    speed_mult = 1.0
                    game_state.previous_boost_state = False
                
                if is_slowing:
                    speed_mult *= slow_speed_mult
                    game_state.previous_slow_state = True
                else:
                    game_state.previous_slow_state = False
                
                # Apply fire rate buff
                effective_fire_rate = game_state.player_shoot_cooldown
                if game_state.fire_rate_buff_t < fire_rate_buff_duration:
                    effective_fire_rate *= fire_rate_mult
                
                # Calculate movement
                if move_x != 0 or move_y != 0:
                    move_dir = pygame.Vector2(move_x, move_y).normalize()
                    move_speed = game_state.player_speed * speed_mult * game_state.player_stat_multipliers["speed"]
                    
                    # Apply jump/dash velocity
                    if game_state.is_jumping:
                        move_speed += game_state.jump_velocity.length()
                    
                    move_amount = move_speed * dt
                    move_vec = move_dir * move_amount
                    
                    game_state.last_move_velocity = move_dir * move_speed
                    
                    # Move player with collision
                    move_player_with_push(player, int(move_vec.x), int(move_vec.y), blocks)
                    clamp_rect_to_screen(player)
                else:
                    game_state.last_move_velocity = pygame.Vector2(0, 0)
                
                # Update jump/dash
                if game_state.is_jumping:
                    player.x += int(game_state.jump_velocity.x * dt)
                    player.y += int(game_state.jump_velocity.y * dt)
                    clamp_rect_to_screen(player)
                
                # Player shooting
                mouse_buttons = pygame.mouse.get_pressed()
                shoot_input = mouse_buttons[0] or (aiming_mode == AIM_ARROWS and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]))
                
                if shoot_input and game_state.player_time_since_shot >= effective_fire_rate:
                    spawn_player_bullet_and_log(game_state)
                    game_state.player_time_since_shot = 0.0
                
                # Laser beam weapon
                if game_state.current_weapon_mode == "laser" and game_state.laser_time_since_shot >= laser_cooldown:
                    if aiming_mode == AIM_ARROWS:
                        keys = pygame.key.get_pressed()
                        dx = (1 if keys[pygame.K_RIGHT] else 0) - (1 if keys[pygame.K_LEFT] else 0)
                        dy = (1 if keys[pygame.K_DOWN] else 0) - (1 if keys[pygame.K_UP] else 0)
                        if dx == 0 and dy == 0:
                            if game_state.last_move_velocity.length_squared() > 0:
                                direction = game_state.last_move_velocity.normalize()
                            else:
                                direction = pygame.Vector2(1, 0)
                        else:
                            direction = pygame.Vector2(dx, dy).normalize()
                    else:
                        mx, my = pygame.mouse.get_pos()
                        direction = vec_toward(player.centerx, player.centery, mx, my)
                    
                    end_pos = pygame.Vector2(player.center) + direction * laser_length
                    game_state.laser_beams.append({
                        "start": pygame.Vector2(player.center),
                        "end": end_pos,
                        "color": (255, 50, 50),
                        "width": 5,
                        "damage": laser_damage,
                        "timer": 0.1
                    })
                    game_state.laser_time_since_shot = 0.0
                
                # Wave beam weapon
                if game_state.current_weapon_mode == "wave_beam" and game_state.wave_beam_time_since_shot >= wave_beam_cooldown:
                    if aiming_mode == AIM_ARROWS:
                        keys = pygame.key.get_pressed()
                        dx = (1 if keys[pygame.K_RIGHT] else 0) - (1 if keys[pygame.K_LEFT] else 0)
                        dy = (1 if keys[pygame.K_DOWN] else 0) - (1 if keys[pygame.K_UP] else 0)
                        if dx == 0 and dy == 0:
                            if game_state.last_move_velocity.length_squared() > 0:
                                direction = game_state.last_move_velocity.normalize()
                            else:
                                direction = pygame.Vector2(1, 0)
                        else:
                            direction = pygame.Vector2(dx, dy).normalize()
                    else:
                        mx, my = pygame.mouse.get_pos()
                        direction = vec_toward(player.centerx, player.centery, mx, my)
                    
                    pattern = wave_beam_patterns[game_state.wave_beam_pattern_index % len(wave_beam_patterns)]
                    points = generate_wave_beam_points(
                        pygame.Vector2(player.center),
                        direction,
                        pattern,
                        wave_beam_length,
                        amplitude=7.0,  # 7 pixels amplitude as specified
                        frequency=0.02,
                        time_offset=game_state.run_time
                    )
                    game_state.wave_beams.append({
                        "points": points,
                        "color": (50, 255, 50),  # Lime green
                        "width": wave_beam_width,
                        "damage": wave_beam_damage,
                        "timer": 999.0  # Constant beam (no flashing) - very long timer
                    })
                    game_state.wave_beam_time_since_shot = 0.0
                
                # Update laser beams
                for beam in game_state.laser_beams[:]:
                    beam["timer"] -= dt
                    if beam["timer"] <= 0:
                        game_state.laser_beams.remove(beam)
                    else:
                        # Check collision with enemies
                        for enemy in game_state.enemies[:]:
                            if line_rect_intersection(beam["start"], beam["end"], enemy["rect"]):
                                enemy["hp"] -= beam["damage"] * dt * 60  # Damage per frame
                                if enemy["hp"] <= 0:
                                    kill_enemy(enemy, game_state)
                
                # Update wave beams
                for beam in game_state.wave_beams[:]:
                    beam["timer"] -= dt
                    if beam["timer"] <= 0:
                        game_state.wave_beams.remove(beam)
                    else:
                        # Check collision with enemies
                        for enemy in game_state.enemies[:]:
                            hit_pos, dist = check_wave_beam_collision(beam["points"], enemy["rect"], wave_beam_width)
                            if hit_pos:
                                enemy["hp"] -= beam["damage"] * dt * 60
                                if enemy["hp"] <= 0:
                                    kill_enemy(enemy, game_state)
                
                # Enemy updates
                for enemy in game_state.enemies[:]:
                    if enemy.get("hp", 1) <= 0:
                        kill_enemy(enemy, game_state)
                        continue
                    
                    # Track enemy position for stuck detection
                    current_pos = pygame.Vector2(enemy["rect"].center)
                    last_pos = enemy.get("last_pos", current_pos)
                    stuck_timer = enemy.get("stuck_timer", 0.0)
                    
                    # Check if enemy has moved (distance threshold: 5 pixels)
                    distance_moved = current_pos.distance_to(last_pos)
                    if distance_moved < 5.0:
                        stuck_timer += dt
                    else:
                        stuck_timer = 0.0  # Reset if moved
                    
                    enemy["last_pos"] = current_pos
                    enemy["stuck_timer"] = stuck_timer
                    
                    # Enemy AI: find target and move towards it
                    enemy_pos = pygame.Vector2(enemy["rect"].center)
                    target_info = find_nearest_threat(enemy_pos, player, game_state.friendly_ai)
                    
                    if target_info:
                        target_pos, target_type = target_info
                        direction = vec_toward(enemy_pos.x, enemy_pos.y, target_pos.x, target_pos.y)
                        enemy_speed = enemy.get("speed", 80) * dt
                        
                        # When 5 or fewer enemies remain, all enemies move directly towards player
                        if len(game_state.enemies) <= 5:
                            # Direct movement towards player (no wandering when few enemies remain)
                            direction = vec_toward(enemy_pos.x, enemy_pos.y, player.centerx, player.centery)
                        else:
                            # If enemy is stuck (hasn't moved for 5 seconds), change direction away from obstacle
                            if stuck_timer >= 5.0:
                                # Move in opposite direction from target (away from obstacle)
                                direction = -direction
                                # Add random component to help escape
                                random_angle = random.uniform(0, 2 * math.pi)
                                escape_dir = pygame.Vector2(math.cos(random_angle), math.sin(random_angle))
                                direction = (direction + escape_dir * 0.5).normalize()
                                stuck_timer = 0.0  # Reset stuck timer after escape attempt
                                enemy["stuck_timer"] = stuck_timer
                            
                            # Add some random wandering to make enemies move around more
                            # Occasionally add a random offset to movement direction
                            if random.random() < 0.25:  # 25% chance per frame (increased from 10%)
                                wander_angle = random.uniform(-0.8, 0.8)  # Larger random angle (increased from 0.3)
                                cos_a = math.cos(wander_angle)
                                sin_a = math.sin(wander_angle)
                                direction = pygame.Vector2(
                                    direction.x * cos_a - direction.y * sin_a,
                                    direction.x * sin_a + direction.y * cos_a
                                ).normalize()
                            
                            # Additional random movement: sometimes move in a completely random direction
                            if random.random() < 0.05:  # 5% chance to move randomly instead of toward target
                                random_angle = random.uniform(0, 2 * math.pi)
                                direction = pygame.Vector2(math.cos(random_angle), math.sin(random_angle))
                        
                        # Dodge bullets if in range (only if more than 5 enemies remain)
                        if len(game_state.enemies) > 5:
                            dodge_threats = find_threats_in_dodge_range(enemy_pos, game_state.player_bullets, game_state.friendly_projectiles, 200.0)
                            if dodge_threats:
                                # Try to dodge by moving perpendicular
                                dodge_dir = pygame.Vector2(-direction.y, direction.x)  # Perpendicular
                                if random.random() < 0.5:
                                    dodge_dir = -dodge_dir
                                direction = (direction + dodge_dir * 0.5).normalize()
                        
                        move_x = int(direction.x * enemy_speed)
                        move_y = int(direction.y * enemy_speed)
                        move_enemy_with_push(enemy["rect"], move_x, move_y, blocks, game_state)
                    
                    # Queen-specific: Shield activation/deactivation system
                    if enemy.get("type") == "queen" and enemy.get("has_shield"):
                        shield_timer = enemy.get("shield_timer", 0.0) + dt
                        shield_active = enemy.get("shield_active", False)
                        shield_phase_duration = enemy.get("shield_phase_duration", 15.0)
                        shield_active_duration = enemy.get("shield_active_duration", 7.5)
                        
                        if shield_active:
                            # Shield is active - check if duration expired
                            if shield_timer >= shield_active_duration:
                                # Deactivate shield and reset timer for next phase
                                enemy["shield_active"] = False
                                enemy["shield_timer"] = 0.0
                                # Randomize next phase duration (10-20 seconds)
                                enemy["shield_phase_duration"] = random.uniform(10.0, 20.0)
                        else:
                            # Shield is inactive - check if phase duration expired
                            if shield_timer >= shield_phase_duration:
                                # Activate shield and reset timer
                                enemy["shield_active"] = True
                                enemy["shield_timer"] = 0.0
                                # Randomize active duration (5-10 seconds)
                                enemy["shield_active_duration"] = random.uniform(5.0, 10.0)
                        
                        enemy["shield_timer"] = shield_timer
                    
                    # Queen-specific: Missile firing (10 second cooldown)
                    if enemy.get("type") == "queen" and enemy.get("can_use_missiles"):
                        time_since_missile = enemy.get("time_since_missile", 999.0) + dt
                        missile_cooldown = enemy.get("missile_cooldown", 10.0)
                        
                        if time_since_missile >= missile_cooldown:
                            # Fire missile at player
                            if target_info:
                                target_pos, target_type = target_info
                                # Spawn missile targeting player
                                missile_rect = pygame.Rect(
                                    enemy["rect"].centerx - 8,
                                    enemy["rect"].centery - 8,
                                    16, 16
                                )
                                game_state.                                game_state.missiles.append({
                                    "rect": missile_rect,
                                    "vel": pygame.Vector2(0, 0),
                                    "target_enemy": None,  # Queen missiles target player, not enemy
                                    "target_player": True,  # Mark as player-targeting
                                    "speed": 500,
                                    "damage": missile_damage,
                                    "explosion_radius": 150,
                                    "source": "queen"
                                })
                                time_since_missile = 0.0
                        
                        enemy["time_since_missile"] = time_since_missile
                    
                    # Suicide enemy: detonate when close to player
                    if enemy.get("is_suicide"):
                        player_pos = pygame.Vector2(player.center)
                        enemy_pos = pygame.Vector2(enemy["rect"].center)
                        dist_to_player = (enemy_pos - player_pos).length()
                        detonation_distance = enemy.get("detonation_distance", 50)
                        
                        if dist_to_player <= detonation_distance:
                            # Detonate - create explosion
                            explosion_range = enemy.get("explosion_range", 150)
                            game_state.grenade_explosions.append({
                                "x": enemy["rect"].centerx,
                                "y": enemy["rect"].centery,
                                "radius": 0,
                                "max_radius": explosion_range,
                                "timer": 0.3,
                                "damage": 500,  # Same as player grenade
                            })
                            # Damage player if in range
                            if dist_to_player <= explosion_range:
                                # Shield blocks all damage - check shield first
                                if game_state.shield_active:
                                    # Shield is active - block damage
                                    pass
                                elif not (testing_mode and invulnerability_mode):
                                    # No shield - apply damage (overshield takes damage first, then player health)
                                    damage = 500
                                    if game_state.overshield > 0:
                                        damage_to_overshield = min(damage, game_state.overshield)
                                        game_state.overshield = max(0, game_state.overshield - damage)
                                        remaining_damage = damage - damage_to_overshield
                                    else:
                                        remaining_damage = damage
                                    if remaining_damage > 0:
                                        game_state.player_hp -= remaining_damage
                                    game_state.damage_taken += damage
                                    game_state.wave_damage_taken += damage  # Track damage for side quest
                                    if game_state.player_hp <= 0:
                                        if game_state.lives > 0:
                                            game_state.lives -= 1
                                            reset_after_death(game_state)
                                        else:
                                            # Game over - transition to name input
                                            game_state.final_score_for_high_score = game_state.score
                                            game_state.player_name_input = ""
                                            game_state.name_input_active = True
                                            state = STATE_NAME_INPUT
                            # Remove suicide enemy (despawns after detonation)
                            kill_enemy(enemy, game_state)
                            continue
                    
                    # Spawner enemy: spawn enemies during round
                    if enemy.get("is_spawner"):
                        time_since_spawn = enemy.get("time_since_spawn", 0.0) + dt
                        spawn_cooldown = enemy.get("spawn_cooldown", 5.0)
                        spawn_count = enemy.get("spawn_count", 0)
                        max_spawns = enemy.get("max_spawns", 3)
                        
                        if time_since_spawn >= spawn_cooldown and spawn_count < max_spawns:
                            # Spawn a new enemy
                            tmpl = random.choice(enemy_templates)
                            # Don't spawn another spawner or boss
                            while tmpl.get("type") in ["spawner", "FINAL_BOSS"]:
                                tmpl = random.choice(enemy_templates)
                            
                            spawned_enemy = make_enemy_from_template(tmpl, 1.0, 1.0)
                            spawned_enemy["rect"] = random_spawn_position((spawned_enemy["rect"].w, spawned_enemy["rect"].h), game_state)
                            spawned_enemy["spawned_by"] = enemy  # Track parent spawner
                            game_state.enemies.append(spawned_enemy)
                            enemy["spawn_count"] = spawn_count + 1
                            enemy["time_since_spawn"] = 0.0
                            
                            # Log spawn
                            if telemetry_enabled and telemetry:
                                enemies_spawned_ref = [game_state.enemies_spawned]
                                log_enemy_spawns([spawned_enemy], telemetry, game_state.run_time, enemies_spawned_ref)
                                game_state.enemies_spawned = enemies_spawned_ref[0]
                        else:
                            enemy["time_since_spawn"] = time_since_spawn
                    
                    # Patrol enemy: patrol outside border of map
                    if enemy.get("is_patrol"):
                        patrol_side = enemy.get("patrol_side", 0)
                        patrol_progress = enemy.get("patrol_progress", 0.0)
                        patrol_speed = 0.3 * dt  # Progress speed
                        
                        patrol_progress += patrol_speed
                        if patrol_progress >= 1.0:
                            patrol_progress = 0.0
                            patrol_side = (patrol_side + 1) % 4  # Cycle through sides
                            enemy["patrol_side"] = patrol_side
                        
                        enemy["patrol_progress"] = patrol_progress
                        
                        # Calculate position along border
                        border_margin = 50  # Distance from edge
                        if patrol_side == 0:  # Top
                            x = border_margin + (WIDTH - 2 * border_margin) * patrol_progress
                            y = border_margin
                        elif patrol_side == 1:  # Right
                            x = WIDTH - border_margin
                            y = border_margin + (HEIGHT - 2 * border_margin) * patrol_progress
                        elif patrol_side == 2:  # Bottom
                            x = WIDTH - border_margin - (WIDTH - 2 * border_margin) * patrol_progress
                            y = HEIGHT - border_margin
                        else:  # Left
                            x = border_margin
                            y = HEIGHT - border_margin - (HEIGHT - 2 * border_margin) * patrol_progress
                        
                        enemy["rect"].center = (int(x), int(y))
                    
                    # Reflector enemy: turn shield towards player (slow turn speed)
                    if enemy.get("has_reflective_shield"):
                        if target_info:
                            target_pos, target_type = target_info
                            enemy_center = pygame.Vector2(enemy["rect"].center)
                            to_target = (target_pos - enemy_center).normalize()
                            target_angle = math.atan2(to_target.y, to_target.x)
                            
                            # Turn shield towards target (slow turn speed)
                            shield_angle = enemy.get("shield_angle", 0.0)
                            turn_speed = enemy.get("turn_speed", 0.5) * dt
                            
                            # Calculate angle difference
                            angle_diff = target_angle - shield_angle
                            # Normalize to [-pi, pi]
                            while angle_diff > math.pi:
                                angle_diff -= 2 * math.pi
                            while angle_diff < -math.pi:
                                angle_diff += 2 * math.pi
                            
                            # Turn towards target
                            if abs(angle_diff) > turn_speed:
                                shield_angle += turn_speed if angle_diff > 0 else -turn_speed
                            else:
                                shield_angle = target_angle
                            
                            enemy["shield_angle"] = shield_angle
                    
                    # Enemy shooting (reflector doesn't shoot normally)
                    if not enemy.get("has_reflective_shield"):
                        enemy["shoot_cooldown"] = enemy.get("shoot_cooldown", 999.0) + dt
                        if enemy["shoot_cooldown"] >= enemy.get("shoot_cooldown_time", 1.0):
                            if target_info:
                                target_pos, target_type = target_info
                                if enemy.get("is_predictive", False):
                                    spawn_enemy_projectile_predictive(enemy, direction, game_state)
                                else:
                                    spawn_enemy_projectile(enemy, game_state)
                            enemy["shoot_cooldown"] = 0.0
                
                # Bullet/projectile updates
                for bullet in game_state.player_bullets[:]:
                    bullet["rect"].x += int(bullet["vel"].x * dt)
                    bullet["rect"].y += int(bullet["vel"].y * dt)
                    
                    # Remove if off screen
                    if rect_offscreen(bullet["rect"]):
                        if bullet in game_state.player_bullets:
                            game_state.player_bullets.remove(bullet)
                        continue
                    
                    # Check collision with enemies
                    for enemy in game_state.enemies[:]:
                        if bullet["rect"].colliderect(enemy["rect"]):
                            # Reflector enemy: reflective shield absorbs damage and fires back
                            if enemy.get("has_reflective_shield"):
                                # Calculate angle from enemy to bullet
                                enemy_center = pygame.Vector2(enemy["rect"].center)
                                bullet_center = pygame.Vector2(bullet["rect"].center)
                                bullet_dir = (bullet_center - enemy_center).normalize()
                                
                                # Check if bullet hits the shield (front-facing)
                                shield_angle = enemy.get("shield_angle", 0.0)
                                shield_dir = pygame.Vector2(math.cos(shield_angle), math.sin(shield_angle))
                                
                                # Check if bullet is coming from shield direction (within 90 degrees)
                                dot_product = bullet_dir.dot(-shield_dir)  # Negative because shield faces away from enemy
                                if dot_product > 0.0:  # Bullet hits shield
                                    # Absorb damage into shield
                                    damage = bullet.get("damage", game_state.player_bullet_damage)
                                    enemy["shield_hp"] = enemy.get("shield_hp", 0) + damage
                                    
                                    # Fire back reflected projectile
                                    if enemy["shield_hp"] > 0:
                                        reflected_dir = -bullet_dir  # Reflect back
                                        reflected_proj = pygame.Rect(
                                            enemy["rect"].centerx - enemy_projectile_size[0] // 2,
                                            enemy["rect"].centery - enemy_projectile_size[1] // 2,
                                            enemy_projectile_size[0],
                                            enemy_projectile_size[1]
                                        )
                                        game_state.enemy_projectiles.append({
                                            "rect": reflected_proj,
                                            "vel": reflected_dir * enemy.get("projectile_speed", 300),
                                            "enemy_type": enemy["type"],
                                            "color": enemy.get("projectile_color", enemy_projectiles_color),
                                            "shape": enemy.get("projectile_shape", "circle"),
                                            "bounces": 0,
                                        })
                                        enemy["shield_hp"] = 0  # Reset shield HP after firing
                                    
                                    # Remove bullet (shield blocks it)
                                    if bullet in game_state.player_bullets:
                                        game_state.player_bullets.remove(bullet)
                                    break
                                else:
                                    # Bullet hits enemy from behind (no shield protection)
                                    damage = bullet.get("damage", game_state.player_bullet_damage)
                                    enemy["hp"] -= damage
                                    
                                    # Damage number (displayed for 2 seconds)
                                    game_state.damage_numbers.append({
                                        "x": enemy["rect"].centerx,
                                        "y": enemy["rect"].y - 20,
                                        "damage": int(damage),  # Display as integer
                                        "timer": 2.0,  # Disappear after 2 seconds
                                        "color": (255, 255, 100)
                                    })
                                    
                                    if enemy["hp"] <= 0:
                                        kill_enemy(enemy, game_state)
                                    
                                    # Remove bullet (unless it has penetration)
                                    if bullet.get("penetration", 0) <= 0:
                                        if bullet in game_state.player_bullets:
                                            game_state.player_bullets.remove(bullet)
                                        break
                                    else:
                                        bullet["penetration"] -= 1
                            else:
                                # Normal enemy collision
                                damage = bullet.get("damage", game_state.player_bullet_damage)
                                enemy["hp"] -= damage
                                
                                # Damage number (displayed for 2 seconds)
                                game_state.damage_numbers.append({
                                    "x": enemy["rect"].centerx,
                                    "y": enemy["rect"].y - 20,
                                    "damage": int(damage),  # Display as integer
                                    "timer": 2.0,  # Disappear after 2 seconds
                                    "color": (255, 255, 100)
                                })
                                
                                if enemy["hp"] <= 0:
                                    kill_enemy(enemy, game_state)
                                
                                # Remove bullet (unless it has penetration)
                                if bullet.get("penetration", 0) <= 0:
                                    if bullet in game_state.player_bullets:
                                        game_state.player_bullets.remove(bullet)
                                    break
                                else:
                                    bullet["penetration"] -= 1
                    
                    # Check collision with blocks and obstacles
                    # Bullets can only pass through destructible walls if they have penetration > 0
                    # All other obstacles (giant blocks, trapezoids, triangles) always stop bullets
                    if not bullet.get("removed", False):
                        # Check destructible blocks (can be penetrated with penetration > 0)
                        for block in destructible_blocks + moveable_destructible_blocks:
                            if block.get("is_destructible") and bullet["rect"].colliderect(block["rect"]):
                                # If bullet has penetration, it passes through blocks (doesn't stop)
                                if bullet.get("penetration", 0) > 0:
                                    # Bullet passes through, but still damages the block
                                    block["hp"] -= bullet.get("damage", game_state.player_bullet_damage)
                                    if block["hp"] <= 0:
                                        destructible_blocks.remove(block) if block in destructible_blocks else moveable_destructible_blocks.remove(block)
                                    # Continue moving through block
                                else:
                                    # No penetration - bullet stops at block
                                    block["hp"] -= bullet.get("damage", game_state.player_bullet_damage)
                                    if block["hp"] <= 0:
                                        destructible_blocks.remove(block) if block in destructible_blocks else moveable_destructible_blocks.remove(block)
                                    if not bullet.get("bouncing", False):
                                        if bullet in game_state.player_bullets:
                                            game_state.player_bullets.remove(bullet)
                                        bullet["removed"] = True
                                        break
                                    else:
                                        # Bounce bullet
                                        bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
                        
                        # Check giant blocks (always stop bullets, no penetration)
                        if not bullet.get("removed", False):
                            for block in giant_blocks + super_giant_blocks:
                                if bullet["rect"].colliderect(block["rect"]):
                                    if not bullet.get("bouncing", False):
                                        if bullet in game_state.player_bullets:
                                            game_state.player_bullets.remove(bullet)
                                        bullet["removed"] = True
                                        break
                                    else:
                                        # Bounce bullet
                                        bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
                        
                        # Check trapezoid blocks (always stop bullets, no penetration)
                        if not bullet.get("removed", False):
                            for tb in trapezoid_blocks:
                                if bullet["rect"].colliderect(tb.get("bounding_rect", tb.get("rect"))):
                                    if not bullet.get("bouncing", False):
                                        if bullet in game_state.player_bullets:
                                            game_state.player_bullets.remove(bullet)
                                        bullet["removed"] = True
                                        break
                                    else:
                                        # Bounce bullet
                                        bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
                        
                        # Check triangle blocks (always stop bullets, no penetration)
                        if not bullet.get("removed", False):
                            for tr in triangle_blocks:
                                if bullet["rect"].colliderect(tr.get("bounding_rect", tr.get("rect"))):
                                    if not bullet.get("bouncing", False):
                                        if bullet in game_state.player_bullets:
                                            game_state.player_bullets.remove(bullet)
                                        bullet["removed"] = True
                                        break
                                    else:
                                        # Bounce bullet
                                        bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
                        
                        # Check hazard obstacles (paraboloids/trapezoids) - bullets push hazards
                        if not bullet.get("removed", False):
                            for hazard in hazard_obstacles:
                                if hazard.get("points") and len(hazard["points"]) > 2:
                                    bullet_center = pygame.Vector2(bullet["rect"].center)
                                    # Check if bullet is inside hazard shape
                                    if check_point_in_hazard(bullet_center, hazard["points"], hazard["bounding_rect"]):
                                        # Push hazard in direction of bullet velocity
                                        bullet_vel = bullet.get("vel", pygame.Vector2(0, 0))
                                        if bullet_vel.length_squared() > 0:
                                            push_force = bullet_vel.normalize() * 200.0  # Push force
                                            hazard["velocity"] += push_force * dt
                                        # Remove bullet (hazards stop bullets)
                                        if bullet in game_state.player_bullets:
                                            game_state.player_bullets.remove(bullet)
                                        bullet["removed"] = True
                                        break
                
                for proj in game_state.enemy_projectiles[:]:
                    proj["rect"].x += int(proj["vel"].x * dt)
                    proj["rect"].y += int(proj["vel"].y * dt)
                    
                    # Track if projectile was removed to avoid double removal
                    proj_removed = False
                    
                    # Remove projectiles that have exceeded their lifetime
                    if "lifetime" in proj:
                        proj["lifetime"] -= dt
                        if proj["lifetime"] <= 0:
                            if proj in game_state.enemy_projectiles:
                                game_state.enemy_projectiles.remove(proj)
                            proj_removed = True
                            continue
                    
                    if not proj_removed and rect_offscreen(proj["rect"]):
                        if proj in game_state.enemy_projectiles:
                            game_state.enemy_projectiles.remove(proj)
                        proj_removed = True
                        continue
                    
                    # Check collision with destructible blocks
                    if not proj_removed:
                        for block in destructible_blocks + moveable_destructible_blocks:
                            if block.get("is_destructible") and proj["rect"].colliderect(block["rect"]):
                                block["hp"] -= proj.get("damage", 10)
                                if block["hp"] <= 0:
                                    destructible_blocks.remove(block) if block in destructible_blocks else moveable_destructible_blocks.remove(block)
                                if proj in game_state.enemy_projectiles:
                                    game_state.enemy_projectiles.remove(proj)
                                proj_removed = True
                                break
                    
                    # Check collision with player (only if not already removed)
                    if not proj_removed and proj["rect"].colliderect(player):
                        # Shield blocks all damage - check shield first
                        if game_state.shield_active:
                            # Shield is active - block damage, remove projectile
                            if proj in game_state.enemy_projectiles:
                                game_state.enemy_projectiles.remove(proj)
                        elif not (testing_mode and invulnerability_mode):
                            # No shield - apply damage (overshield takes damage first, then player health)
                            damage = proj.get("damage", 10)
                            if game_state.overshield > 0:
                                damage_to_overshield = min(damage, game_state.overshield)
                                game_state.overshield = max(0, game_state.overshield - damage)
                                remaining_damage = damage - damage_to_overshield
                            else:
                                remaining_damage = damage
                            if remaining_damage > 0:
                                game_state.player_hp -= remaining_damage
                            game_state.damage_taken += damage
                            game_state.wave_damage_taken += damage  # Track damage for side quest
                            if game_state.player_hp <= 0:
                                if game_state.lives > 0:
                                    game_state.lives -= 1
                                    reset_after_death(game_state)
                                else:
                                    # Game over - transition to name input
                                    game_state.final_score_for_high_score = game_state.score
                                    game_state.player_name_input = ""
                                    game_state.name_input_active = True
                                    state = STATE_NAME_INPUT
                            if proj in game_state.enemy_projectiles:
                                game_state.enemy_projectiles.remove(proj)
                        else:
                            # Testing mode with invulnerability - block damage
                            if proj in game_state.enemy_projectiles:
                                game_state.enemy_projectiles.remove(proj)
                
                # Pickup collection
                for pickup in game_state.pickups[:]:
                    if player.colliderect(pickup["rect"]):
                        # Create visual effect when picking up
                        create_pickup_collection_effect(pickup["rect"].centerx, pickup["rect"].centery, pickup["color"], game_state)
                        apply_pickup_effect(pickup["type"], game_state)
                        game_state.pickups.remove(pickup)
                
                # Health regeneration (from pickups)
                if game_state.player_health_regen_rate > 0:
                    regen_amount = game_state.player_health_regen_rate * dt
                    game_state.player_hp = min(game_state.player_max_hp, game_state.player_hp + regen_amount)
                
                # Health zone interaction
                if player.colliderect(moving_health_zone["rect"]):
                    if game_state.player_hp < game_state.player_max_hp:
                        game_state.player_hp = min(game_state.player_max_hp, game_state.player_hp + 50 * dt)  # Heal over time
                
                # Friendly AI updates
                update_friendly_ai(
                    game_state.friendly_ai,
                    game_state.enemies,
                    blocks,
                    dt,
                    find_nearest_enemy,
                    vec_toward,
                    lambda rect, mx, my, bl: move_enemy_with_push(rect, mx, my, bl, game_state),
                    lambda f, t: spawn_friendly_projectile(f, t, game_state.friendly_projectiles, vec_toward, telemetry, game_state.run_time),
                )
                
                # Friendly projectile updates
                for proj in game_state.friendly_projectiles[:]:
                    proj["rect"].x += int(proj["vel"].x * dt)
                    proj["rect"].y += int(proj["vel"].y * dt)
                    
                    if rect_offscreen(proj["rect"]):
                        game_state.friendly_projectiles.remove(proj)
                        continue
                    
                    # Check collision with destructible blocks
                    for block in destructible_blocks + moveable_destructible_blocks:
                        if block.get("is_destructible") and proj["rect"].colliderect(block["rect"]):
                            block["hp"] -= proj.get("damage", 20)
                            if block["hp"] <= 0:
                                destructible_blocks.remove(block) if block in destructible_blocks else moveable_destructible_blocks.remove(block)
                            game_state.friendly_projectiles.remove(proj)
                            break
                    
                    for enemy in game_state.enemies[:]:
                        if proj["rect"].colliderect(enemy["rect"]):
                            damage = proj.get("damage", 20)
                            enemy["hp"] -= damage
                            
                            # Damage number (displayed for 2 seconds)
                            game_state.damage_numbers.append({
                                "x": enemy["rect"].centerx,
                                "y": enemy["rect"].y - 20,
                                "damage": int(damage),  # Display as integer
                                "timer": 2.0,  # Disappear after 2 seconds
                                "color": (255, 255, 100)
                            })
                            
                            if enemy["hp"] <= 0:
                                kill_enemy(enemy, game_state)
                            game_state.friendly_projectiles.remove(proj)
                            break
                
                # Grenade explosion updates
                for explosion in game_state.grenade_explosions[:]:
                    explosion["timer"] -= dt
                    explosion["radius"] = int(explosion["max_radius"] * (1.0 - explosion["timer"] / 0.3))
                    
                    if explosion["timer"] <= 0:
                        game_state.grenade_explosions.remove(explosion)
                        continue
                    
                    # Damage enemies and blocks in radius
                    explosion_pos = pygame.Vector2(explosion["x"], explosion["y"])
                    for enemy in game_state.enemies[:]:
                        enemy_pos = pygame.Vector2(enemy["rect"].center)
                        dist = (enemy_pos - explosion_pos).length()
                        if dist <= explosion["radius"]:
                            damage = explosion["damage"]
                            enemy["hp"] -= damage
                            
                            # Damage number (displayed for 2 seconds)
                            game_state.damage_numbers.append({
                                "x": enemy["rect"].centerx,
                                "y": enemy["rect"].y - 20,
                                "damage": int(damage),  # Display as integer
                                "timer": 2.0,  # Disappear after 2 seconds
                                "color": (255, 200, 100)  # Slightly different color for explosion damage
                            })
                            
                            if enemy["hp"] <= 0:
                                kill_enemy(enemy, game_state)
                    
                    # Damage player if in explosion radius (make player immune to own bomb damage)
                    player_pos = pygame.Vector2(player.center)
                    player_dist = (player_pos - explosion_pos).length()
                    if player_dist <= explosion["radius"]:
                        # Player is immune to their own grenade/bomb damage
                        # Only damage player if explosion is from enemy (not player grenade)
                        if explosion.get("source") != "player":
                            # Shield blocks all damage - check shield first
                            if game_state.shield_active:
                                # Shield is active - block damage
                                pass
                            elif not (testing_mode and invulnerability_mode):
                                # No shield - apply damage (overshield takes damage first, then player health)
                                damage = explosion.get("damage", 500)
                                if game_state.overshield > 0:
                                    damage_to_overshield = min(damage, game_state.overshield)
                                    game_state.overshield = max(0, game_state.overshield - damage)
                                    remaining_damage = damage - damage_to_overshield
                                else:
                                    remaining_damage = damage
                                if remaining_damage > 0:
                                    game_state.player_hp -= remaining_damage
                                game_state.damage_taken += damage
                                game_state.wave_damage_taken += damage  # Track damage for side quest
                                if game_state.player_hp <= 0:
                                    if game_state.lives > 0:
                                        game_state.lives -= 1
                                        reset_after_death(game_state)
                                    else:
                                        # Game over - transition to name input
                                        game_state.final_score_for_high_score = game_state.score
                                        game_state.player_name_input = ""
                                        game_state.name_input_active = True
                                        state = STATE_NAME_INPUT
                    
                    # Damage destructible blocks
                    for block in destructible_blocks[:] + moveable_destructible_blocks[:]:
                        if block.get("is_destructible"):
                            block_pos = pygame.Vector2(block["rect"].center)
                            dist = (block_pos - explosion_pos).length()
                            if dist <= explosion["radius"]:
                                block["hp"] -= explosion["damage"]
                                if block["hp"] <= 0:
                                    if block in destructible_blocks:
                                        destructible_blocks.remove(block)
                                    else:
                                        moveable_destructible_blocks.remove(block)
                
                # Missile updates
                for missile in game_state.missiles[:]:
                    # Handle player-targeting missiles (from queen)
                    if missile.get("target_player"):
                        # Seek player
                        target_pos = pygame.Vector2(player.center)
                        missile_pos = pygame.Vector2(missile["rect"].center)
                        direction = (target_pos - missile_pos).normalize()
                        missile["vel"] = direction * missile["speed"]
                    elif missile.get("target_enemy"):
                        # Handle enemy-targeting missiles (from player)
                        if missile["target_enemy"] not in game_state.enemies:
                            # Target died, find new target
                            target_enemy = None
                            min_dist = float("inf")
                            for enemy in game_state.enemies:
                                dist = (pygame.Vector2(enemy["rect"].center) - pygame.Vector2(missile["rect"].center)).length_squared()
                                if dist < min_dist:
                                    min_dist = dist
                                    target_enemy = enemy
                            missile["target_enemy"] = target_enemy
                        
                        if missile["target_enemy"]:
                            # Seek target
                            target_pos = pygame.Vector2(missile["target_enemy"]["rect"].center)
                            missile_pos = pygame.Vector2(missile["rect"].center)
                            direction = (target_pos - missile_pos).normalize()
                            missile["vel"] = direction * missile["speed"]
                    
                    missile["rect"].x += int(missile["vel"].x * dt)
                    missile["rect"].y += int(missile["vel"].y * dt)
                    
                    if rect_offscreen(missile["rect"]):
                        game_state.missiles.remove(missile)
                        continue
                    
                    # Check collision with target
                    hit_target = False
                    if missile.get("target_player") and missile["rect"].colliderect(player):
                        # Queen missile hit player
                        hit_target = True
                        # Shield blocks all damage - check shield first
                        if game_state.shield_active:
                            # Shield is active - block damage
                            pass
                        elif not (testing_mode and invulnerability_mode):
                            # No shield - apply damage (overshield takes damage first, then player health)
                            damage = missile.get("damage", missile_damage)
                            if game_state.overshield > 0:
                                damage_to_overshield = min(damage, game_state.overshield)
                                game_state.overshield = max(0, game_state.overshield - damage)
                                remaining_damage = damage - damage_to_overshield
                            else:
                                remaining_damage = damage
                            if remaining_damage > 0:
                                game_state.player_hp -= remaining_damage
                            game_state.damage_taken += damage
                            game_state.wave_damage_taken += damage  # Track damage for side quest
                            if game_state.player_hp <= 0:
                                if game_state.lives > 0:
                                    game_state.lives -= 1
                                    reset_after_death(game_state)
                                else:
                                    # Game over - transition to name input
                                    game_state.final_score_for_high_score = game_state.score
                                    game_state.player_name_input = ""
                                    game_state.name_input_active = True
                                    state = STATE_NAME_INPUT
                    elif missile.get("target_enemy") and missile["rect"].colliderect(missile["target_enemy"]["rect"]):
                        # Player missile hit enemy
                        hit_target = True
                    
                    if hit_target:
                        # Explode
                        explosion_pos = pygame.Vector2(missile["rect"].center)
                        # Damage enemies in explosion radius
                        for enemy in game_state.enemies[:]:
                            enemy_pos = pygame.Vector2(enemy["rect"].center)
                            dist = (enemy_pos - explosion_pos).length()
                            if dist <= missile["explosion_radius"]:
                                damage = missile["damage"]
                                enemy["hp"] -= damage
                                
                                # Damage number (displayed for 2 seconds)
                                game_state.damage_numbers.append({
                                    "x": enemy["rect"].centerx,
                                    "y": enemy["rect"].y - 20,
                                    "damage": int(damage),  # Display as integer
                                    "timer": 2.0,  # Disappear after 2 seconds
                                    "color": (255, 150, 50)  # Orange color for missile damage
                                })
                                
                                if enemy["hp"] <= 0:
                                    kill_enemy(enemy, game_state)
                        
                        # Damage player if in explosion radius (for queen missiles)
                        if missile.get("target_player"):
                            player_pos = pygame.Vector2(player.center)
                            dist = (player_pos - explosion_pos).length()
                            if dist <= missile["explosion_radius"]:
                                # Shield blocks all damage - check shield first
                                if game_state.shield_active:
                                    # Shield is active - block damage
                                    pass
                                elif not (testing_mode and invulnerability_mode):
                                    # No shield - apply damage (overshield takes damage first, then player health)
                                    damage = missile.get("damage", missile_damage)
                                    if game_state.overshield > 0:
                                        damage_to_overshield = min(damage, game_state.overshield)
                                        game_state.overshield = max(0, game_state.overshield - damage)
                                        remaining_damage = damage - damage_to_overshield
                                    else:
                                        remaining_damage = damage
                                    if remaining_damage > 0:
                                        game_state.player_hp -= remaining_damage
                                    game_state.damage_taken += damage
                                    game_state.wave_damage_taken += damage  # Track damage for side quest
                                    if game_state.player_hp <= 0:
                                        if game_state.lives > 0:
                                            game_state.lives -= 1
                                            reset_after_death(game_state)
                                        else:
                                            # Game over - transition to name input
                                            game_state.final_score_for_high_score = game_state.score
                                            game_state.player_name_input = ""
                                            game_state.name_input_active = True
                                            state = STATE_NAME_INPUT
                        
                        game_state.missiles.remove(missile)
                
                # Wave management
                if game_state.wave_active and len(game_state.enemies) == 0:
                    game_state.time_to_next_wave += dt
                    if game_state.time_to_next_wave >= 3.0:  # 3 second countdown between waves
                        # Check side quest: Perfect Wave (no damage taken)
                        if game_state.wave_damage_taken == 0 and game_state.side_quests["no_hit_wave"]["active"]:
                            # Award bonus points
                            bonus = game_state.side_quests["no_hit_wave"]["bonus_points"]
                            game_state.score += bonus
                            game_state.side_quests["no_hit_wave"]["completed"] = True
                            # Show bonus message
                            game_state.damage_numbers.append({
                                "x": WIDTH // 2,
                                "y": HEIGHT // 2,
                                "value": f"PERFECT WAVE! +{bonus}",
                                "timer": 3.0,
                                "color": (255, 215, 0)  # Gold color
                            })
                        
                        game_state.wave_number += 1
                        game_state.wave_in_level += 1
                        if game_state.wave_in_level > 3:
                            game_state.wave_in_level = 1
                            game_state.current_level += 1
                            if game_state.current_level > game_state.max_level:
                                state = STATE_VICTORY
                                game_state.wave_active = False
                        if state != STATE_VICTORY:
                            start_wave(game_state.wave_number, game_state)
                            game_state.time_to_next_wave = 0.0
            
            # Rendering
            # Clear screen with background color based on level theme
            theme = level_themes.get(game_state.current_level, level_themes[1])
            screen.fill(theme["bg_color"])
            
            # Draw game elements based on state
            if state == STATE_MENU:
                # Menu rendering
                draw_centered_text(screen, font, big_font, WIDTH, "MOUSE AIM SHOOTER", HEIGHT // 4, use_big=True)
                
                y_offset = HEIGHT // 2
                if menu_section == 0:
                    # Difficulty selection
                    draw_centered_text(screen, font, big_font, WIDTH, "Select Difficulty:", y_offset - 60)
                    for i, diff in enumerate(difficulty_options):
                        color = (255, 255, 0) if i == difficulty_selected else (200, 200, 200)
                        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == difficulty_selected else '  '} {diff}", y_offset + i * 40, color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 1:
                    # Aiming mode selection
                    draw_centered_text(screen, font, big_font, WIDTH, "Select Aiming Mode:", y_offset - 60)
                    modes = ["Mouse", "Arrow Keys"]
                    for i, mode in enumerate(modes):
                        color = (255, 255, 0) if i == aiming_mode_selected else (200, 200, 200)
                        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == aiming_mode_selected else '  '} {mode}", y_offset + i * 40, color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 1.5:
                    # Character profile yes/no
                    draw_centered_text(screen, font, big_font, WIDTH, "Use Character Profile?", y_offset - 60)
                    options = ["No", "Yes"]
                    for i, opt in enumerate(options):
                        color = (255, 255, 0) if i == use_character_profile_selected else (200, 200, 200)
                        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == use_character_profile_selected else '  '} {opt}", y_offset + i * 40, color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 2:
                    # Character profile selection
                    draw_centered_text(screen, font, big_font, WIDTH, "Character Profile:", y_offset - 60)
                    for i, profile in enumerate(character_profile_options):
                        color = (255, 255, 0) if i == character_profile_selected else (200, 200, 200)
                        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == character_profile_selected else '  '} {profile}", y_offset + i * 40, color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 3:
                    # HUD options
                    draw_centered_text(screen, font, big_font, WIDTH, "HUD Options:", y_offset - 60)
                    options = ["Show Metrics", "Hide Metrics"]
                    for i, opt in enumerate(options):
                        color = (255, 255, 0) if i == ui_show_metrics_selected else (200, 200, 200)
                        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == ui_show_metrics_selected else '  '} {opt}", y_offset + i * 40, color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 3.5:
                    # Telemetry options
                    draw_centered_text(screen, font, big_font, WIDTH, "Telemetry:", y_offset - 60)
                    options = ["Enabled", "Disabled"]
                    for i, opt in enumerate(options):
                        color = (255, 255, 0) if i == ui_telemetry_enabled_selected else (200, 200, 200)
                        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == ui_telemetry_enabled_selected else '  '} {opt}", y_offset + i * 40, color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 4:
                    # Beam/weapon selection (if testing mode)
                    if testing_mode:
                        draw_centered_text(screen, font, big_font, WIDTH, "Select Weapon:", y_offset - 60)
                        for i, weapon in enumerate(weapon_selection_options):
                            color = (255, 255, 0) if i == beam_selection_selected else (200, 200, 200)
                            draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == beam_selection_selected else '  '} {weapon}", y_offset + i * 30, color)
                        draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
                    else:
                        menu_section = 5  # Skip to start
                
                elif menu_section == 4.5:
                    # Testing options (testing mode only)
                    draw_centered_text(screen, font, big_font, WIDTH, "Testing Options:", y_offset - 60)
                    invuln_color = (255, 255, 0) if invulnerability_mode else (200, 200, 200)
                    draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if invulnerability_mode else '  '} Invulnerability: {'ON' if invulnerability_mode else 'OFF'}", y_offset, invuln_color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to toggle, LEFT to go back, RIGHT/ENTER to start", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 5:
                    # Start game
                    draw_centered_text(screen, font, big_font, WIDTH, "Ready to Start!", y_offset)
                    draw_centered_text(screen, font, big_font, WIDTH, "Press ENTER or SPACE to begin", y_offset + 60, (150, 150, 150))
                    draw_centered_text(screen, font, big_font, WIDTH, "Press LEFT to go back", y_offset + 100, (150, 150, 150))
                
                elif menu_section == 6:
                    # Custom profile creator
                    draw_centered_text(screen, font, big_font, WIDTH, "Custom Profile Creator:", y_offset - 100)
                    for i, stat_name in enumerate(custom_profile_stats_list):
                        stat_key = custom_profile_stats_keys[i]
                        stat_value = custom_profile_stats[stat_key]
                        color = (255, 255, 0) if i == custom_profile_stat_selected else (200, 200, 200)
                        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == custom_profile_stat_selected else '  '} {stat_name}: {stat_value:.1f}x", y_offset + i * 35, color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select stat, LEFT/RIGHT to adjust, ENTER to continue", HEIGHT - 100, (150, 150, 150))
                
                elif menu_section == 7:
                    # Class selection
                    draw_centered_text(screen, font, big_font, WIDTH, "Select Class:", y_offset - 60)
                    for i, cls in enumerate(player_class_options):
                        color = (255, 255, 0) if i == player_class_selected else (200, 200, 200)
                        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == player_class_selected else '  '} {cls}", y_offset + i * 40, color)
                    draw_centered_text(screen, font, big_font, WIDTH, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", HEIGHT - 100, (150, 150, 150))
            elif state == STATE_PLAYING or state == STATE_ENDURANCE:
                # Draw all game elements
                
                # Draw trapezoid blocks (cached surfaces)
                for tr in trapezoid_blocks:
                    block_id = f"trap_{id(tr)}"
                    if block_id not in _cached_trapezoid_surfaces:
                        # Create cached surface for this trapezoid
                        points = tr.get("points", [])
                        if points:
                            min_x = min(p[0] for p in points)
                            max_x = max(p[0] for p in points)
                            min_y = min(p[1] for p in points)
                            max_y = max(p[1] for p in points)
                            cached_surf = pygame.Surface((max_x - min_x + 10, max_y - min_y + 10), pygame.SRCALPHA)
                            offset_points = [(p[0] - min_x + 5, p[1] - min_y + 5) for p in points]
                            pygame.draw.polygon(cached_surf, tr["color"], offset_points)
                            pygame.draw.polygon(cached_surf, (255, 255, 255), offset_points, 2)
                            _cached_trapezoid_surfaces[block_id] = (cached_surf, (min_x - 5, min_y - 5))
                    
                    if block_id in _cached_trapezoid_surfaces:
                        cached_surf, offset = _cached_trapezoid_surfaces[block_id]
                        screen.blit(cached_surf, offset)
                
                # Draw triangle blocks (cached surfaces)
                for tr in triangle_blocks:
                    block_id = f"tri_{id(tr)}"
                    if block_id not in _cached_triangle_surfaces:
                        points = tr.get("points", [])
                        if points:
                            min_x = min(p[0] for p in points)
                            max_x = max(p[0] for p in points)
                            min_y = min(p[1] for p in points)
                            max_y = max(p[1] for p in points)
                            cached_surf = pygame.Surface((max_x - min_x + 10, max_y - min_y + 10), pygame.SRCALPHA)
                            offset_points = [(p[0] - min_x + 5, p[1] - min_y + 5) for p in points]
                            pygame.draw.polygon(cached_surf, tr["color"], offset_points)
                            pygame.draw.polygon(cached_surf, (255, 255, 255), offset_points, 2)
                            _cached_triangle_surfaces[block_id] = (cached_surf, (min_x - 5, min_y - 5))
                    
                    if block_id in _cached_triangle_surfaces:
                        cached_surf, offset = _cached_triangle_surfaces[block_id]
                        screen.blit(cached_surf, offset)
                
                # Draw destructible blocks
                for block in destructible_blocks:
                    if block.get("is_destructible") and block.get("hp", 0) > 0:
                        draw_cracked_brick_wall_texture(screen, block["rect"], block.get("crack_level", 0))
                    else:
                        draw_silver_wall_texture(screen, block["rect"])
                
                # Draw moveable destructible blocks
                for block in moveable_destructible_blocks:
                    if block.get("is_destructible") and block.get("hp", 0) > 0:
                        draw_cracked_brick_wall_texture(screen, block["rect"], block.get("crack_level", 0))
                    else:
                        draw_silver_wall_texture(screen, block["rect"])
                
                # Draw giant blocks
                for block in giant_blocks:
                    draw_silver_wall_texture(screen, block["rect"])
                
                # Draw super giant blocks
                for block in super_giant_blocks:
                    draw_silver_wall_texture(screen, block["rect"])
                
                # Draw hazard obstacles (paraboloids/trapezoids)
                for hazard in hazard_obstacles:
                    points = hazard.get("points", [])
                    if len(points) >= 3:
                        pygame.draw.polygon(screen, hazard["color"], points)
                        pygame.draw.polygon(screen, (255, 255, 255), points, 2)
                
                # Draw moving health recovery zone
                zone = moving_health_zone
                zone_center = (zone["rect"].centerx, zone["rect"].centery)
                zone_width = zone["rect"].w
                zone_height = zone["rect"].h
                use_triangle = (game_state.wave_in_level % 2 == 0)
                
                zone_surf = pygame.Surface((zone["rect"].w + 20, zone["rect"].h + 20), pygame.SRCALPHA)
                
                if use_triangle:
                    triangle_points = [
                        (zone_width // 2, 10),
                        (10, zone_height + 10),
                        (zone_width + 10, zone_height + 10)
                    ]
                    pygame.draw.polygon(zone_surf, zone["color"], triangle_points)
                    screen.blit(zone_surf, (zone["rect"].x - 10, zone["rect"].y - 10))
                    pulse = 0.5 + 0.5 * math.sin(game_state.run_time * 3.0)
                    border_alpha = int(150 + 100 * pulse)
                    border_color = (50, 255, 50)
                    pygame.draw.polygon(screen, border_color, [
                        (zone_center[0], zone["rect"].y),
                        (zone["rect"].x, zone["rect"].bottom),
                        (zone["rect"].right, zone["rect"].bottom)
                    ], 3)
                else:
                    pygame.draw.rect(zone_surf, zone["color"], (10, 10, zone["rect"].w, zone["rect"].h))
                    screen.blit(zone_surf, (zone["rect"].x - 10, zone["rect"].y - 10))
                    pulse = 0.5 + 0.5 * math.sin(game_state.run_time * 3.0)
                    border_alpha = int(150 + 100 * pulse)
                    border_color = (50, 255, 50)
                    pygame.draw.rect(screen, border_color, zone["rect"], 3)
                
                # Draw pickups
                for pickup in game_state.pickups:
                    pygame.draw.circle(screen, pickup["color"], pickup["rect"].center, pickup["rect"].w // 2)
                    pygame.draw.circle(screen, (255, 255, 255), pickup["rect"].center, pickup["rect"].w // 2, 2)
                    
                    # Draw pickup name above pickup
                    if pickup.get("is_weapon_drop", False):
                        # Weapon pickup - use weapon name
                        weapon_type = pickup.get("type", "")
                        pickup_name = WEAPON_NAMES.get(weapon_type, weapon_type.upper())
                    else:
                        # Regular pickup - use type name
                        pickup_type = pickup.get("type", "")
                        pickup_name = pickup_type.upper().replace("_", " ")
                    
                    # Render pickup name text above the pickup
                    name_surf = small_font.render(pickup_name, True, (255, 255, 255))
                    name_rect = name_surf.get_rect(center=(pickup["rect"].centerx, pickup["rect"].y - 20))
                    # Draw text with black outline for visibility
                    outline_surf = small_font.render(pickup_name, True, (0, 0, 0))
                    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        screen.blit(outline_surf, (name_rect.x + dx, name_rect.y + dy))
                    screen.blit(name_surf, name_rect)
                
                # Draw enemy projectiles
                for proj in game_state.enemy_projectiles:
                    draw_projectile(screen, proj["rect"], proj["color"], proj.get("shape", "circle"))
                
                # Draw player bullets
                for bullet in game_state.player_bullets:
                    draw_projectile(screen, bullet["rect"], bullet["color"], bullet.get("shape", "circle"))
                
                # Draw friendly projectiles
                for proj in game_state.friendly_projectiles:
                    draw_projectile(screen, proj["rect"], proj["color"], proj.get("shape", "circle"))
                
                # Draw friendly AI (only dropped allies from Q key, not regular spawns)
                for friendly in game_state.friendly_ai:
                    pygame.draw.rect(screen, friendly.get("color", (100, 200, 100)), friendly["rect"])
                    if friendly.get("hp", 0) > 0 and ui_show_health_bars:
                        draw_health_bar(screen, friendly["rect"].x, friendly["rect"].y - 10, friendly["rect"].w, 5, friendly["hp"], friendly.get("max_hp", friendly["hp"]))
                
                # Draw enemies
                for enemy in game_state.enemies:
                    enemy_color = enemy.get("color", (200, 50, 50))
                    pygame.draw.rect(screen, enemy_color, enemy["rect"])
                    if enemy.get("hp", 0) > 0 and ui_show_health_bars:
                        draw_health_bar(screen, enemy["rect"].x, enemy["rect"].y - 10, enemy["rect"].w, 5, enemy["hp"], enemy.get("max_hp", enemy["hp"]))
                
                # Draw grenade explosions
                for explosion in game_state.grenade_explosions:
                    alpha = int(255 * (explosion["timer"] / 0.3))
                    color = (255, 100, 0, alpha)
                    pygame.draw.circle(screen, (255, 100, 0), (explosion["x"], explosion["y"]), explosion["radius"], 3)
                    pygame.draw.circle(screen, (255, 200, 0), (explosion["x"], explosion["y"]), explosion["radius"] // 2)
                
                # Draw missiles
                for missile in game_state.missiles:
                    pygame.draw.rect(screen, (255, 200, 0), missile["rect"])
                    pygame.draw.rect(screen, (255, 100, 0), missile["rect"], 2)
                
                # Draw player (circle with border)
                player_color = (255, 255, 255)
                border_color = (200, 200, 200)
                if game_state.shield_active:
                    player_color = (255, 100, 100)  # Red when shield is active
                    border_color = (255, 150, 150)  # Lighter red border when shield active
                # Draw border circle (slightly larger)
                pygame.draw.circle(screen, border_color, player.center, player.w // 2 + 2, 2)
                # Draw player circle
                pygame.draw.circle(screen, player_color, player.center, player.w // 2)
                # Health bar and overshield bar moved to bottom of screen (drawn later in HUD section)
                
                # Draw laser beams
                for beam in game_state.laser_beams:
                    if "start" in beam and "end" in beam:
                        pygame.draw.line(screen, beam.get("color", (255, 50, 50)), beam["start"], beam["end"], beam.get("width", 5))
                
                # Draw wave beams
                for beam in game_state.wave_beams:
                    points = beam.get("points", [])
                    if len(points) >= 2:
                        pygame.draw.lines(screen, beam.get("color", (50, 255, 50)), False, points, beam.get("width", 10))
                
                # Draw HUD
                if ui_show_hud:
                    # Draw prominent score at center top with yellow text and black outline
                    score_text = f"Score: {game_state.score}"
                    score_surface = big_font.render(score_text, True, (255, 255, 0))  # Yellow text
                    # Create outline by rendering black text at offsets
                    outline_surface = big_font.render(score_text, True, (0, 0, 0))  # Black outline
                    score_x = WIDTH // 2 - score_surface.get_width() // 2
                    score_y = 10
                    # Draw outline (8 directions)
                    for dx, dy in [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]:
                        screen.blit(outline_surface, (score_x + dx, score_y + dy))
                    # Draw yellow text on top
                    screen.blit(score_surface, (score_x, score_y))
                    
                    y_pos = 10
                    if ui_show_metrics:
                        y_pos = render_hud_text(screen, font, f"HP: {game_state.player_hp}/{game_state.player_max_hp}", y_pos)
                        if game_state.overshield > 0:
                            y_pos = render_hud_text(screen, font, f"Overshield: {game_state.overshield}/{overshield_max}", y_pos)
                        y_pos = render_hud_text(screen, font, f"Wave: {game_state.wave_number} | Level: {game_state.current_level}", y_pos)
                        # Display time survived (format as MM:SS)
                        minutes = int(game_state.survival_time // 60)
                        seconds = int(game_state.survival_time % 60)
                        y_pos = render_hud_text(screen, font, f"Time: {minutes:02d}:{seconds:02d}", y_pos)
                        if state == STATE_PLAYING:
                            y_pos = render_hud_text(screen, font, f"Lives: {game_state.lives}", y_pos)
                        y_pos = render_hud_text(screen, font, f"Enemies: {len(game_state.enemies)}", y_pos)
                        y_pos = render_hud_text(screen, font, f"Weapon: {game_state.current_weapon_mode.upper()}", y_pos)
                        if game_state.shield_active:
                            y_pos = render_hud_text(screen, font, "SHIELD ACTIVU", y_pos, (255, 100, 100))
                        # Display random damage multiplier if not 1.0x
                        if game_state.random_damage_multiplier != 1.0:
                            multiplier_color = (255, 255, 0) if game_state.random_damage_multiplier > 1.0 else (255, 150, 150)
                            y_pos = render_hud_text(screen, font, f"DMG MULT: {game_state.random_damage_multiplier:.2f}x", y_pos, multiplier_color)
                        
                        # Draw health bar and overshield bar at bottom of screen (above controls)
                        health_bar_y = HEIGHT - 80
                        health_bar_height = 20
                        health_bar_width = 300
                        
                        # Draw overshield bar (above health bar, only if active)
                        if game_state.overshield > 0:
                            overshield_bar_y = health_bar_y - 25
                            overshield_bar_height = 15
                            overshield_fill = int((game_state.overshield / overshield_max) * health_bar_width)
                            pygame.draw.rect(screen, (60, 60, 60), (10, overshield_bar_y, health_bar_width, overshield_bar_height))
                            pygame.draw.rect(screen, (255, 150, 0), (10, overshield_bar_y, overshield_fill, overshield_bar_height))
                            pygame.draw.rect(screen, (20, 20, 20), (10, overshield_bar_y, health_bar_width, overshield_bar_height), 2)
                            overshield_text = small_font.render(f"Armor: {int(game_state.overshield)}/{int(overshield_max)}", True, (255, 255, 255))
                            screen.blit(overshield_text, (15, overshield_bar_y + 2))
                        
                        # Draw health bar
                        health_fill = int((game_state.player_hp / game_state.player_max_hp) * health_bar_width)
                        pygame.draw.rect(screen, (60, 60, 60), (10, health_bar_y, health_bar_width, health_bar_height))
                        pygame.draw.rect(screen, (100, 255, 100), (10, health_bar_y, health_fill, health_bar_height))
                        pygame.draw.rect(screen, (20, 20, 20), (10, health_bar_y, health_bar_width, health_bar_height), 2)
                        health_text = small_font.render(f"HP: {int(game_state.player_hp)}/{int(game_state.player_max_hp)}", True, (255, 255, 255))
                        screen.blit(health_text, (15, health_bar_y + 2))
                        
                        # Draw cooldown bars at bottom
                        bar_y = HEIGHT - 30
                        bar_height = 20
                        bar_width = 200
                        
                        # Bomb (grenade) cooldown - red when not ready, purple when ready
                        grenade_progress = min(1.0, game_state.grenade_time_since_used / grenade_cooldown)
                        grenade_x = 10
                        pygame.draw.rect(screen, (60, 60, 60), (grenade_x, bar_y, bar_width, bar_height))
                        pygame.draw.rect(screen, (200, 100, 255) if grenade_progress >= 1.0 else (255, 50, 50), 
                                        (grenade_x, bar_y, int(bar_width * grenade_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (grenade_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("BOMB (E)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (grenade_x + 5, bar_y + 2))
                        
                        # Missile cooldown
                        missile_progress = min(1.0, game_state.missile_time_since_used / missile_cooldown)
                        missile_x = grenade_x + bar_width + 10
                        pygame.draw.rect(screen, (60, 60, 60), (missile_x, bar_y, bar_width, bar_height))
                        pygame.draw.rect(screen, (255, 200, 0) if missile_progress >= 1.0 else (100, 100, 100), 
                                        (missile_x, bar_y, int(bar_width * missile_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (missile_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("MISSILE (R)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (missile_x + 5, bar_y + 2))
                        
                        # Ally drop cooldown
                        ally_progress = min(1.0, game_state.ally_drop_timer / ally_drop_cooldown)
                        ally_x = missile_x + bar_width + 10
                        pygame.draw.rect(screen, (60, 60, 60), (ally_x, bar_y, bar_width, bar_height))
                        pygame.draw.rect(screen, (200, 100, 255) if ally_progress >= 1.0 else (100, 100, 100), 
                                        (ally_x, bar_y, int(bar_width * ally_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (ally_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("ALLY DROP (Q)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (ally_x + 5, bar_y + 2))
                        
                        # Overshield cooldown
                        overshield_progress = min(1.0, game_state.overshield_recharge_timer / overshield_recharge_cooldown)
                        overshield_x = ally_x + bar_width + 10
                        pygame.draw.rect(screen, (60, 60, 60), (overshield_x, bar_y, bar_width, bar_height))
                        pygame.draw.rect(screen, (255, 150, 0) if overshield_progress >= 1.0 else (100, 100, 100), 
                                        (overshield_x, bar_y, int(bar_width * overshield_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (overshield_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("OVERSHIELD (TAB)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (overshield_x + 5, bar_y + 2))
                        
                        # Shield recharge cooldown
                        # Calculate progress: if shield is active, show duration remaining; if on cooldown, show recharge progress
                        if game_state.shield_active:
                            # Shield is active - show duration remaining (inverse progress)
                            shield_progress = min(1.0, game_state.shield_duration_remaining / shield_duration)
                            shield_ready = False
                        else:
                            # Shield is on cooldown - show recharge progress
                            if game_state.shield_recharge_cooldown > 0:
                                shield_progress = min(1.0, game_state.shield_recharge_timer / game_state.shield_recharge_cooldown)
                            else:
                                shield_progress = 1.0  # Ready if no cooldown set
                            shield_ready = shield_progress >= 1.0
                        
                        shield_x = overshield_x + bar_width + 10
                        pygame.draw.rect(screen, (60, 60, 60), (shield_x, bar_y, bar_width, bar_height))
                        # Blue/cyan when ready, red when not ready, yellow when active
                        if game_state.shield_active:
                            shield_color = (255, 255, 100)  # Yellow when active
                        elif shield_ready:
                            shield_color = (100, 200, 255)  # Blue/cyan when ready
                        else:
                            shield_color = (255, 50, 50)  # Red when recharging
                        pygame.draw.rect(screen, shield_color, 
                                        (shield_x, bar_y, int(bar_width * shield_progress), bar_height))
                        pygame.draw.rect(screen, (255, 255, 255), (shield_x, bar_y, bar_width, bar_height), 2)
                        small_font_surf = small_font.render("SHIELD (LALT)", True, (255, 255, 255))
                        screen.blit(small_font_surf, (shield_x + 5, bar_y + 2))
                        
                        # Draw controls at bottom of screen
                        controls_y = HEIGHT - 10
                        controls_text = ""
                        if aiming_mode == AIM_ARROWS:
                            controls_text = "WASD: Move | Arrow Keys: Aim & Shoot | E: Bomb | R: Missile | Q: Ally Drop | TAB: Overshield | LALT: Shield | SPACE: Dash"
                        else:
                            controls_text = "WASD: Move | Mouse + Click: Aim & Shoot | E: Bomb | R: Missile | Q: Ally Drop | TAB: Overshield | LALT: Shield | SPACE: Dash"
                        controls_surf = small_font.render(controls_text, True, (150, 150, 150))
                        controls_rect = controls_surf.get_rect(center=(WIDTH // 2, controls_y))
                        screen.blit(controls_surf, controls_rect)
                
                # Draw damage numbers (fade out over 2 seconds)
                # Note: Timers are decremented in the update loop above
                for dmg_num in game_state.damage_numbers[:]:
                    if dmg_num["timer"] > 0:
                        alpha = int(255 * (dmg_num["timer"] / 2.0))  # Fade over 2 seconds
                        color = (*dmg_num["color"][:3], alpha) if len(dmg_num["color"]) > 3 else dmg_num["color"]
                        # Handle both "damage" (numeric) and "value" (text) keys
                        if "value" in dmg_num:
                            text = dmg_num["value"]
                            # Use bigger font for text messages like "PERFECT WAVE!"
                            text_surf = font.render(text, True, color[:3])
                        else:
                            text = str(int(dmg_num.get("damage", 0)))  # Ensure integer display
                            text_surf = small_font.render(text, True, color[:3])
                        screen.blit(text_surf, (dmg_num["x"], dmg_num["y"]))
                    else:
                        game_state.damage_numbers.remove(dmg_num)
                
                # Draw enemy defeat messages in bottom right corner
                defeat_y_start = HEIGHT - 100  # Start from bottom, work upwards
                for i, msg in enumerate(game_state.enemy_defeat_messages[-5:]):  # Show last 5 messages
                    if msg["timer"] > 0:
                        enemy_type = msg.get("enemy_type", "enemy")
                        alpha = int(255 * (msg["timer"] / 3.0))  # Fade over 3 seconds
                        color = (255, 200, 100, alpha)  # Orange color with alpha
                        text = f"{enemy_type.upper()} DEFEATED!"
                        text_surf = small_font.render(text, True, color[:3])
                        text_rect = text_surf.get_rect()
                        # Position in bottom right corner, stacked upwards
                        x_pos = WIDTH - text_rect.width - 20
                        y_pos = defeat_y_start - (i * 25)  # Stack messages with 25px spacing
                        screen.blit(text_surf, (x_pos, y_pos))
                
                # Draw weapon pickup messages
                # Note: Timers are decremented in the update loop above
                for msg in game_state.weapon_pickup_messages[:]:
                    if msg["timer"] > 0:
                        alpha = int(255 * (msg["timer"] / 3.0))
                        color = (*msg["color"][:3], alpha) if len(msg["color"]) > 3 else msg["color"]
                        text_surf = font.render(f"PICKED UP: {msg['weapon_name']}", True, color[:3])
                        text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(text_surf, text_rect)
                    else:
                        game_state.weapon_pickup_messages.remove(msg)
                
                # Draw wave countdown (3, 2, 1) when wave is complete and next wave is starting
                if game_state.wave_active and len(game_state.enemies) == 0 and game_state.time_to_next_wave < 3.0:
                    # Calculate countdown number (3, 2, or 1)
                    # time_to_next_wave goes from 0.0 to 3.0
                    # At 0.0-0.99: show 3
                    # At 1.0-1.99: show 2
                    # At 2.0-2.99: show 1
                    countdown_number = 3 - int(game_state.time_to_next_wave)
                    countdown_number = max(1, min(3, countdown_number))  # Clamp between 1 and 3
                    
                    # Display countdown text
                    next_wave_num = game_state.wave_number + 1
                    countdown_text = f"WAVE {next_wave_num} STARTING IN {countdown_number}"
                    draw_centered_text(screen, font, big_font, WIDTH, countdown_text, HEIGHT // 2, (255, 255, 0), use_big=True)
            elif state == STATE_PAUSED:
                # Draw paused game with overlay
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                
                draw_centered_text(screen, font, big_font, WIDTH, "PAUSED", HEIGHT // 2 - 100, use_big=True)
                
                y_offset = HEIGHT // 2
                for i, option in enumerate(pause_options):
                    color = (255, 255, 0) if i == pause_selected else (200, 200, 200)
                    draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == pause_selected else '  '} {option}", y_offset + i * 50, color)
                
                draw_centered_text(screen, font, big_font, WIDTH, "Press ENTER to select, ESC to unpause", HEIGHT - 100, (150, 150, 150))
            elif state == STATE_GAME_OVER:
                # Game over screen
                # (Game over rendering would go here)
                pass
            elif state == STATE_VICTORY:
                # Victory screen
                # (Victory rendering would go here)
                pass
            elif state == STATE_HIGH_SCORES:
                # High scores screen
                screen.fill((20, 20, 40))
                title = big_font.render("HIGH SCORES", True, (255, 255, 255))
                screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
                
                scores = get_high_scores(10)
                y_offset = 150
                if scores:
                    # Header
                    header = font.render("Rank  Name          Score    Waves  Time    Kills   Difficulty", True, (200, 200, 200))
                    screen.blit(header, (WIDTH // 2 - header.get_width() // 2, y_offset))
                    y_offset += 40
                    
                    for i, score_data in enumerate(scores, 1):
                        name = score_data["name"][:12]  # Limit name length
                        score_val = score_data["score"]
                        waves = score_data["waves"]
                        time_val = score_data["time"]
                        minutes = int(time_val // 60)
                        seconds = int(time_val % 60)
                        kills = score_data["kills"]
                        diff = score_data["difficulty"]
                        
                        rank_color = (255, 215, 0) if i == 1 else (255, 255, 255) if i <= 3 else (200, 200, 200)
                        text = font.render(f"{i:2d}.  {name:12s}  {score_val:8d}  {waves:3d}  {minutes:02d}:{seconds:02d}  {kills:5d}  {diff:8s}", True, rank_color)
                        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
                        y_offset += 35
                else:
                    no_scores = font.render("No high scores yet!", True, (150, 150, 150))
                    screen.blit(no_scores, (WIDTH // 2 - no_scores.get_width() // 2, y_offset))
                
                # Instructions
                instruction = small_font.render("Press ESC to exit", True, (100, 100, 100))
                screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 50))
            elif state == STATE_NAME_INPUT:
                # Name input screen
                screen.fill((20, 20, 40))
                title = big_font.render("ENTER YOUR NAME", True, (255, 255, 255))
                screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
                
                # Display current input with cursor
                display_text = game_state.player_name_input + ("_" if int(game_state.run_time * 2) % 2 == 0 else " ")
                input_surface = font.render(display_text, True, (255, 255, 255))
                screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT // 2))
                
                # Display score
                score_text = font.render(f"Score: {game_state.final_score_for_high_score}", True, (200, 200, 200))
                screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
                
                # Instructions
                instruction1 = small_font.render("Type your name and press ENTER to save", True, (150, 150, 150))
                instruction2 = small_font.render("Press ESC to skip", True, (150, 150, 150))
                screen.blit(instruction1, (WIDTH // 2 - instruction1.get_width() // 2, HEIGHT // 2 + 100))
                screen.blit(instruction2, (WIDTH // 2 - instruction2.get_width() // 2, HEIGHT // 2 + 125))
            elif state == STATE_CONTROLS:
                # Controls menu
                # (Controls menu rendering would go here)
                pass
            
            pygame.display.flip()

            # Write flow state back to GameState after this iteration
            game_state.current_screen = state
            game_state.previous_screen = previous_game_state
            game_state.menu_section = menu_section
            game_state.pause_selected = pause_selected
            game_state.continue_blink_t = continue_blink_t
            game_state.controls_selected = controls_selected
            game_state.controls_rebinding = controls_rebinding

    except KeyboardInterrupt:
        print("Interrupted by user (Ctrl+C). Saving run...")
    
    except Exception as e:
        print("Unhandled exception:", repr(e))
        raise
    
    finally:
        run_ended_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if telemetry_enabled and telemetry:
            telemetry.end_run(
                ended_at_iso=run_ended_at,
                seconds_survived=game_state.run_time,
                player_hp_end=game_state.player_hp,
                shots_fired=game_state.shots_fired,
                hits=game_state.hits,
                damage_taken=game_state.damage_taken,
                damage_dealt=game_state.damage_dealt,
                enemies_spawned=game_state.enemies_spawned,
                enemies_killed=game_state.enemies_killed,
                deaths=game_state.deaths,
                max_wave=game_state.wave_number,
            )
            telemetry.close()
            print(f"Saved run_id={game_state.run_id} to game_telemetry.db")
        pygame.quit()


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


# Controls will be initialized in main() after pygame.init()
# Using a placeholder dict to avoid calling pygame.key.key_code() before pygame.init()
controls = {}

# ----------------------------
# Telemetry
# ----------------------------
# Telemetry can be disabled to improve performance
telemetry_enabled = False  # Default: Disabled (will be set by user in menu)
telemetry = None  # Will be initialized if enabled
run_started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

# Game state constants are now imported from constants.py

state = STATE_MENU
previous_game_state = None  # Track previous game state for pause/unpause (STATE_PLAYING or STATE_ENDURANCE)
menu_section = 0  # 0 = difficulty, 1 = aiming, 1.5 = character profile yes/no, 2 = class, 3 = HUD options, 3.5 = Telemetry options, 4 = beam_selection, 5 = start
ui_show_metrics_selected = 0  # 0 = Show, 1 = Hide - Default: Show (enabled)
ui_show_hud = True  # HUD visibility (follows metrics setting)
ui_options_selected = 0  # 0 = Metrics, 1 = Telemetry (which option is currently focused)
endurance_mode_selected = 0  # 0 = Normal, 1 = Endurance Mode

# Character profile system
use_character_profile = False  # Whether to use character profiles
use_character_profile_selected = 0  # 0 = No, 1 = Yes
character_profile_selected = 0  # 0 = Premade, 1 = Custom
# character_profile_options is now imported from constants.py
custom_profile_stat_selected = 0  # Which stat is being edited
custom_profile_stats = {
    "hp_mult": 1.0,
    "speed_mult": 1.0,
    "damage_mult": 1.0,
    "firerate_mult": 1.0,
}
# custom_profile_stats_list and custom_profile_stats_keys are now imported from constants.py

# Side quests and goal tracking
side_quests = {
    "no_hit_wave": {
        "name": "Perfect Wave",
        "description": "Complete wave without getting hit",
        "bonus_points": 10000,
        "active": False,
        "completed": False,
    }
}
wave_damage_taken = 0  # Track damage taken in current wave
# Beam selection for testing (harder to access - requires testing mode)
testing_mode = True  # Set to True to enable weapon selection menu and testing options
invulnerability_mode = False  # Set to True to make player invulnerable (testing mode only)
beam_selection_selected = 6  # 0 = wave_beam, 1 = rocket, etc., 6 = basic (default)
beam_selection_pattern = "basic"  # Default weapon pattern

# Level system - 3 levels, each with 3 waves (boss on wave 3)
current_level = 1
max_level = 3
wave_in_level = 1  # Track which wave within current level (1, 2, or 3)
# level_themes is now imported from constants.py

# Difficulty settings (constants imported from constants.py)
difficulty = DIFFICULTY_NORMAL
difficulty_selected = 1  # 0 = Easy, 1 = Normal, 2 = Hard

# Aiming mode selection (constants imported from constants.py)
aiming_mode = AIM_MOUSE
aiming_mode_selected = 0  # 0 = Mouse, 1 = Arrows

# Player classes (constants imported from constants.py)
player_class = PLAYER_CLASS_BALANCED
player_class_selected = 0  # 0 = Balanced, 1 = Tank, 2 = Speedster, 3 = Sniper

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
ui_show_metrics = True  # Show metrics/stats in HUD - Default: Enabled
ui_telemetry_enabled_selected = 1  # 0 = Enabled, 1 = Disabled (for menu) - Default: Disabled

# Alternative aiming mechanics
aiming_mechanic = "mouse"  # "mouse", "lockon", "predictive", "directional", "hybrid"

# difficulty_multipliers and pause_options are now imported from constants.py
pause_selected = 0
continue_blink_t = 0.0

# Controls menu state (constants imported from constants.py)
controls_selected = 0
controls_rebinding = False

# ----------------------------
# Player (initialized in main() after WIDTH/HEIGHT are set)
# ----------------------------
player = None  # Will be initialized in main() after WIDTH/HEIGHT are set
player_speed = 450  # px/s (base speed, modified by class) - 1.5x (300 * 1.5)
player_max_hp = 7500  # base HP (modified by class) - 10x (750 * 10)
player_hp = player_max_hp

# player_class_stats and overshield_max are now imported from constants.py
overshield = 0  # Current overshield amount
# overshield_recharge_cooldown is now imported from constants.py
overshield_recharge_timer = 0.0  # Time since last overshield activation
# shield_recharge_cooldown is now imported from constants.py
shield_recharge_timer = 0.0  # Time since shield was used
# pygame.mouse.set_visible(True)  # Moved to main() after pygame.init()

# LIVES_START is now imported from constants.py
lives = LIVES_START

# Track most recent movement keys so latest press wins on conflicts
last_horizontal_key = None  # keycode of current "latest" horizontal key
last_vertical_key = None  # keycode of current "latest" vertical key
last_move_velocity = pygame.Vector2(0, 0)

# Dash mechanic (space bar) - constants imported from constants.py
jump_cooldown_timer = 0.0
jump_velocity = pygame.Vector2(0, 0)  # Current jump velocity
jump_timer = 0.0
is_jumping = False

# Boost / slow
previous_boost_state = False  # Track for telemetry
previous_slow_state = False  # Track for telemetry

# Boost/slow constants imported from constants.py
boost_meter = boost_meter_max

# Fire-rate pickup buff
fire_rate_buff_t = 0.0
fire_rate_buff_duration = 10.0
fire_rate_mult = 0.55  # reduces cooldown while active

# Shield system (Left Alt key) - constants imported from constants.py
shield_active = False
shield_duration_remaining = 0.0
shield_cooldown = 10.0  # Fixed 10 second cooldown
shield_cooldown_remaining = 0.0
shield_recharge_cooldown = shield_recharge_cooldown  # Imported from constants.py (default 10.0), will be set when shield is activated
shield_recharge_timer = 0.0

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

# Random damage multiplier (from "random_damage" pickup)
# This multiplies the base damage, and changes randomly when pickup is collected
random_damage_multiplier = 1.0  # Starts at 1.0x

# Damage number display system (floating damage numbers over enemies)
damage_numbers: list[dict] = []  # List of {x, y, damage, timer, color}
weapon_pickup_messages: list[dict] = []  # List of {weapon_name, timer, color} for displaying weapon pickup notifications

# Weapon mode system (keys 1-6 to switch)
# "basic" = normal bullets, "rocket" = rocket launcher, "triple" = triple shot,
# "bouncing" = bouncing bullets, "giant" = giant bullets, "laser" = laser beam
current_weapon_mode = "basic"
previous_weapon_mode = "basic"  # Track for telemetry
unlocked_weapons: set[str] = {"basic"}  # Weapons player has unlocked (starts with basic only)

# Laser beam system - constants imported from constants.py
laser_beams: list[dict] = []  # List of active laser beams
laser_time_since_shot = 999.0

# Wave beam system (trigonometric wave patterns) - constants imported from constants.py
wave_beams: list[dict] = []  # List of active wave beams
wave_beam_time_since_shot = 999.0
wave_beam_pattern_index = 0  # Current wave pattern (cycles through patterns)

# Rotating paraboloid/trapezoid hazard system
# On level 1: paraboloids, on level 2+: trapezoids
hazard_obstacles = [
    {
        "center": pygame.Vector2(250, 250),  # Top-left corner area
        "width": 250,  # Half size (250x250)
        "height": 250,
        "rotation_angle": 0.0,
        "rotation_speed": 0.9,  # 3x faster (0.3 * 3)
        "orbit_center": pygame.Vector2(250, 250),
        "orbit_radius": 100,
        "orbit_angle": 0.0,
        "orbit_speed": 0.6,  # 3x faster (0.2 * 3)
        "velocity": pygame.Vector2(150, 90),  # 3x faster (50*3, 30*3)
        "damage": 20,
        "color": (255, 100, 100),
        "points": [],
        "bounding_rect": pygame.Rect(0, 0, 250, 250),
        "shape": "paraboloid",  # Shape type
    },
    {
        "center": pygame.Vector2(WIDTH - 250, 250),  # Top-right corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 1.0,
        "rotation_speed": 0.75,  # 3x faster (0.25 * 3)
        "orbit_center": pygame.Vector2(WIDTH - 250, 250),
        "orbit_radius": 100,
        "orbit_angle": 1.5,
        "orbit_speed": 0.45,  # 3x faster (0.15 * 3)
        "velocity": pygame.Vector2(-120, 150),  # 3x faster (-40*3, 50*3)
        "damage": 10,
        "color": (255, 150, 100),
        "points": [],
        "bounding_rect": pygame.Rect(0, 0, 250, 250),
        "shape": "paraboloid",
    },
    {
        "center": pygame.Vector2(250, HEIGHT - 250),  # Bottom-left corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 2.0,
        "rotation_speed": 1.05,  # 3x faster (0.35 * 3)
        "orbit_center": pygame.Vector2(250, HEIGHT - 250),
        "orbit_radius": 100,
        "orbit_angle": 3.0,
        "orbit_speed": 0.54,  # 3x faster (0.18 * 3)
        "velocity": pygame.Vector2(90, -135),  # 3x faster (30*3, -45*3)
        "damage": 10,
        "color": (255, 120, 120),
        "points": [],
        "bounding_rect": pygame.Rect(0, 0, 250, 250),
        "shape": "paraboloid",
    },
    {
        "center": pygame.Vector2(WIDTH - 250, HEIGHT - 250),  # Bottom-right corner area
        "width": 250,
        "height": 250,
        "rotation_angle": 1.5,
        "rotation_speed": 0.84,  # 3x faster (0.28 * 3)
        "orbit_center": pygame.Vector2(WIDTH - 250, HEIGHT - 250),
        "orbit_radius": 100,
        "orbit_angle": 2.5,
        "orbit_speed": 0.66,  # 3x faster (0.22 * 3)
        "velocity": pygame.Vector2(-105, -120),  # 3x faster (-35*3, -40*3)
        "damage": 10,
        "color": (255, 130, 110),
        "points": [],
        "bounding_rect": pygame.Rect(0, 0, 250, 250),
        "shape": "paraboloid",
    },
]

# ----------------------------
# World blocks
# ----------------------------
# Removed all moveable indestructible blocks - keeping only:
# - moveable_destructible_blocks (destructible, movable)
# - destructible_blocks (unmovable, destructible)
# - trapezoid_blocks (unmovable, indestructible) - new border layout
# - triangle_blocks (unmovable, indestructible) - decorative border elements

blocks = []  # Empty - no moveable indestructible blocks

# Destructible blocks: 50% destructible (with HP), 50% indestructible (no HP), all moveable
destructible_blocks = [
    # First 6 blocks: Destructible (with HP)
    {"rect": pygame.Rect(300, 200, 80, 80), "color": (150, 100, 200), "hp": 500, "max_hp": 500, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(450, 300, 60, 60), "color": (100, 200, 150), "hp": 400, "max_hp": 400, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(200, 500, 90, 50), "color": (200, 150, 100), "hp": 600, "max_hp": 600, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(750, 600, 70, 70), "color": (150, 150, 200), "hp": 450, "max_hp": 450, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(150, 700, 100, 40), "color": (200, 200, 100), "hp": 550, "max_hp": 550, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1100, 300, 90, 90), "color": (180, 120, 180), "hp": 550, "max_hp": 550, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    # Last 6 blocks: Indestructible (no HP)
    {"rect": pygame.Rect(1300, 500, 70, 70), "color": (120, 180, 120), "is_moveable": True},
    {"rect": pygame.Rect(1000, 800, 80, 60), "color": (200, 120, 100), "is_moveable": True},
    {"rect": pygame.Rect(400, 1000, 100, 50), "color": (150, 150, 220), "is_moveable": True},
    {"rect": pygame.Rect(800, 1200, 70, 70), "color": (220, 200, 120), "is_moveable": True},
    {"rect": pygame.Rect(1200, 1000, 90, 40), "color": (200, 150, 200), "is_moveable": True},
    {"rect": pygame.Rect(1400, 700, 60, 60), "color": (100, 200, 200), "is_moveable": True},
]

# Moveable destructible blocks: Reduced amount, bigger size
moveable_destructible_blocks = [
    # First 3 blocks: Destructible (with HP) - bigger and fewer
    {"rect": pygame.Rect(350, 400, 120, 120), "color": (200, 100, 100), "hp": 400, "max_hp": 400, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(850, 500, 120, 120), "color": (100, 200, 100), "hp": 350, "max_hp": 350, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(650, 700, 120, 120), "color": (200, 150, 100), "hp": 450, "max_hp": 450, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    # Last 3 blocks: Indestructible (no HP) - bigger and fewer
    {"rect": pygame.Rect(1050, 300, 120, 120), "color": (200, 120, 150), "is_moveable": True},
    {"rect": pygame.Rect(200, 600, 120, 120), "color": (150, 150, 200), "is_moveable": True},
    {"rect": pygame.Rect(500, 900, 120, 120), "color": (200, 100, 150), "is_moveable": True},
]

# Giant and super giant blocks (unmovable, indestructible)
giant_blocks: list[dict] = [
    # Giant blocks (200x200)
    {"rect": pygame.Rect(200, 200, 200, 200), "color": (80, 80, 120), "is_moveable": False, "size": "giant"},
    {"rect": pygame.Rect(1000, 400, 200, 200), "color": (80, 80, 120), "is_moveable": False, "size": "giant"},
    {"rect": pygame.Rect(600, 800, 200, 200), "color": (80, 80, 120), "is_moveable": False, "size": "giant"},
]

super_giant_blocks: list[dict] = [
    # Super giant blocks (300x300)
    {"rect": pygame.Rect(500, 300, 300, 300), "color": (60, 60, 100), "is_moveable": False, "size": "super_giant"},
    {"rect": pygame.Rect(1200, 700, 300, 300), "color": (60, 60, 100), "is_moveable": False, "size": "super_giant"},
]

# Border geometry: trapezoids and triangles (unmovable, indestructible)
# Layout: 3 trapezoids left (spaced), 2 trapezoids right (adjacent), 
#         5 trapezoids with 2 triangles each on top, line of triangles on bottom
trapezoid_blocks = []
triangle_blocks = []  # New: triangles for decorative border elements

# Calculate spacing for left side (3 trapezoids with gaps)
left_trap_height = HEIGHT // 4  # Each trapezoid takes 1/4 of screen height
left_gap = 50  # Gap between trapezoids
left_trap_width = 100  # Width of trapezoid hanging into screen

# Left side: 3 trapezoids with spaces
for i in range(3):
    y_start = i * (left_trap_height + left_gap)
    y_end = y_start + left_trap_height
    trap_rect = pygame.Rect(-60, y_start, left_trap_width + 60, y_end - y_start)
    trapezoid_blocks.append({
        "points": [(-60, y_start), (left_trap_width, y_start + 20), (left_trap_width, y_end - 20), (-60, y_end)],
        "bounding_rect": trap_rect,
        "rect": trap_rect,  # Add rect for pushing support
        "color": (140, 110, 170),
        "is_moveable": True,
        "side": "left"
    })

# Right side: 2 trapezoids with space between them and triangles for player access
right_trap_height = HEIGHT // 3  # Smaller trapezoids to create space
right_trap_width = 100
right_y1 = 0
gap_size = 150  # Space between trapezoids for player access
right_y2 = right_trap_height + gap_size  # Larger gap

trap_rect1 = pygame.Rect(WIDTH - right_trap_width, right_y1, right_trap_width + 60, right_trap_height)
trapezoid_blocks.append({
    "points": [(WIDTH - right_trap_width, right_y1 + 20), (WIDTH + 60, right_y1), (WIDTH + 60, right_y1 + right_trap_height), (WIDTH - right_trap_width, right_y1 + right_trap_height - 20)],
    "bounding_rect": trap_rect1,
    "rect": trap_rect1,  # Add rect for pushing support
    "color": (110, 130, 190),
    "is_moveable": True,
    "side": "right"
})

# Add triangles in the gap to allow player access to outer map area
gap_center_y = right_y1 + right_trap_height + gap_size // 2
triangle_size = 40
# Left triangle (pointing right, allows passage)
tri_rect_gap1 = pygame.Rect(WIDTH - right_trap_width - triangle_size, gap_center_y - triangle_size // 2, triangle_size, triangle_size)
triangle_blocks.append({
    "points": [(WIDTH - right_trap_width - triangle_size, gap_center_y), (WIDTH - right_trap_width, gap_center_y - triangle_size // 2), (WIDTH - right_trap_width, gap_center_y + triangle_size // 2)],
    "bounding_rect": tri_rect_gap1,
    "rect": tri_rect_gap1,
    "color": (120, 140, 200),
    "is_moveable": True,
    "side": "right"
})
# Right triangle (pointing left, decorative)
tri_rect_gap2 = pygame.Rect(WIDTH - triangle_size // 2, gap_center_y - triangle_size // 2, triangle_size, triangle_size)
triangle_blocks.append({
    "points": [(WIDTH, gap_center_y - triangle_size // 2), (WIDTH, gap_center_y + triangle_size // 2), (WIDTH - triangle_size // 2, gap_center_y)],
    "bounding_rect": tri_rect_gap2,
    "rect": tri_rect_gap2,
    "color": (120, 140, 200),
    "is_moveable": True,
    "side": "right"
})

# Bottom right trapezoid - extends to bottom of screen
bottom_right_trap_height = HEIGHT - right_y2  # Extend to bottom of screen
trap_rect2 = pygame.Rect(WIDTH - right_trap_width, right_y2, right_trap_width + 60, bottom_right_trap_height)
trapezoid_blocks.append({
    "points": [(WIDTH - right_trap_width, right_y2 + 20), (WIDTH + 60, right_y2), (WIDTH + 60, HEIGHT), (WIDTH - right_trap_width, HEIGHT - 20)],
    "bounding_rect": trap_rect2,
    "rect": trap_rect2,  # Add rect for pushing support
    "color": (110, 130, 190),
    "is_moveable": True,
    "side": "right"
})

# Top: 5 trapezoids with 2 triangles each on top
top_trap_width = WIDTH // 5.5
top_trap_height = 80
top_trap_spacing = (WIDTH - 5 * top_trap_width) / 6  # Even spacing

for i in range(5):
    x_start = top_trap_spacing + i * (top_trap_width + top_trap_spacing)
    x_end = x_start + top_trap_width
    
    # Trapezoid hanging down
    trap_rect = pygame.Rect(x_start, -60, x_end - x_start, top_trap_height + 60)
    trapezoid_blocks.append({
        "points": [(x_start, -60), (x_end, -60), (x_end - 20, top_trap_height), (x_start + 20, top_trap_height)],
        "bounding_rect": trap_rect,
        "rect": trap_rect,  # Add rect for pushing support
        "color": (100, 120, 180),
        "is_moveable": True,
        "side": "top"
    })
    
    # 2 triangles on top of each trapezoid
    triangle_center_x = (x_start + x_end) // 2
    triangle_size = 30
    
    # Triangle 1 (left)
    tri_rect1 = pygame.Rect(triangle_center_x - triangle_size, -100, triangle_size, 40)
    triangle_blocks.append({
        "points": [(triangle_center_x - triangle_size, -60), (triangle_center_x, -100), (triangle_center_x - triangle_size // 2, -60)],
        "bounding_rect": tri_rect1,
        "rect": tri_rect1,  # Add rect for pushing support
        "color": (120, 140, 200),
        "is_moveable": True,
        "side": "top"
    })
    
    # Triangle 2 (right)
    tri_rect2 = pygame.Rect(triangle_center_x, -100, triangle_size, 40)
    triangle_blocks.append({
        "points": [(triangle_center_x + triangle_size // 2, -60), (triangle_center_x, -100), (triangle_center_x + triangle_size, -60)],
        "bounding_rect": tri_rect2,
        "rect": tri_rect2,  # Add rect for pushing support
        "color": (120, 140, 200),
        "is_moveable": True,
        "side": "top"
    })

# Bottom: Line of triangles across the bottom
bottom_triangle_count = 10
bottom_triangle_width = WIDTH // bottom_triangle_count
bottom_triangle_height = 40

for i in range(bottom_triangle_count):
    x_center = i * bottom_triangle_width + bottom_triangle_width // 2
    tri_rect = pygame.Rect(x_center - bottom_triangle_width // 2, HEIGHT, bottom_triangle_width, bottom_triangle_height)
    triangle_blocks.append({
        "points": [(x_center - bottom_triangle_width // 2, HEIGHT), (x_center, HEIGHT + bottom_triangle_height), (x_center + bottom_triangle_width // 2, HEIGHT)],
        "bounding_rect": tri_rect,
        "rect": tri_rect,  # Add rect for pushing support
        "color": (120, 100, 160),
        "is_moveable": True,
        "side": "bottom"
    })

# Add more blocks: 50% destructible, 50% indestructible, all moveable
destructible_blocks.extend([
    # First 6 blocks: Indestructible (no HP)
    {"rect": pygame.Rect(240, 360, 70, 70), "color": (160, 110, 210), "is_moveable": True},
    {"rect": pygame.Rect(400, 520, 60, 60), "color": (110, 210, 160), "is_moveable": True},
    {"rect": pygame.Rect(560, 680, 80, 50), "color": (210, 160, 110), "is_moveable": True},
    {"rect": pygame.Rect(720, 840, 70, 70), "color": (160, 160, 210), "is_moveable": True},
    {"rect": pygame.Rect(880, 1000, 60, 60), "color": (210, 210, 110), "is_moveable": True},
    {"rect": pygame.Rect(1040, 1160, 80, 50), "color": (190, 130, 190), "is_moveable": True},
    # Last 6 blocks: Destructible (with HP)
    {"rect": pygame.Rect(1200, 1320, 70, 70), "color": (130, 190, 130), "hp": 450, "max_hp": 450, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1360, 1160, 60, 60), "color": (210, 130, 110), "hp": 500, "max_hp": 500, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1520, 1000, 80, 50), "color": (160, 160, 230), "hp": 600, "max_hp": 600, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1680, 840, 70, 70), "color": (230, 210, 130), "hp": 450, "max_hp": 450, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(1840, 680, 60, 60), "color": (200, 160, 210), "hp": 550, "max_hp": 550, "is_destructible": True, "is_moveable": True, "crack_level": 0},
    {"rect": pygame.Rect(200, 840, 80, 50), "color": (110, 210, 210), "hp": 400, "max_hp": 400, "is_destructible": True, "is_moveable": True, "crack_level": 0},
])

# Single moving health recovery zone
moving_health_zone = {
    "rect": pygame.Rect(WIDTH // 4 - 75, HEIGHT // 4 - 75, 150, 150),  # Offset from center (boss spawn)
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
# Player bullets - constants imported from constants.py
# ----------------------------
player_bullets: list[dict] = []
player_time_since_shot = 999.0
player_bullet_shape_index = 0

# Grenade system - constants imported from constants.py
grenade_explosions: list[dict] = []  # List of active explosions {x, y, radius, max_radius, timer, damage}
grenade_time_since_used = 999.0  # Time since last grenade

# Missile system (seeking missiles) - constants imported from constants.py
missiles: list[dict] = []  # List of active missiles {rect, vel, target_enemy, speed, damage, explosion_radius}
missile_time_since_used = 999.0  # Time since last missile
missile_explosion_radius = 100  # Explosion radius
missile_speed = 400  # Missile movement speed

# Filter blocks to prevent them from spawning within 10x player size radius from player
# This must be done after all blocks are defined
# NOTE: This code runs at module level but player is None until main() is called
# The actual filtering will happen in main() after player is initialized
# player_center = pygame.Vector2(player.center)  # Moved to main()
# player_size = max(player.w, player.h)  # Use larger dimension (28)
# min_block_distance = player_size * 10  # 10x player size = 280 pixels

# Filter all block lists to remove blocks too close to player and prevent overlaps with each other
def filter_blocks_no_overlap(block_list: list[dict], all_other_blocks: list[list[dict]], player_rect: pygame.Rect) -> list[dict]:
    """Filter blocks to remove those too close to player and overlapping with other blocks."""
    filtered = []
    player_center = pygame.Vector2(player_rect.center)
    player_size = max(player_rect.w, player_rect.h)  # Use larger dimension (28)
    min_block_distance = player_size * 10  # 10x player size = 280 pixels
    
    for block in block_list:
        block_rect = block["rect"]
        block_center = pygame.Vector2(block_rect.center)
        
        # Check distance from player
        if block_center.distance_to(player_center) < min_block_distance:
            continue
        
        # Check collision with player
        if block_rect.colliderect(player_rect):
            continue
        
        # Check collision with other blocks
        overlaps = False
        for other_block_list in all_other_blocks:
            for other_block in other_block_list:
                if block_rect.colliderect(other_block["rect"]):
                    overlaps = True
                    break
            if overlaps:
                break
        
        # Check collision with other blocks in same list (prevent self-overlap)
        if not overlaps:
            for other_block in block_list:
                if other_block is not block and block_rect.colliderect(other_block["rect"]):
                    overlaps = True
                    break
        
        if not overlaps:
            filtered.append(block)
    
    return filtered

# Filter blocks to prevent overlaps (allies checked at runtime in random_spawn_position)
# Note: trapezoid_blocks and triangle_blocks are border elements and don't need overlap filtering
# NOTE: This filtering will be done in main() after player is initialized
# destructible_blocks = filter_blocks_no_overlap(...)  # Moved to main()
# moveable_destructible_blocks = filter_blocks_no_overlap(...)  # Moved to main()
# giant_blocks = filter_blocks_no_overlap(...)  # Moved to main()
# super_giant_blocks = filter_blocks_no_overlap(...)  # Moved to main()

# Ensure health zone doesn't overlap with blocks
health_zone_overlaps = True
max_health_zone_attempts = 100
for _ in range(max_health_zone_attempts):
    health_zone_overlaps = False
    # Check if health zone overlaps with any blocks
    for block_list in [destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks]:
        for block in block_list:
            if moving_health_zone["rect"].colliderect(block["rect"]):
                health_zone_overlaps = True
                break
        if health_zone_overlaps:
            break
    # Also check trapezoid and triangle blocks
    if not health_zone_overlaps:
        for tb in trapezoid_blocks:
            if moving_health_zone["rect"].colliderect(tb.get("bounding_rect", tb.get("rect"))):
                health_zone_overlaps = True
                break
    if not health_zone_overlaps:
        for tr in triangle_blocks:
            if moving_health_zone["rect"].colliderect(tr.get("bounding_rect", tr.get("rect"))):
                health_zone_overlaps = True
                break
    
    if not health_zone_overlaps:
        break  # Found a good position
    
    # Try a new random position for health zone
    new_x = random.randint(100, WIDTH - 250)
    new_y = random.randint(100, HEIGHT - 250)
    moving_health_zone["rect"].center = (new_x, new_y)

# ----------------------------
# Enemy templates are now imported from config_enemies.py
# ----------------------------
enemy_templates = ENEMY_TEMPLATES  # Alias for compatibility

# Boss enemy template is now imported from config_enemies.py
# Note: rect position will be set at runtime in spawn_boss()
# boss_template will be created from BOSS_TEMPLATE.copy() when needed in start_wave()
# We keep a reference here for compatibility, but it will be copied at runtime
boss_template = BOSS_TEMPLATE  # Reference (will be copied when spawning boss)


def clone_enemies_from_templates() -> list[dict]:
    # Kept for compatibility but waves use start_wave() instead.
    return [make_enemy_from_template(t, 1.0, 1.0) for t in enemy_templates]


enemies: list[dict] = []

# ----------------------------
# Friendly AI
# ----------------------------
# Friendly AI templates are now imported from config_enemies.py
friendly_ai_templates = FRIENDLY_AI_TEMPLATES  # Alias for compatibility

friendly_ai: list[dict] = []

# Dropped ally system (distracts enemies)
dropped_ally: dict | None = None  # Single dropped ally that distracts enemies
ally_drop_cooldown = 5.0  # Cooldown between ally drops (seconds)
ally_drop_timer = 0.0  # Time since last ally drop
friendly_projectiles: list[dict] = []

# ----------------------------
# Enemy projectiles
# ----------------------------
enemy_projectiles: list[dict] = []
# Enemy projectile constants are now imported from constants.py
enemy_projectile_size = ENEMY_PROJECTILE_SIZE
enemy_projectile_damage = ENEMY_PROJECTILE_DAMAGE
enemy_projectiles_color = ENEMY_PROJECTILES_COLOR
enemy_projectile_shapes = ["circle", "square", "diamond"]

# ----------------------------
# Run counters (runs table) - initialized in main()
# ----------------------------
running = True  # Will be set in main()
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

# High score system - HIGH_SCORES_DB imported from constants.py
player_name_input = ""  # Current name being typed
name_input_active = False  # Whether we're in name input mode
final_score_for_high_score = 0  # Score to save when name is entered

# POS_SAMPLE_INTERVAL imported from constants.py
pos_timer = 0.0

# Waves / progression
wave_number = 1
wave_in_level = 1  # Wave within current level (1, 2, or 3)
wave_respawn_delay = 2.5  # seconds between waves
time_to_next_wave = 0.0
wave_active = True
# Enemy spawn constants are now imported from config_enemies.py
base_enemies_per_wave = BASE_ENEMIES_PER_WAVE
max_enemies_per_wave = MAX_ENEMIES_PER_WAVE
boss_active = False

# Pickups - PICKUP_SPAWN_INTERVAL imported from constants.py
pickups: list[dict] = []
pickup_spawn_timer = 0.0

# Scoring constants imported from constants.py
# Weapon key mapping imported from constants.py
# Removed: enemy_spawn_boost_level - enemies no longer collect pickups

# Weapon key mapping (uses pygame constants, so must stay here)
WEAPON_KEY_MAP = {
    pygame.K_1: "basic",
    pygame.K_2: "rocket",
    pygame.K_3: "triple",
    pygame.K_4: "bouncing",
    pygame.K_5: "giant",
    pygame.K_6: "laser",
    pygame.K_7: "wave_beam",  # Wave pattern beam weapon
}

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
    # Include all moveable blocks: destructible, moveable_destructible, trapezoid, and triangle blocks
    destructible_rects = [b["rect"] for b in destructible_blocks]
    moveable_destructible_rects = [b["rect"] for b in moveable_destructible_blocks]
    trapezoid_rects = [tb["rect"] for tb in trapezoid_blocks]  # Now use rect instead of bounding_rect
    triangle_rects = [tr["rect"] for tr in triangle_blocks]  # Now use rect instead of bounding_rect
    # Include giant and super giant blocks (unmovable) - player cannot pass through
    giant_block_rects = [gb["rect"] for gb in giant_blocks]
    super_giant_block_rects = [sgb["rect"] for sgb in super_giant_blocks]
    # Friendly AI rects removed - player can now fly through allies
    # friendly_ai_rects = [f["rect"] for f in friendly_ai if f.get("hp", 1) > 0]
    all_collision_rects = block_rects + destructible_rects + moveable_destructible_rects + trapezoid_rects + triangle_rects + giant_block_rects + super_giant_block_rects  # Removed friendly_ai_rects

    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        player_rect.x += axis_dx
        player_rect.y += axis_dy

        hit_block = None
        hit_is_unpushable = False
        # Check regular blocks first
        for b in block_list:
            if player_rect.colliderect(b["rect"]):
                hit_block = b
                break
        # Check destructible blocks (now moveable)
        if hit_block is None:
            for b in destructible_blocks:
                if player_rect.colliderect(b["rect"]):
                    hit_block = b
                    break
        # Check moveable destructible blocks
        if hit_block is None:
            for b in moveable_destructible_blocks:
                if player_rect.colliderect(b["rect"]):
                    hit_block = b
                    break
        # Check trapezoid blocks (now moveable) - use point-in-polygon for accurate collision
        if hit_block is None:
            for tb in trapezoid_blocks:
                # First check bounding rect for performance
                if player_rect.colliderect(tb.get("bounding_rect", tb.get("rect"))):
                    # Use point-in-polygon for accurate collision with trapezoid shape
                    player_center = pygame.Vector2(player_rect.center)
                    if "points" in tb and len(tb["points"]) >= 3:
                        # Convert points to Vector2 (points are stored as tuples (x, y))
                        trap_points = [pygame.Vector2(p[0], p[1]) if isinstance(p, (tuple, list)) and len(p) >= 2 else pygame.Vector2(p.x, p.y) if hasattr(p, 'x') else p for p in tb["points"]]
                        if check_point_in_hazard(player_center, trap_points, tb.get("bounding_rect", tb.get("rect"))):
                            hit_block = tb
                            break
                    else:
                        # Fallback to rect collision if no points
                        if player_rect.colliderect(tb["rect"]):
                            hit_block = tb
                            break
        # Check triangle blocks (now moveable)
        if hit_block is None:
            for tr in triangle_blocks:
                if player_rect.colliderect(tr["rect"]):
                    hit_block = tr
                    break
        # Check hazard obstacles (paraboloids/trapezoids) - player cannot pass through or push
        if hit_block is None:
            for hazard in hazard_obstacles:
                if hazard.get("points") and len(hazard["points"]) > 2:
                    # Use point-in-polygon check for accurate collision
                    player_center = pygame.Vector2(player_rect.center)
                    if check_point_in_hazard(player_center, hazard["points"], hazard["bounding_rect"]):
                        hit_block = hazard
                        hit_is_unpushable = True  # Hazards are unmovable
                        break
        # Check giant and super giant blocks (unmovable) - player cannot pass through or push
        if hit_block is None:
            for gb in giant_blocks:
                if player_rect.colliderect(gb["rect"]):
                    hit_block = gb
                    hit_is_unpushable = True  # Can't push giant blocks
                    break
        if hit_block is None:
            for sgb in super_giant_blocks:
                if player_rect.colliderect(sgb["rect"]):
                    hit_block = sgb
                    hit_is_unpushable = True  # Can't push super giant blocks
                    break
        # Friendly AI (allies) - player can now fly through allies (collision removed)
        # if hit_block is None:
        #     for f in friendly_ai:
        #         if f.get("hp", 1) > 0 and player_rect.colliderect(f["rect"]):
        #             hit_block = f
        #             hit_is_unpushable = True  # Can't push allies
        #             break

        if hit_block is None:
            continue

        # Hazards and allies are unmovable, so just block player movement
        if hit_is_unpushable:
            player_rect.x -= axis_dx
            player_rect.y -= axis_dy
            continue

        hit_rect = hit_block["rect"]
        other_rects = [r for r in all_collision_rects if r is not hit_rect]

        if can_move_rect(hit_rect, axis_dx, axis_dy, other_rects):
            hit_rect.x += axis_dx
            hit_rect.y += axis_dy
            # Update bounding_rect for trapezoid/triangle blocks to match rect position
            if "bounding_rect" in hit_block:
                hit_block["bounding_rect"].x = hit_rect.x
                hit_block["bounding_rect"].y = hit_rect.y
        else:
            player_rect.x -= axis_dx
            player_rect.y -= axis_dy

    clamp_rect_to_screen(player_rect)


def move_enemy_with_push(enemy_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict], state: GameState):
    """Enemy movement - enemies cannot go through objects and must navigate around them."""
    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        enemy_rect.x += axis_dx
        enemy_rect.y += axis_dy

        # Check collisions with all objects - enemies cannot pass through anything
        collision = False
        
        # Check regular blocks
        for b in block_list:
            if enemy_rect.colliderect(b["rect"]):
                collision = True
                break
        
        # Check destructible blocks
        if not collision:
            for b in destructible_blocks:
                if enemy_rect.colliderect(b["rect"]):
                    collision = True
                    break
        
        # Check moveable destructible blocks
        if not collision:
            for b in moveable_destructible_blocks:
                if enemy_rect.colliderect(b["rect"]):
                    collision = True
                    break
        
        # Check giant blocks (unmovable)
        if not collision:
            for gb in giant_blocks:
                if enemy_rect.colliderect(gb["rect"]):
                    collision = True
                    break
        
        # Check super giant blocks (unmovable)
        if not collision:
            for sgb in super_giant_blocks:
                if enemy_rect.colliderect(sgb["rect"]):
                    collision = True
                    break
        
        # Check trapezoid blocks
        if not collision:
            for tb in trapezoid_blocks:
                if enemy_rect.colliderect(tb.get("bounding_rect", tb.get("rect"))):
                    collision = True
                    break
        
        # Check triangle blocks
        if not collision:
            for tr in triangle_blocks:
                if enemy_rect.colliderect(tr.get("bounding_rect", tr.get("rect"))):
                    collision = True
                    break
        
        # Check pickups (enemies cannot collect pickups - only collision detection)
        if not collision:
            for pickup in state.pickups:
                if enemy_rect.colliderect(pickup["rect"]):
                    collision = True
                    break
        
        # Check health zone
        if not collision:
            if enemy_rect.colliderect(moving_health_zone["rect"]):
                collision = True
        
        # Check player
        if not collision and state.player_rect is not None:
            if enemy_rect.colliderect(state.player_rect):
                collision = True

        # Check friendly AI
        if not collision:
            for f in state.friendly_ai:
                if f.get("hp", 1) > 0 and enemy_rect.colliderect(f["rect"]):
                    collision = True
                    break
        
        # Check other enemies (prevent enemy stacking)
        if not collision:
            for other_e in state.enemies:
                if other_e["rect"] is not enemy_rect and enemy_rect.colliderect(other_e["rect"]):
                    collision = True
                    break

        # If collision detected, revert movement
        if collision:
            enemy_rect.x -= axis_dx
            enemy_rect.y -= axis_dy

    clamp_rect_to_screen(enemy_rect)


def rect_offscreen(r: pygame.Rect) -> bool:
    return r.right < 0 or r.left > WIDTH or r.bottom < 0 or r.top > HEIGHT


def filter_blocks_too_close_to_player(block_list: list[dict], player_center: pygame.Vector2, player_size: int) -> list[dict]:
    """Filter out blocks that are too close to the player (within 10x player size radius)."""
    min_distance = player_size * 10  # 10x player size radius
    filtered = []
    for block in block_list:
        block_center = pygame.Vector2(block["rect"].center)
        distance = block_center.distance_to(player_center)
        if distance >= min_distance:
            filtered.append(block)
    return filtered


def random_spawn_position(size: tuple[int, int], state: GameState, max_attempts: int = 25) -> pygame.Rect:
    """Find a spawn position not overlapping player or blocks. Player spawn takes priority."""
    w, h = size
    if state.player_rect is None:
        player_center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        player_size = 28
    else:
        player_center = pygame.Vector2(state.player_rect.center)
        player_size = max(state.player_rect.w, state.player_rect.h)  # Use larger dimension for player size
    min_distance = player_size * 10  # 10x player size radius

    for _ in range(max_attempts):
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        candidate = pygame.Rect(x, y, w, h)
        candidate_center = pygame.Vector2(candidate.center)

        # Check if too close to player (10x player size radius)
        if candidate_center.distance_to(player_center) < min_distance:
            continue

        # Player spawn takes priority - don't spawn blocks on player
        if state.player_rect is not None and candidate.colliderect(state.player_rect):
            continue
        if any(candidate.colliderect(b["rect"]) for b in blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in moveable_destructible_blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in destructible_blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in giant_blocks):
            continue
        if any(candidate.colliderect(b["rect"]) for b in super_giant_blocks):
            continue
        if any(candidate.colliderect(tb["bounding_rect"]) for tb in trapezoid_blocks):
            continue
        if any(candidate.colliderect(tr["bounding_rect"]) for tr in triangle_blocks):
            continue
        if any(candidate.colliderect(p["rect"]) for p in state.pickups):
            continue
        # Prevent spawning in health recovery zone
        if candidate.colliderect(moving_health_zone["rect"]):
            continue
        return candidate
    # fallback: top-left corner inside bounds
    return pygame.Rect(max(0, WIDTH // 2 - w), max(0, HEIGHT // 2 - h), w, h)


def start_wave(wave_num: int, state: GameState):
    """Spawn a new wave with scaling. Each level has 3 waves, boss on wave 3."""
    state.enemies = []
    state.boss_active = False
    # Reset wave damage tracking and activate side quest
    state.wave_damage_taken = 0
    state.side_quests["no_hit_wave"]["active"] = True
    state.side_quests["no_hit_wave"]["completed"] = False
    # Reset lives to 3 at the beginning of each wave (unless in endurance mode)
    # In endurance mode, lives is set to 999 and should not be reset
    if state.lives != 999:
        state.lives = 3  # Reset to 3 lives at the beginning of each wave
    
    # Calculate level and wave within level (1-based)
    state.current_level = min(state.max_level, (wave_num - 1) // 3 + 1)
    state.wave_in_level = ((wave_num - 1) % 3) + 1
    
    # Boss appears on wave 3 of each level
    if state.wave_in_level == 3:
        # Spawn boss (create a copy from template)
        boss = BOSS_TEMPLATE.copy()  # Create a copy to modify
        # Set rect position at runtime (WIDTH/HEIGHT are now available)
        boss["rect"] = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
        boss["rect"] = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
        diff_mult = difficulty_multipliers[difficulty]
        
        # Boss HP is capped at 300 (same as all enemies)
        # Scale boss HP for different levels, but cap at 300
        # Apply 110% multiplier (1.1x) to all boss stats
        boss_hp_scale = 1.0 + (state.current_level - 1) * 0.3
        boss["hp"] = min(int(boss["max_hp"] * boss_hp_scale * diff_mult["enemy_hp"] * 1.1), 300)  # 110% health
        boss["max_hp"] = boss["hp"]
        boss["shoot_cooldown"] = boss_template["shoot_cooldown"] / ENEMY_FIRE_RATE_MULTIPLIER  # Apply fire rate multiplier
        boss["speed"] = boss_template["speed"] * ENEMY_SPEED_SCALE_MULTIPLIER  # Apply speed multiplier
        
        boss["phase"] = 1
        boss["time_since_shot"] = 0.0
        state.enemies.append(boss)
        state.boss_active = True
        enemies_spawned_ref = [state.enemies_spawned]
        log_enemy_spawns([boss], telemetry, state.run_time, enemies_spawned_ref)
        state.enemies_spawned = enemies_spawned_ref[0]
        # Log boss as enemy type for this wave
        if telemetry_enabled and telemetry:
            telemetry.log_wave_enemy_types(
                WaveEnemyTypeEvent(
                    t=state.run_time,
                    wave_number=wave_num,
                    enemy_type=boss["type"],
                    count=1,
                )
            )
        state.wave_active = True
        
        # Charge overshield at wave start (boss wave)
        state.overshield_recharge_timer = overshield_recharge_cooldown  # Set to full charge
        
        return
    
    # Normal wave spawning (waves 1 and 2 of each level)
    # Apply difficulty multipliers
    diff_mult = difficulty_multipliers[difficulty]
    # Level-based scaling - increase difficulty with level and wave in level
    level_mult = 1.0 + (state.current_level - 1) * 0.3
    wave_in_level_mult = 1.0 + (state.wave_in_level - 1) * 0.15  # Wave 2 is harder than wave 1
    hp_scale = (1.0 + 0.15 * (wave_num - 1)) * diff_mult["enemy_hp"] * level_mult * wave_in_level_mult
    speed_scale = (1.0 + 0.05 * (wave_num - 1)) * diff_mult["enemy_speed"] * level_mult * wave_in_level_mult
    # Apply difficulty to enemy count
    base_count = base_enemies_per_wave + 2 * (wave_num - 1)  # Removed enemy_spawn_boost_level
    count = min(int(base_count * diff_mult["enemy_spawn"] * ENEMY_SPAWN_MULTIPLIER), max_enemies_per_wave)

    spawned: list[dict] = []
    # Track enemy types for this wave
    enemy_type_counts: dict[str, int] = {}
    queen_count = 0  # Track queen spawns (max 3 per wave)
    max_queens_per_wave = 3
    
    for _ in range(count):
        tmpl = random.choice(enemy_templates)
        # Limit queen spawns to max 3 per wave
        if tmpl.get("type") == "queen" and queen_count >= max_queens_per_wave:
            # Reselect a different enemy type if we've hit the queen limit
            non_queen_templates = [t for t in enemy_templates if t.get("type") != "queen"]
            if non_queen_templates:
                tmpl = random.choice(non_queen_templates)
            else:
                continue  # Skip if no other templates available
        
        enemy = make_enemy_from_template(tmpl, hp_scale, speed_scale)
        enemy["rect"] = random_spawn_position((enemy["rect"].w, enemy["rect"].h), state)
        spawned.append(enemy)
        # Count enemy types
        enemy_type = enemy["type"]
        enemy_type_counts[enemy_type] = enemy_type_counts.get(enemy_type, 0) + 1
        if enemy_type == "queen":
            queen_count += 1

    state.enemies.extend(spawned)
    enemies_spawned_ref = [state.enemies_spawned]
    if telemetry_enabled and telemetry:
        log_enemy_spawns(spawned, telemetry, state.run_time, enemies_spawned_ref)
    state.enemies_spawned = enemies_spawned_ref[0]
    
    # Log enemy types for this wave
    if telemetry_enabled and telemetry:
        for enemy_type, type_count in enemy_type_counts.items():
            telemetry.log_wave_enemy_types(
                WaveEnemyTypeEvent(
                    t=state.run_time,
                    wave_number=wave_num,
                    enemy_type=enemy_type,
                    count=type_count,
                )
            )
    
    # Spawn friendly AI: 2-4 per wave (increased from 1-2)
    # Calculate friendly AI count based on enemy count - more friendly AI
    # REMOVED: No longer spawn friendly AI at wave start - only dropped ally is used
    # friendly_count = max(2, min(4, (count + 1) // 2))  # 2-4 friendly per wave
    # spawn_friendly_ai(friendly_count, hp_scale, speed_scale, friendly_ai_templates, friendly_ai, random_spawn_position, telemetry, run_time)
    
    state.wave_active = True
    
    # Charge overshield at wave start
    state.overshield_recharge_timer = overshield_recharge_cooldown  # Set to full charge
    state.ally_drop_timer = ally_drop_cooldown  # Charge ally drop at wave start
    # Charge shield at wave start
    state.shield_recharge_timer = state.shield_recharge_cooldown  # Set to full charge
    state.shield_cooldown_remaining = 0.0  # Shield ready to use
    
    # Log wave start event
    if telemetry_enabled and telemetry:
        telemetry.log_wave(
            WaveEvent(
                t=state.run_time,
                wave_number=wave_num,
                event_type="start",
                enemies_spawned=count,
                hp_scale=hp_scale,
                speed_scale=speed_scale,
            )
        )


def init_high_scores_db():
    """Initialize the high scores database."""
    conn = sqlite3.connect(HIGH_SCORES_DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            waves_survived INTEGER NOT NULL,
            time_survived REAL NOT NULL,
            enemies_killed INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            date_achieved TEXT NOT NULL
        );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_score ON high_scores(score DESC);")
    conn.commit()
    conn.close()


def get_high_scores(limit: int = 10) -> list[dict]:
    """Get top high scores from database."""
    conn = sqlite3.connect(HIGH_SCORES_DB)
    cursor = conn.execute("""
        SELECT player_name, score, waves_survived, time_survived, enemies_killed, difficulty, date_achieved
        FROM high_scores
        ORDER BY score DESC
        LIMIT ?
    """, (limit,))
    scores = []
    for row in cursor.fetchall():
        scores.append({
            "name": row[0],
            "score": row[1],
            "waves": row[2],
            "time": row[3],
            "kills": row[4],
            "difficulty": row[5],
            "date": row[6]
        })
    conn.close()
    return scores


def save_high_score(name: str, score: int, waves: int, time_survived: float, enemies_killed: int, difficulty: str):
    """Save a high score to the database."""
    if not name or not name.strip():
        name = "Anonymous"
    conn = sqlite3.connect(HIGH_SCORES_DB)
    conn.execute("""
        INSERT INTO high_scores (player_name, score, waves_survived, time_survived, enemies_killed, difficulty, date_achieved)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name.strip()[:20], score, waves, time_survived, enemies_killed, difficulty, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()


def is_high_score(score: int) -> bool:
    """Check if a score qualifies for the high score board (top 10)."""
    scores = get_high_scores(10)
    if len(scores) < 10:
        return True
    return score > scores[-1]["score"]


def generate_wave_beam_points(start_pos: pygame.Vector2, direction: pygame.Vector2, pattern: str, length: int, amplitude: float = 50.0, frequency: float = 0.02, time_offset: float = 0.0) -> list[pygame.Vector2]:
    """Generate points along a wave pattern beam.
    
    Args:
        start_pos: Starting position of the beam
        direction: Normalized direction vector
        pattern: Wave pattern type ("sine", "cosine", "tangent", etc.)
        length: Length of the beam in pixels
        amplitude: Amplitude of the wave (pixels)
        frequency: Frequency of the wave (cycles per pixel)
        time_offset: Time-based phase offset for undulation (in seconds)
    
    Returns:
        List of points along the wave path
    """
    points = []
    perp = pygame.Vector2(-direction.y, direction.x)  # Perpendicular vector for wave offset
    
    num_points = max(200, length // 5)  # Generate more points for smoother solid line
    step = length / num_points
    
    # Undulation: 0.5 second period = 4 * pi radians per second (2 * pi / 0.5)
    undulation_phase = time_offset * 4 * math.pi  # Phase offset for 0.5 second period
    
    for i in range(num_points + 1):
        t = i * step
        x = start_pos.x + direction.x * t
        y = start_pos.y + direction.y * t
        
        # Calculate wave offset based on pattern with time-based undulation
        wave_value = 0.0
        angle = t * frequency * 2 * math.pi + undulation_phase
        
        if pattern == "sine":
            wave_value = math.sin(angle)
        elif pattern == "cosine":
            wave_value = math.cos(angle)
        elif pattern == "tangent":
            # Clamp to prevent infinite values
            wave_value = math.tan(angle)
            wave_value = max(-10.0, min(10.0, wave_value))
        elif pattern == "cotangent":
            # Clamp to prevent infinite values
            if abs(math.sin(angle)) > 0.01:
                wave_value = math.cos(angle) / math.sin(angle)
                wave_value = max(-10.0, min(10.0, wave_value))
            else:
                wave_value = 0.0
        elif pattern == "secant":
            # Clamp to prevent infinite values
            if abs(math.cos(angle)) > 0.01:
                wave_value = 1.0 / math.cos(angle)
                wave_value = max(-10.0, min(10.0, wave_value))
            else:
                wave_value = 0.0
        elif pattern == "cosecant":
            # Clamp to prevent infinite values
            if abs(math.sin(angle)) > 0.01:
                wave_value = 1.0 / math.sin(angle)
                wave_value = max(-10.0, min(10.0, wave_value))
            else:
                wave_value = 0.0
        
        # Apply wave offset perpendicular to direction
        offset = perp * (wave_value * amplitude)
        point = pygame.Vector2(x, y) + offset
        points.append(point)
    
    return points


def check_wave_beam_collision(points: list[pygame.Vector2], rect: pygame.Rect, width: int) -> tuple[pygame.Vector2 | None, float]:
    """Check if a wave beam (represented by points) collides with a rectangle.
    
    Returns:
        Tuple of (closest_hit_point, distance) or (None, infinity) if no collision
    """
    closest_hit = None
    closest_dist = float('inf')
    
    # Check each segment of the beam
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        
        # Check if this segment intersects the rect
        hit = line_rect_intersection(p1, p2, rect)
        if hit:
            dist = (hit - points[0]).length()
            if dist < closest_dist:
                closest_dist = dist
                closest_hit = hit
    
    # Also check if any point is inside the rect (for thick beams)
    for point in points:
        if rect.collidepoint(point.x, point.y):
            dist = (point - points[0]).length()
            if dist < closest_dist:
                closest_dist = dist
                closest_hit = point
    
    return (closest_hit, closest_dist)


def generate_paraboloid_points(center: pygame.Vector2, width: float, height: float, rotation: float) -> list[pygame.Vector2]:
    """Generate points for a paraboloid shape (parabolic curve in 2D).
    
    Args:
        center: Center position of the paraboloid
        width: Width of the paraboloid
        height: Height of the paraboloid
        rotation: Rotation angle in radians
    
    Returns:
        List of points forming the paraboloid shape
    """
    points = []
    num_points = 100  # Number of points for smooth curve
    
    # Generate points for a parabolic curve
    for i in range(num_points + 1):
        # Parameter t from -1 to 1
        t = (i / num_points) * 2.0 - 1.0
        
        # Parabolic curve: y = a * x^2
        # We'll create a U-shaped parabola
        x_local = t * (width / 2)
        y_local = (t ** 2) * (height / 2)  # Parabolic curve
        
        # Rotate the point around center
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)
        x_rotated = x_local * cos_r - y_local * sin_r
        y_rotated = x_local * sin_r + y_local * cos_r
        
        # Translate to center position
        point = pygame.Vector2(
            center.x + x_rotated,
            center.y + y_rotated
        )
        points.append(point)
    
    return points


def generate_trapezoid_points(center: pygame.Vector2, width: float, height: float, rotation: float) -> list[pygame.Vector2]:
    """Generate points for a trapezoid shape.
    
    Args:
        center: Center position of the trapezoid
        width: Width of the trapezoid (top and bottom)
        height: Height of the trapezoid
        rotation: Rotation angle in radians
    
    Returns:
        List of points forming the trapezoid shape
    """
    points = []
    # Create a trapezoid (wider at bottom)
    top_width = width * 0.6
    bottom_width = width
    
    # Local coordinates
    local_points = [
        (-top_width / 2, -height / 2),  # Top left
        (top_width / 2, -height / 2),   # Top right
        (bottom_width / 2, height / 2),  # Bottom right
        (-bottom_width / 2, height / 2),  # Bottom left
    ]
    
    # Rotate and translate
    cos_r = math.cos(rotation)
    sin_r = math.sin(rotation)
    for x_local, y_local in local_points:
        x_rotated = x_local * cos_r - y_local * sin_r
        y_rotated = x_local * sin_r + y_local * cos_r
        point = pygame.Vector2(center.x + x_rotated, center.y + y_rotated)
        points.append(point)
    
    return points


def check_point_in_hazard(point: pygame.Vector2, hazard_points: list[pygame.Vector2], bounding_rect: pygame.Rect) -> bool:
    """Check if a point is inside the hazard shape (paraboloid or trapezoid).
    
    Uses point-in-polygon algorithm.
    """
    if not bounding_rect.collidepoint(point.x, point.y):
        return False
    
    # Use ray casting algorithm for point-in-polygon
    x, y = point.x, point.y
    n = len(hazard_points)
    if n < 3:
        return False
    
    inside = False
    p1x, p1y = hazard_points[0].x, hazard_points[0].y
    for i in range(1, n + 1):
        p2x, p2y = hazard_points[i % n].x, hazard_points[i % n].y
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def check_hazard_collision(hazard1: dict, hazard2: dict) -> bool:
    """Check if two hazards are colliding based on their bounding rectangles."""
    return hazard1["bounding_rect"].colliderect(hazard2["bounding_rect"])


def resolve_hazard_collision(hazard1: dict, hazard2: dict):
    """Resolve collision between two hazards - make them bounce off each other."""
    # Calculate collision normal (direction from hazard1 to hazard2)
    center1 = hazard1["center"]
    center2 = hazard2["center"]
    normal = (center2 - center1)
    if normal.length_squared() > 0:
        normal = normal.normalize()
    else:
        # If centers overlap, use random direction
        normal = pygame.Vector2(1, 0)
    
    # Calculate relative velocity
    rel_vel = hazard2["velocity"] - hazard1["velocity"]
    
    # Calculate relative velocity along collision normal
    vel_along_normal = rel_vel.dot(normal)
    
    # Don't resolve if velocities are separating
    if vel_along_normal > 0:
        return
    
    # Calculate bounce (elastic collision)
    # For simplicity, we'll use a simple bounce with some energy loss
    restitution = 0.8  # Energy retention (0.8 = 80% energy retained)
    
    # Calculate impulse
    impulse = vel_along_normal * restitution
    
    # Apply impulse to velocities
    hazard1["velocity"] += normal * impulse
    hazard2["velocity"] -= normal * impulse
    
    # Separate the hazards slightly to prevent sticking
    separation = 10.0
    hazard1["center"] -= normal * separation
    hazard2["center"] += normal * separation


def update_hazard_obstacles(dt: float):
    """Update all rotating hazard obstacles (paraboloids/trapezoids) with collision physics."""
    global hazard_obstacles, current_level
    
    # Update each hazard
    for hazard in hazard_obstacles:
        # Determine shape based on level
        if current_level >= 2:
            hazard["shape"] = "trapezoid"
        else:
            hazard["shape"] = "paraboloid"
        # Update rotation
        hazard["rotation_angle"] += hazard["rotation_speed"] * dt
        if hazard["rotation_angle"] >= 2 * math.pi:
            hazard["rotation_angle"] -= 2 * math.pi
        
        # Update orbit position
        hazard["orbit_angle"] += hazard["orbit_speed"] * dt
        if hazard["orbit_angle"] >= 2 * math.pi:
            hazard["orbit_angle"] -= 2 * math.pi
        
        # Calculate orbit position
        orbit_pos = pygame.Vector2(
            hazard["orbit_center"].x + math.cos(hazard["orbit_angle"]) * hazard["orbit_radius"],
            hazard["orbit_center"].y + math.sin(hazard["orbit_angle"]) * hazard["orbit_radius"]
        )
        
        # Apply velocity for collision physics
        hazard["center"] += hazard["velocity"] * dt
        
        # Blend orbit position with velocity-based movement (50/50)
        hazard["center"] = hazard["center"] * 0.5 + orbit_pos * 0.5
        
        # Keep within screen bounds with bounce
        if hazard["center"].x < hazard["width"] // 2:
            hazard["center"].x = hazard["width"] // 2
            hazard["velocity"].x = abs(hazard["velocity"].x)  # Bounce right
        elif hazard["center"].x > WIDTH - hazard["width"] // 2:
            hazard["center"].x = WIDTH - hazard["width"] // 2
            hazard["velocity"].x = -abs(hazard["velocity"].x)  # Bounce left
        
        if hazard["center"].y < hazard["height"] // 2:
            hazard["center"].y = hazard["height"] // 2
            hazard["velocity"].y = abs(hazard["velocity"].y)  # Bounce up
        elif hazard["center"].y > HEIGHT - hazard["height"] // 2:
            hazard["center"].y = HEIGHT - hazard["height"] // 2
            hazard["velocity"].y = -abs(hazard["velocity"].y)  # Bounce down
        
        # Regenerate points with new rotation and position based on shape
        if hazard["shape"] == "trapezoid":
            hazard["points"] = generate_trapezoid_points(
                hazard["center"],
                hazard["width"],
                hazard["height"],
                hazard["rotation_angle"]
            )
        else:
            hazard["points"] = generate_paraboloid_points(
                hazard["center"],
                hazard["width"],
                hazard["height"],
                hazard["rotation_angle"]
            )
        
        # Update bounding rect
        if hazard["points"]:
            min_x = min(p.x for p in hazard["points"])
            max_x = max(p.x for p in hazard["points"])
            min_y = min(p.y for p in hazard["points"])
            max_y = max(p.y for p in hazard["points"])
            hazard["bounding_rect"] = pygame.Rect(
                min_x, min_y,
                max_x - min_x,
                max_y - min_y
            )
    
    # Check collisions between hazards
    for i in range(len(hazard_obstacles)):
        for j in range(i + 1, len(hazard_obstacles)):
            if check_hazard_collision(hazard_obstacles[i], hazard_obstacles[j]):
                resolve_hazard_collision(hazard_obstacles[i], hazard_obstacles[j])


def spawn_pickup(pickup_type: str):
    # Make pickups bigger (2x size)
    size = (64, 64)  # Doubled from 32x32
    max_attempts = 50  # Increased attempts to avoid overlaps
    for _ in range(max_attempts):
        r = random_spawn_position(size, state)
        # Check if pickup overlaps with existing pickups
        overlaps = False
        for existing_pickup in state.pickups:
            if r.colliderect(existing_pickup["rect"]):
                overlaps = True
                break
        # Check if pickup overlaps with health zone
        if r.colliderect(moving_health_zone["rect"]):
            overlaps = True
        
        if not overlaps:
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
            return  # Successfully spawned, exit function
    # If we couldn't find a non-overlapping position, skip spawning this pickup


def spawn_weapon_in_center(weapon_type: str, state: GameState):
    """Spawn a weapon pickup in the center of the screen (level completion reward)."""
    # Do not spawn basic beam as a pickup
    if weapon_type == "basic":
        return
    # Weapon colors are now imported from config_weapons.py
    weapon_pickup_size = (80, 80)  # Bigger for level completion rewards (2x from 40x40)
    weapon_pickup_rect = pygame.Rect(
        WIDTH // 2 - weapon_pickup_size[0] // 2,
        HEIGHT // 2 - weapon_pickup_size[1] // 2,
        weapon_pickup_size[0],
        weapon_pickup_size[1]
    )
    state.pickups.append({
        "type": weapon_type,
        "rect": weapon_pickup_rect,
        "color": WEAPON_DISPLAY_COLORS.get(weapon_type, (180, 100, 255)),
        "timer": 30.0,  # Level completion weapons last longer
        "age": 0.0,
        "is_weapon_drop": True,
        "is_level_reward": True,  # Mark as level completion reward
    })


def spawn_weapon_drop(enemy: dict, state: GameState):
    """Spawn a weapon drop from a killed enemy."""
    enemy_type = enemy.get("type", "grunt")
    weapon_drop_map = {
        "grunt": "basic",
        "stinky": "basic",
        "heavy": "rocket",
        "baka": "triple",
        "neko neko desu": "bouncing",
        "BIG NEKU": "wave_beam",  # Wave beam second to last
        "bouncer": "bouncing",
    }
    # 30% chance to drop weapon (exclude basic beam)
    if random.random() < 0.3 and enemy_type in weapon_drop_map:
        weapon_type = weapon_drop_map[enemy_type]
        # Skip basic beam - do not drop it as a pickup
        if weapon_type == "basic":
            return
        # Spawn weapon pickup at enemy location (2x size)
        weapon_pickup_size = (56, 56)  # Doubled from 28x28
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
        state.pickups.append({
            "type": weapon_type,
            "rect": weapon_pickup_rect,
            "color": WEAPON_DISPLAY_COLORS.get(weapon_type, (180, 100, 255)),
            "timer": 10.0,  # Weapon pickups last 10 seconds
            "age": 0.0,
            "is_weapon_drop": True,  # Mark as weapon drop
        })


# Rendering helper functions are now imported from rendering.py


def create_pickup_collection_effect(x: int, y: int, color: tuple[int, int, int], state: GameState):
    """Create particle effect when pickup is collected."""
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 150)
        state.collection_effects.append({
            "x": float(x),
            "y": float(y),
            "vel_x": math.cos(angle) * speed,
            "vel_y": math.sin(angle) * speed,
            "color": color,
            "life": 0.4,  # particle lifetime
            "size": random.randint(3, 6),
        })


def update_pickup_effects(dt: float, state: GameState):
    """Update pickup particle effects."""
    # Update collection effects
    for effect in state.collection_effects[:]:
        effect["x"] += effect["vel_x"] * dt
        effect["y"] += effect["vel_y"] * dt
        effect["life"] -= dt
        if effect["life"] <= 0:
            state.collection_effects.remove(effect)
    
    # Generate particles around pickups
    state.pickup_particles.clear()
    for p in state.pickups:
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
            state.pickup_particles.append({
                "x": px,
                "y": py,
                "color": p["color"],
                "alpha": int(glow_alpha * 0.6),
                "size": 3,
            })


# Rendering helper functions are now imported from rendering.py


def spawn_player_bullet_and_log(state: GameState):
    if state.player_rect is None:
        return
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
            if state.last_move_velocity.length_squared() > 0:
                base_dir = state.last_move_velocity.normalize()
            else:
                base_dir = pygame.Vector2(1, 0)  # Default right
        else:
            base_dir = pygame.Vector2(dx, dy).normalize()
        
        # Calculate target position for telemetry (extend direction from player)
        target_dist = 100  # Distance to calculate target point
        mx = int(state.player_rect.centerx + base_dir.x * target_dist)
        my = int(state.player_rect.centery + base_dir.y * target_dist)
    else:
        # Mouse aiming (default)
        mx, my = pygame.mouse.get_pos()
        base_dir = vec_toward(state.player_rect.centerx, state.player_rect.centery, mx, my)

    shape = player_bullet_shapes[state.player_bullet_shape_index % len(player_bullet_shapes)]
    state.player_bullet_shape_index = (state.player_bullet_shape_index + 1) % len(player_bullet_shapes)

    # Get weapon config (default to basic if not found)
    weapon_config = WEAPON_CONFIGS.get(state.current_weapon_mode, WEAPON_CONFIGS["basic"])
    
    # Determine shot pattern based on weapon mode
    if weapon_config["num_projectiles"] > 1:
        # Multi-projectile weapons (triple, basic)
        spread_angle_deg = weapon_config["spread_angle_deg"]
        directions = [
            base_dir,  # center
            base_dir.rotate(-spread_angle_deg),  # left
            base_dir.rotate(spread_angle_deg),  # right
        ]
    else:
        directions = [base_dir]

    # Spawn bullets for each direction
    for d in directions:
        # Apply stat multipliers and weapon-specific multipliers
        size_mult = state.player_stat_multipliers["bullet_size"] * weapon_config["size_multiplier"]
        
        effective_size = (
            int(player_bullet_size[0] * size_mult),
            int(player_bullet_size[1] * size_mult),
        )
        effective_speed = player_bullet_speed * state.player_stat_multipliers["bullet_speed"] * weapon_config["speed_multiplier"]
        base_damage = int(state.player_bullet_damage * state.player_stat_multipliers["bullet_damage"])
        
        # Apply weapon damage multiplier
        effective_damage = int(base_damage * weapon_config["damage_multiplier"])
        
        # Apply random damage multiplier (from random_damage pickup)
        effective_damage = int(effective_damage * state.random_damage_multiplier)
        
        # Rocket launcher: always has explosion
        if weapon_config["is_rocket"]:
            rocket_explosion = max(weapon_config["explosion_radius"], state.player_stat_multipliers["bullet_explosion_radius"] + 100.0)
        else:
            rocket_explosion = max(weapon_config["explosion_radius"], state.player_stat_multipliers["bullet_explosion_radius"])

        r = pygame.Rect(
            state.player_rect.centerx - effective_size[0] // 2,
            state.player_rect.centery - effective_size[1] // 2,
            effective_size[0],
            effective_size[1],
        )
        state.player_bullets.append({
                "rect": r,
                "vel": d * effective_speed,
                "shape": shape,
                "color": weapon_config.get("color", player_bullets_color),  # Use weapon color from config
                "damage": effective_damage,
                "penetration": int(state.player_stat_multipliers["bullet_penetration"]),
                "explosion_radius": rocket_explosion,
                "knockback": state.player_stat_multipliers["bullet_knockback"],
                "bounces": weapon_config["max_bounces"],  # Max bounces from config
                "is_rocket": weapon_config["is_rocket"],
            })
    state.shots_fired += 1

    if telemetry_enabled and telemetry:
        telemetry.log_shot(
            ShotEvent(
                t=state.run_time,
                origin_x=state.player_rect.centerx,
                origin_y=state.player_rect.centery,
                target_x=mx,
                target_y=my,
                dir_x=float(d.x),
                dir_y=float(d.y),
            )
        )

        # Log bullet metadata
        telemetry.log_bullet_metadata(
            BulletMetadataEvent(
                t=state.run_time,
                bullet_type="player",
                shape=shape,
                color_r=player_bullets_color[0],
                color_g=player_bullets_color[1],
                color_b=player_bullets_color[2],
            )
        )


def spawn_enemy_projectile(enemy: dict, state: GameState):
    """Spawn projectile from enemy targeting nearest threat (player or friendly AI)."""
    if state.player_rect is None:
        return
    e_pos = pygame.Vector2(enemy["rect"].center)
    threat_result = find_nearest_threat(e_pos, state.player_rect, state.friendly_ai)

    # Calculate direction
    if threat_result:
        threat_pos, threat_type = threat_result
        d = vec_toward(e_pos.x, e_pos.y, threat_pos.x, threat_pos.y)
    else:
        # Fallback to player if no threats
        d = vec_toward(enemy["rect"].centerx, enemy["rect"].centery, state.player_rect.centerx, state.player_rect.centery)
    
    # Create projectile rect and properties (used regardless of threat result)
    r = pygame.Rect(
        enemy["rect"].centerx - enemy_projectile_size[0] // 2,
        enemy["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    proj_color = enemy.get("projectile_color", enemy_projectiles_color)
    proj_shape = enemy.get("projectile_shape", "circle")
    bounces = enemy.get("bouncing_projectiles", False)
    
    state.enemy_projectiles.append({
        "rect": r,
        "vel": d * enemy["projectile_speed"],
        "enemy_type": enemy["type"],  # attribute damage source
        "color": proj_color,
        "shape": proj_shape,
        "bounces": 10 if bounces else 0,  # max bounces for bouncing enemy type
    })
    
    # Log enemy projectile metadata
    if telemetry_enabled and telemetry:
        telemetry.log_bullet_metadata(
            BulletMetadataEvent(
                t=state.run_time,
                bullet_type="enemy",
                shape=proj_shape,
                color_r=proj_color[0],
                color_g=proj_color[1],
                color_b=proj_color[2],
                source_enemy_type=enemy["type"],
            )
        )


def spawn_enemy_projectile_predictive(enemy: dict, direction: pygame.Vector2, state: GameState):
    """Spawn projectile from predictive enemy in a specific direction (predicted player position)."""
    r = pygame.Rect(
        enemy["rect"].centerx - enemy_projectile_size[0] // 2,
        enemy["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    proj_color = enemy.get("projectile_color", enemy_projectiles_color)
    proj_shape = enemy.get("projectile_shape", "diamond")  # Rhomboid shape
    state.enemy_projectiles.append({
        "rect": r,
        "vel": direction * enemy["projectile_speed"],
        "enemy_type": enemy["type"],
        "color": proj_color,
        "shape": proj_shape,
        "bounces": 0,
        "lifetime": 5.0,  # Projectiles disappear after 5 seconds to prevent lingering
    })


def spawn_boss_projectile(boss: dict, direction: pygame.Vector2, state: GameState):
    """Spawn a projectile from the boss in a specific direction."""
    r = pygame.Rect(
        boss["rect"].centerx - enemy_projectile_size[0] // 2,
        boss["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    proj_color = boss.get("projectile_color", enemy_projectiles_color)
    proj_shape = boss.get("projectile_shape", "circle")
    state.enemy_projectiles.append(
        {
            "rect": r,
            "vel": direction * boss["projectile_speed"],
            "enemy_type": boss["type"],
            "color": proj_color,
            "shape": proj_shape,
            "bounces": 0,
            "lifetime": 5.0,  # Boss projectiles disappear after 5 seconds to prevent lingering
        }
    )


def log_enemy_spawns_for_current_wave():
    enemies_spawned_ref = [enemies_spawned]
    log_enemy_spawns(enemies, telemetry, run_time, enemies_spawned_ref)
    enemies_spawned = enemies_spawned_ref[0]


def calculate_kill_score(wave_num: int, run_time: float) -> int:
    """Calculate score for killing an enemy."""
    return SCORE_BASE_POINTS + (wave_num * SCORE_WAVE_MULTIPLIER) + int(run_time * SCORE_TIME_MULTIPLIER)


# Enemy defeat messages
enemy_defeat_messages: list[dict] = []  # List of {enemy_type, timer} for defeat messages

def kill_enemy(enemy: dict, state: GameState):
    """Handle enemy death: drop weapon, update score, remove from list, and clean up projectiles."""
    is_boss = enemy.get("is_boss", False)
    
    # Spawner enemy: when killed, all spawned enemies die
    if enemy.get("is_spawner"):
        # Find and kill all enemies spawned by this spawner
        for spawned_enemy in state.enemies[:]:
            if spawned_enemy.get("spawned_by") is enemy:
                # Recursively kill spawned enemy (but don't drop weapons for spawned enemies)
                spawned_enemy_type = spawned_enemy.get("type", "enemy")
                # Remove projectiles
                for proj in state.enemy_projectiles[:]:
                    if proj.get("enemy_type") == spawned_enemy_type:
                        state.enemy_projectiles.remove(proj)
                # Remove from list
                try:
                    state.enemies.remove(spawned_enemy)
                except ValueError:
                    pass
                state.enemies_killed += 1
                state.score += calculate_kill_score(state.wave_number, state.run_time)
    
    # Add defeat message
    enemy_type = enemy.get("type", "enemy")
    state.enemy_defeat_messages.append({
        "enemy_type": enemy_type,
        "timer": 3.0,  # Display for 3 seconds
    })
    
    # Remove projectiles and damage numbers associated with this dead enemy
    enemy_pos = pygame.Vector2(enemy["rect"].center)
    cleanup_radius_sq = 2500  # 50 pixels squared - damage numbers within this range are removed
    
    # Remove ALL enemy projectiles from this dead enemy (by matching enemy_type)
    # This ensures projectiles are removed regardless of distance when enemy dies
    for proj in state.enemy_projectiles[:]:
        # Remove if projectile matches this enemy's type
        # This removes all projectiles from this enemy, even if they've traveled far
        if proj.get("enemy_type") == enemy_type:
            state.enemy_projectiles.remove(proj)
    
    # Remove damage numbers near the dead enemy's position
    for dmg_num in state.damage_numbers[:]:
        dmg_pos = pygame.Vector2(dmg_num["x"], dmg_num["y"])
        if (dmg_pos - enemy_pos).length_squared() < cleanup_radius_sq:
            state.damage_numbers.remove(dmg_num)
    
    # If boss is killed, spawn level completion weapon in center
    if is_boss:
        # Weapon unlock order is now imported from config_weapons.py
        if state.current_level in WEAPON_UNLOCK_ORDER:
            weapon_to_unlock = WEAPON_UNLOCK_ORDER[state.current_level]
            if weapon_to_unlock not in state.unlocked_weapons:
                spawn_weapon_in_center(weapon_to_unlock, state)
    else:
        # Regular enemies drop weapons randomly (except suicide enemies which despawn)
        if not enemy.get("is_suicide"):
            spawn_weapon_drop(enemy, state)
    
    try:
        state.enemies.remove(enemy)
    except ValueError:
        pass  # Already removed
    state.enemies_killed += 1
    state.score += calculate_kill_score(state.wave_number, state.run_time)


def apply_pickup_effect(pickup_type: str, state: GameState):
    """Apply the effect of a collected pickup."""
    if pickup_type == "boost":
        state.boost_meter = min(boost_meter_max, state.boost_meter + 45.0)
    elif pickup_type == "firerate":
        state.fire_rate_buff_t = fire_rate_buff_duration
    elif pickup_type == "health":
        # Restore 100 HP (capped at max HP)
        state.player_hp = min(state.player_max_hp, state.player_hp + 100)
    elif pickup_type == "max_health":
        state.player_max_hp += 15
        state.player_hp += 15  # also heal by the same amount
    elif pickup_type == "speed":
        state.player_stat_multipliers["speed"] += 0.15
    elif pickup_type == "firerate_permanent":
        # Cap fire rate multiplier at 2.0 (2x firing speed max) to prevent performance issues
        state.player_stat_multipliers["firerate"] = min(2.0, state.player_stat_multipliers["firerate"] + 0.12)
    elif pickup_type == "bullet_size":
        state.player_stat_multipliers["bullet_size"] += 0.20
    elif pickup_type == "bullet_speed":
        state.player_stat_multipliers["bullet_speed"] += 0.15
    elif pickup_type == "bullet_damage":
        state.player_stat_multipliers["bullet_damage"] += 0.20
    elif pickup_type == "bullet_knockback":
        state.player_stat_multipliers["bullet_knockback"] += 0.25
    elif pickup_type == "bullet_penetration":
        state.player_stat_multipliers["bullet_penetration"] += 1
    elif pickup_type == "bullet_explosion":
        state.player_stat_multipliers["bullet_explosion_radius"] += 25.0
    elif pickup_type == "health_regen":
        # Increase player health regeneration rate
        state.player_health_regen_rate += 5.0  # Add 5 HP per second regeneration
    elif pickup_type == "random_damage":
        # Randomize damage multiplier (between 0.5x and 2.0x)
        state.random_damage_multiplier = random.uniform(0.5, 2.0)  # Random multiplier between 0.5x and 2.0x
    elif pickup_type == "spawn_boost":
        # Reduce ally drop cooldown (boost player's ability to spawn allies)
        global ally_drop_cooldown
        ally_drop_cooldown = max(1.0, ally_drop_cooldown * 0.8)  # Reduce cooldown by 20% (minimum 1 second)
    # Weapon pickups - unlock and switch to weapon
    elif pickup_type in ["giant_bullets", "giant"]:
        state.unlocked_weapons.add("giant")
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
        if state.previous_weapon_mode == "wave_beam":
            state.wave_beams.clear()
        if state.previous_weapon_mode == "laser":
            state.laser_beams.clear()
        state.current_weapon_mode = "giant"
        # Log weapon switch from pickup
        if state.previous_weapon_mode != state.current_weapon_mode:
            if telemetry_enabled and telemetry:
                telemetry.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=player.centerx,
                    y=player.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type in ["triple_shot", "triple"]:
        state.unlocked_weapons.add("triple")
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
        if state.previous_weapon_mode == "wave_beam":
            state.wave_beams.clear()
        if state.previous_weapon_mode == "laser":
            state.laser_beams.clear()
        state.current_weapon_mode = "triple"
        # Weapon names and colors are now imported from config_weapons.py
        state.weapon_pickup_messages.append({
            "weapon_name": WEAPON_NAMES.get("triple", "TRIPLE SHOT"),
            "timer": 3.0,
            "color": WEAPON_DISPLAY_COLORS.get("triple", (255, 255, 255))
        })
        if state.previous_weapon_mode != state.current_weapon_mode:
            if telemetry_enabled and telemetry:
                telemetry.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=player.centerx,
                    y=player.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type in ["bouncing_bullets", "bouncing"]:
        state.unlocked_weapons.add("bouncing")
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
        if state.previous_weapon_mode == "wave_beam":
            state.wave_beams.clear()
        if state.previous_weapon_mode == "laser":
            state.laser_beams.clear()
        state.current_weapon_mode = "bouncing"
        # Weapon names and colors are now imported from config_weapons.py
        state.weapon_pickup_messages.append({
            "weapon_name": WEAPON_NAMES.get("bouncing", "BOUNCING BULLETS"),
            "timer": 3.0,
            "color": WEAPON_DISPLAY_COLORS.get("bouncing", (255, 255, 255))
        })
        if state.previous_weapon_mode != state.current_weapon_mode:
            if telemetry_enabled and telemetry:
                telemetry.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=player.centerx,
                    y=player.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type in ["rocket_launcher", "rocket"]:
        state.unlocked_weapons.add("rocket")
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
        if state.previous_weapon_mode == "wave_beam":
            state.wave_beams.clear()
        if state.previous_weapon_mode == "laser":
            state.laser_beams.clear()
        state.current_weapon_mode = "rocket"
        # Weapon names and colors are now imported from config_weapons.py
        state.weapon_pickup_messages.append({
            "weapon_name": WEAPON_NAMES.get("rocket", "ROCKET LAUNCHER"),
            "timer": 3.0,
            "color": WEAPON_DISPLAY_COLORS.get("rocket", (255, 255, 255))
        })
        if state.previous_weapon_mode != state.current_weapon_mode:
            if telemetry_enabled and telemetry:
                telemetry.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=player.centerx,
                    y=player.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type == "laser":
        state.unlocked_weapons.add("laser")
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
        if state.previous_weapon_mode == "wave_beam":
            state.wave_beams.clear()
        state.current_weapon_mode = "laser"
        # Weapon names and colors are now imported from config_weapons.py
        state.weapon_pickup_messages.append({
            "weapon_name": WEAPON_NAMES.get("laser", "LASER BEAM"),
            "timer": 3.0,
            "color": WEAPON_DISPLAY_COLORS.get("laser", (255, 255, 255))
        })
        if state.previous_weapon_mode != state.current_weapon_mode:
            if telemetry_enabled and telemetry:
                telemetry.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=player.centerx,
                    y=player.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type == "basic":
        state.unlocked_weapons.add("basic")  # Should already be unlocked, but ensure it
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
        if state.previous_weapon_mode == "wave_beam":
            state.wave_beams.clear()
        if state.previous_weapon_mode == "laser":
            state.laser_beams.clear()
        state.current_weapon_mode = "basic"
        # Weapon names and colors are now imported from config_weapons.py
        state.weapon_pickup_messages.append({
            "weapon_name": WEAPON_NAMES.get("basic", "BASIC FIRE"),
            "timer": 3.0,
            "color": WEAPON_DISPLAY_COLORS.get("basic", (255, 255, 255))
        })
        if state.previous_weapon_mode != state.current_weapon_mode:
            if telemetry_enabled and telemetry:
                telemetry.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=player.centerx,
                    y=player.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type == "wave_beam":
        state.unlocked_weapons.add("wave_beam")
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
        if state.previous_weapon_mode == "laser":
            state.laser_beams.clear()
        state.current_weapon_mode = "wave_beam"
        weapon_names = {
            "giant": "GIANT BULLETS",
            "triple": "TRIPLE SHOT",
            "bouncing": "BOUNCING BULLETS",
            "rocket": "ROCKET LAUNCHER",
            "laser": "LASER BEAM",
            "basic": "BASIC FIRE",
            "wave_beam": "WAVE BEAM"
        }
        weapon_colors = {
            "giant": (255, 200, 0),
            "triple": (100, 200, 255),
            "bouncing": (100, 255, 100),
            "rocket": (255, 100, 0),
            "laser": (255, 50, 50),
            "basic": (200, 200, 200),
            "wave_beam": (50, 255, 50)
        }
        state.weapon_pickup_messages.append({
            "weapon_name": weapon_names.get("wave_beam", "WAVE BEAM"),
            "timer": 3.0,
            "color": weapon_colors.get("wave_beam", (50, 255, 50))
        })
        if state.previous_weapon_mode != state.current_weapon_mode:
            if telemetry_enabled and telemetry:
                telemetry.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=player.centerx,
                    y=player.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type == "overshield":
        state.overshield = min(overshield_max, state.overshield + 25)


# render_hud_text is now imported from rendering.py


def reset_after_death(state: GameState):
    state.player_hp = state.player_max_hp
    state.player_health_regen_rate = 0.0  # Reset health regeneration rate
    state.random_damage_multiplier = 1.0  # Reset random damage multiplier
    state.damage_numbers.clear()  # Clear damage numbers on death
    state.weapon_pickup_messages.clear()  # Clear weapon pickup messages on death
    state.grenade_explosions.clear()  # Clear grenade explosions on death
    state.grenade_time_since_used = 999.0  # Reset grenade cooldown
    state.missiles.clear()  # Clear missiles on death
    state.missile_time_since_used = 999.0  # Reset missile cooldown
    state.dropped_ally = None  # Clear dropped ally on death
    state.ally_drop_timer = 0.0  # Reset ally drop timer on death
    # Reset moving health zone to center
    moving_health_zone["rect"].center = (WIDTH // 4, HEIGHT // 4)  # Offset from center (boss spawn)
    moving_health_zone["target"] = None
    state.overshield = 0  # Reset overshield
    state.player_time_since_shot = 999.0
    state.laser_time_since_shot = 999.0
    state.wave_beam_time_since_shot = 999.0
    state.wave_beam_pattern_index = 0
    state.pos_timer = 0.0
    state.wave_number = 1
    state.wave_in_level = 1
    state.current_level = 1
    state.unlocked_weapons = {"basic"}  # Reset to basic only
    state.current_weapon_mode = "basic"  # Reset to basic weapon
    state.previous_weapon_mode = "basic"
    state.previous_boost_state = False
    state.previous_slow_state = False
    state.player_current_zones = set()
    state.jump_cooldown_timer = 0.0
    state.jump_timer = 0.0
    state.is_jumping = False
    state.jump_velocity = pygame.Vector2(0, 0)
    state.laser_beams.clear()
    state.wave_beams.clear()
    # Reset hazard obstacles positions (corners)
    hazard_obstacles[0]["center"] = pygame.Vector2(250, 250)  # Top-left
    hazard_obstacles[0]["rotation_angle"] = 0.0
    hazard_obstacles[0]["orbit_angle"] = 0.0
    hazard_obstacles[0]["velocity"] = pygame.Vector2(150, 90)  # 3x faster
    hazard_obstacles[0]["points"] = []
    hazard_obstacles[1]["center"] = pygame.Vector2(WIDTH - 250, 250)  # Top-right
    hazard_obstacles[1]["rotation_angle"] = 1.0
    hazard_obstacles[1]["orbit_angle"] = 1.5
    hazard_obstacles[1]["velocity"] = pygame.Vector2(-120, 150)  # 3x faster
    hazard_obstacles[1]["points"] = []
    hazard_obstacles[2]["center"] = pygame.Vector2(250, HEIGHT - 250)  # Bottom-left
    hazard_obstacles[2]["rotation_angle"] = 2.0
    hazard_obstacles[2]["orbit_angle"] = 3.0
    hazard_obstacles[2]["velocity"] = pygame.Vector2(90, -135)  # 3x faster
    hazard_obstacles[2]["points"] = []
    hazard_obstacles[3]["center"] = pygame.Vector2(WIDTH - 250, HEIGHT - 250)  # Bottom-right
    hazard_obstacles[3]["rotation_angle"] = 1.5
    hazard_obstacles[3]["orbit_angle"] = 2.5
    hazard_obstacles[3]["velocity"] = pygame.Vector2(-105, -120)  # 3x faster
    hazard_obstacles[3]["points"] = []
    # Reset shield
    state.shield_active = False
    state.shield_duration_remaining = 0.0
    state.shield_cooldown_remaining = 0.0

    player.x = (WIDTH - player.w) // 2
    player.y = (HEIGHT - player.h) // 2
    clamp_rect_to_screen(player)

    state.player_bullets.clear()
    state.enemy_projectiles.clear()
    state.friendly_ai.clear()
    state.friendly_projectiles.clear()

    state.wave_number = 1
    state.time_to_next_wave = 0.0
    start_wave(state.wave_number, state)


if __name__ == "__main__":
    main()
