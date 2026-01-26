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
    NoOpTelemetry,
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
from rendering import draw_centered_text
from enemies import (
    find_nearest_threat,
    make_enemy_from_template,
)
from allies import (
    find_nearest_enemy,
    make_friendly_from_template,
    spawn_friendly_ai,
    spawn_friendly_projectile,
    update_friendly_ai,
)
from state import GameState
from context import AppContext
from screens import SCREEN_HANDLERS
from screens.gameplay import render as gameplay_render
from systems.movement_system import update as movement_update
from systems.collision_system import update as collision_update
from systems.spawn_system import update as spawn_update, start_wave as spawn_system_start_wave
from systems.ai_system import update as ai_update
from controls_io import _key_name_to_code, load_controls, save_controls
from geometry_utils import (
    clamp_rect_to_screen,
    vec_toward,
    line_rect_intersection,
    can_move_rect,
    rect_offscreen,
    filter_blocks_too_close_to_player,
    set_screen_dimensions,
)
from level_utils import filter_blocks_no_overlap, clone_enemies_from_templates
from hazards import hazard_obstacles, update_hazard_obstacles, check_point_in_hazard

# Placeholder WIDTH/HEIGHT for module-level geometry (trapezoids, etc.). Runtime dimensions live in AppContext (ctx.width, ctx.height).
WIDTH = 1920
HEIGHT = 1080

# ----------------------------
# Rendering cache for performance optimization
# ----------------------------
# Wall texture, HUD text, health bar, and trapezoid/triangle caches are in rendering.py


def main():
    """Main entry point for the game. All mutable game state lives in the GameState instance."""
    global trapezoid_blocks, triangle_blocks, destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks
    global hazard_obstacles, moving_health_zone
    global difficulty_selected, aiming_mode_selected, use_character_profile_selected, character_profile_selected
    global custom_profile_stat_selected, player_class_selected, ui_show_metrics_selected, beam_selection_selected
    global endurance_mode_selected, ui_telemetry_enabled_selected
    global weapon_selection_options
    global boost_meter_max, boost_drain_per_s, boost_regen_per_s, boost_speed_mult
    global friendly_ai_templates, overshield_max, grenade_cooldown, missile_cooldown, ally_drop_cooldown

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
    set_screen_dimensions(WIDTH, HEIGHT)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Mouse Aim Shooter + Telemetry (SQLite)")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 56)
    small_font = pygame.font.SysFont(None, 20)

    # Load controls from file (now that pygame is initialized)
    global controls
    if not controls:
        controls = load_controls()

    # Application context: screen, fonts, clock, telemetry, difficulty, and other app-level config
    ctx = AppContext(
        screen=screen,
        clock=clock,
        font=font,
        big_font=big_font,
        small_font=small_font,
        width=WIDTH,
        height=HEIGHT,
        telemetry_client=None,
        telemetry_enabled=False,
        run_started_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        controls=controls,
        difficulty=DIFFICULTY_NORMAL,
        aiming_mode=AIM_MOUSE,
        profile_enabled=False,
        player_class=PLAYER_CLASS_BALANCED,
        testing_mode=True,
        invulnerability_mode=False,
        ui_show_metrics=True,
        ui_show_hud=True,
        ui_show_health_bars=True,
        ui_show_player_health_bar=True,
    )

    # Create GameState as the single source of truth for all mutable game state.
    game_state = GameState()
    game_state.player_rect = pygame.Rect((ctx.width - 28) // 2, (ctx.height - 28) // 2, 28, 28)
    game_state.current_screen = STATE_TITLE
    game_state.run_started_at = ctx.run_started_at

    # Local alias for readability where the loop uses "player" frequently.
    player = game_state.player_rect

    # Initialize pygame mouse visibility
    pygame.mouse.set_visible(True)

    # Filter blocks to prevent overlaps (moved from module level)
    global destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks
    destructible_blocks = filter_blocks_no_overlap(destructible_blocks, [moveable_destructible_blocks, giant_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], game_state.player_rect)
    moveable_destructible_blocks = filter_blocks_no_overlap(moveable_destructible_blocks, [destructible_blocks, giant_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], game_state.player_rect)
    giant_blocks = filter_blocks_no_overlap(giant_blocks, [destructible_blocks, moveable_destructible_blocks, super_giant_blocks, trapezoid_blocks, triangle_blocks], game_state.player_rect)
    super_giant_blocks = filter_blocks_no_overlap(super_giant_blocks, [destructible_blocks, moveable_destructible_blocks, giant_blocks, trapezoid_blocks, triangle_blocks], game_state.player_rect)

    # Level context for movement_system and collision_system (callables and data; avoids circular imports)
    def _make_level_context():
        w, h = ctx.width, ctx.height
        return {
            "move_player": lambda p, dx, dy: move_player_with_push(p, dx, dy, blocks, w, h),
            "move_enemy": lambda s, rect, mx, my: move_enemy_with_push(rect, mx, my, blocks, s, w, h),
            "clamp": lambda r: clamp_rect_to_screen(r, w, h),
            "blocks": blocks,
            "width": w,
            "height": h,
            "main_area_rect": pygame.Rect(int(w * 0.25), int(h * 0.25), int(w * 0.5), int(h * 0.5)),
            "rect_offscreen": lambda r: r.right < 0 or r.left > w or r.bottom < 0 or r.top > h,
            "vec_toward": vec_toward,
            "update_friendly_ai": lambda s, dt: update_friendly_ai(
                s.friendly_ai, s.enemies, blocks, dt,
                find_nearest_enemy, vec_toward,
                lambda rect, mx, my, bl: move_enemy_with_push(rect, mx, my, bl, s, w, h),
                lambda f, t: spawn_friendly_projectile(f, t, s.friendly_projectiles, vec_toward, ctx.telemetry_client, s.run_time),
                state=s,
                player_rect=getattr(s, "player_rect", None),
                spawn_ally_missile_func=lambda f, t, st: spawn_ally_missile(f, t, st),
            ),
            "kill_enemy": lambda e, s: kill_enemy(e, s, w, h),
            "destructible_blocks": destructible_blocks,
            "moveable_destructible_blocks": moveable_destructible_blocks,
            "giant_blocks": giant_blocks,
            "super_giant_blocks": super_giant_blocks,
            "trapezoid_blocks": trapezoid_blocks,
            "triangle_blocks": triangle_blocks,
            "hazard_obstacles": hazard_obstacles,
            "moving_health_zone": moving_health_zone,
            "teleporter_pads": teleporter_pads,
            "check_point_in_hazard": check_point_in_hazard,
            "line_rect_intersection": line_rect_intersection,
            "testing_mode": ctx.testing_mode,
            "invulnerability_mode": ctx.invulnerability_mode,
            "reset_after_death": lambda s: reset_after_death(s, w, h),
            "create_pickup_collection_effect": create_pickup_collection_effect,
            "apply_pickup_effect": lambda pt, s: apply_pickup_effect(pt, s, ctx),
            "enemy_projectile_size": enemy_projectile_size,
            "enemy_projectiles_color": enemy_projectiles_color,
            "missile_damage": missile_damage,
            "find_nearest_threat": find_nearest_threat,
            "spawn_enemy_projectile": lambda e, s: spawn_enemy_projectile(e, s, ctx.telemetry_client, ctx.telemetry_enabled),
            "spawn_enemy_projectile_predictive": spawn_enemy_projectile_predictive,
            "difficulty": ctx.difficulty,
            "random_spawn_position": random_spawn_position,
            "telemetry": ctx.telemetry_client,
            "telemetry_enabled": ctx.telemetry_enabled,
            "overshield_recharge_cooldown": overshield_recharge_cooldown,
            "ally_drop_cooldown": ally_drop_cooldown,
        }
    game_state.level_context = _make_level_context()

    # ----------------------------
    # Start run + log initial spawns
    # ----------------------------
    game_state.run_id = None  # Will be set when game starts
    # Don't start wave automatically - wait for menu selection

    # ----------------------------
    # Main loop with safe shutdown
    # ----------------------------
    # Initialize high scores database
    init_high_scores_db()

    # Main loop with safe shutdown
    running = True
    FPS = 60
    
    try:
        while running:
            dt = ctx.clock.tick(FPS) / 1000.0  # Delta time in seconds
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

            # Context for screen handlers (shared by event and render)
            screen_ctx = {"WIDTH": ctx.width, "HEIGHT": ctx.height, "font": ctx.font, "big_font": ctx.big_font, "small_font": ctx.small_font, "get_high_scores": get_high_scores, "save_high_score": save_high_score, "difficulty": ctx.difficulty}

            # Event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            handled_by_screen = False
            if running and state in (STATE_PAUSED, STATE_HIGH_SCORES, STATE_NAME_INPUT):
                h = SCREEN_HANDLERS.get(state)
                if h and h.get("handle_events"):
                    result = h["handle_events"](events, game_state, screen_ctx)
                    if result.get("quit"):
                        running = False
                    if result.get("restart") or result.get("restart_to_wave1") or result.get("replay"):
                        game_state.enemies.clear()
                        game_state.player_bullets.clear()
                        game_state.enemy_projectiles.clear()
                        game_state.friendly_projectiles.clear()
                        game_state.friendly_ai.clear()
                        game_state.grenade_explosions.clear()
                        game_state.missiles.clear()
                        game_state.enemy_laser_beams.clear()
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
                        if result.get("restart"):
                            game_state.menu_section = 0
                        if result.get("restart_to_wave1") or result.get("replay"):
                            game_state.player_rect.center = (ctx.width // 2, ctx.height // 2)
                            state = STATE_PLAYING
                            spawn_system_start_wave(1, game_state)
                    if state == STATE_PAUSED:
                        pause_selected = game_state.pause_selected
                    if result.get("screen") is not None:
                        state = result["screen"]
                        game_state.current_screen = state
                    handled_by_screen = True

            for event in events:
                if handled_by_screen:
                    continue
                if event.type == pygame.QUIT:
                    running = False
                    continue

                # Handle text input for name input screen
                if state == STATE_NAME_INPUT and event.type == pygame.TEXTINPUT:
                    if len(game_state.player_name_input) < 20:  # Limit name length
                        game_state.player_name_input += event.text
                
                # Ally direction command: right-click during play sends allies toward mouse position
                # Direct allies: default right-click, or key if rebound
                direct_allies_binding = ctx.controls.get("direct_allies", MOUSE_BUTTON_RIGHT)
                if state in (STATE_PLAYING, STATE_ENDURANCE):
                    if direct_allies_binding == MOUSE_BUTTON_RIGHT and event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                        game_state.ally_command_target = (float(event.pos[0]), float(event.pos[1]))
                        game_state.ally_command_timer = 5.0
                    elif direct_allies_binding != MOUSE_BUTTON_RIGHT and event.type == pygame.KEYDOWN and event.key == direct_allies_binding:
                        # Key binding: use current mouse position as target
                        mx, my = pygame.mouse.get_pos()
                        game_state.ally_command_target = (float(mx), float(my))
                        game_state.ally_command_timer = 5.0

                # Controls rebinding: accept right-click for direct_allies
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and state == STATE_CONTROLS and controls_rebinding:
                    action = controls_actions[controls_selected]
                    if action == "direct_allies":
                        ctx.controls[action] = MOUSE_BUTTON_RIGHT
                        save_controls(ctx.controls)
                        controls_rebinding = False

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
                                    ctx.difficulty
                                )
                            state = STATE_HIGH_SCORES
                            game_state.name_input_active = False
                    
                    # ESC key handling
                    if event.key == pygame.K_ESCAPE:
                        if state == STATE_PLAYING or state == STATE_ENDURANCE:
                            previous_game_state = state
                            state = STATE_PAUSED
                            pause_selected = 0
                            game_state.previous_screen = previous_game_state
                            game_state.pause_selected = 0
                            game_state.current_screen = STATE_PAUSED
                        elif state == STATE_PAUSED:
                            state = previous_game_state if previous_game_state else STATE_PLAYING
                        elif state == STATE_CONTINUE:
                            running = False
                        elif state == STATE_CONTROLS:
                            state = STATE_PAUSED
                            game_state.pause_selected = 0
                            game_state.current_screen = STATE_PAUSED
                        elif state == STATE_TITLE:
                            if game_state.title_confirm_quit:
                                game_state.title_confirm_quit = False
                            else:
                                game_state.title_confirm_quit = True
                        elif state == STATE_MENU:
                            if game_state.menu_confirm_quit:
                                game_state.menu_confirm_quit = False
                            else:
                                game_state.menu_confirm_quit = True
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
                                    ctx.difficulty
                                )
                            state = STATE_HIGH_SCORES
                            game_state.name_input_active = False
                    
                    # P key for pause
                    if event.key == pygame.K_p:
                        if state == STATE_PLAYING or state == STATE_ENDURANCE:
                            previous_game_state = state
                            state = STATE_PAUSED
                            pause_selected = 0
                            game_state.previous_screen = previous_game_state
                            game_state.pause_selected = 0
                            game_state.current_screen = STATE_PAUSED
                        elif state == STATE_PAUSED:
                            state = previous_game_state if previous_game_state else STATE_PLAYING
                    
                    # Pause menu navigation (fallback when not using screen handler)
                    if state == STATE_PAUSED:
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            pause_selected = (pause_selected - 1) % len(pause_options)
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            pause_selected = (pause_selected + 1) % len(pause_options)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            choice = pause_options[pause_selected]
                            if choice == "Continue":
                                state = previous_game_state if previous_game_state else STATE_PLAYING
                            elif choice == "Restart (Wave 1)":
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
                                game_state.player_rect.center = (ctx.width // 2, ctx.height // 2)
                                state = STATE_PLAYING
                                spawn_system_start_wave(1, game_state)
                            elif choice == "Exit to main menu":
                                state = STATE_MENU
                            elif choice == "Quit":
                                running = False
                    
                    # Title screen: Enter/Space to start; or quit confirm (Y/Enter = quit, N/ESC = stay)
                    if state == STATE_TITLE:
                        if game_state.title_confirm_quit:
                            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_y):
                                running = False
                            elif event.key == pygame.K_n:
                                game_state.title_confirm_quit = False
                        else:
                            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                                state = STATE_MENU
                                game_state.current_screen = STATE_MENU
                    
                    # Menu navigation (and quit confirm when ESC was pressed in options)
                    if state == STATE_MENU:
                        if game_state.menu_confirm_quit:
                            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_y):
                                running = False
                            elif event.key == pygame.K_n:
                                game_state.menu_confirm_quit = False
                        elif menu_section == 0:  # Difficulty selection (first options screen: back arrow = return to title/main menu)
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                difficulty_selected = (difficulty_selected - 1) % len(difficulty_options)
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                difficulty_selected = (difficulty_selected + 1) % len(difficulty_options)
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                state = STATE_TITLE
                                game_state.current_screen = STATE_TITLE
                                game_state.menu_confirm_quit = False
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                ctx.difficulty = difficulty_options[difficulty_selected]
                                menu_section = 1.5  # Go to character profile yes/no (aiming mode removed, default mouse)
                        elif menu_section == 1.5:  # Character profile yes/no
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                use_character_profile_selected = (use_character_profile_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                use_character_profile_selected = (use_character_profile_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 0  # Go back to difficulty
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                ctx.profile_enabled = use_character_profile_selected == 1
                                if ctx.profile_enabled:
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
                                ctx.player_class = player_class_options[player_class_selected]
                                menu_section = 3  # Go to options
                        elif menu_section == 3:  # HUD options
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                ui_show_metrics_selected = (ui_show_metrics_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                ui_show_metrics_selected = (ui_show_metrics_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                if ctx.profile_enabled:
                                    menu_section = 7 if character_profile_selected == 0 else 6
                                else:
                                    menu_section = 1.5
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                ctx.ui_show_metrics = ui_show_metrics_selected == 0
                                ctx.ui_show_hud = ctx.ui_show_metrics
                                menu_section = 3.5  # Go to telemetry options
                        elif menu_section == 3.5:  # Telemetry options
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                ui_telemetry_enabled_selected = (ui_telemetry_enabled_selected - 1) % 2
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                ui_telemetry_enabled_selected = (ui_telemetry_enabled_selected + 1) % 2
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 3  # Go back to HUD options
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                ctx.telemetry_enabled = ui_telemetry_enabled_selected == 0
                                if ctx.testing_mode:
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
                                if game_state.current_weapon_mode == "laser" and selected_weapon != "laser":
                                    game_state.laser_beams.clear()
                                game_state.current_weapon_mode = selected_weapon
                                beam_selection_pattern = selected_weapon
                                if ctx.testing_mode:
                                    menu_section = 4.5  # Go to testing options
                                else:
                                    menu_section = 5  # Go to start
                        elif menu_section == 4.5:  # Testing options (testing mode only)
                            if event.key == pygame.K_UP or event.key == pygame.K_w:
                                ctx.invulnerability_mode = not ctx.invulnerability_mode
                            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                                ctx.invulnerability_mode = not ctx.invulnerability_mode
                            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                menu_section = 4  # Go back to weapon selection
                            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                menu_section = 5  # Go to start
                        elif menu_section == 5:  # Start game
                            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                                if ctx.testing_mode:
                                    menu_section = 4.5
                                else:
                                    menu_section = 3.5  # Go back to telemetry options
                            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                                # Initialize game
                                ctx.telemetry_enabled = (ui_telemetry_enabled_selected == 0)
                                if ctx.telemetry_enabled:
                                    ctx.telemetry_client = Telemetry(db_path="game_telemetry.db", flush_interval_s=0.5, max_buffer=700)
                                else:
                                    ctx.telemetry_client = NoOpTelemetry()
                                
                                # Apply class stats
                                stats = player_class_stats[ctx.player_class]
                                game_state.player_max_hp = int(1000 * stats["hp_mult"] * 0.75)  # Reduced by 0.75x
                                game_state.player_hp = game_state.player_max_hp
                                game_state.player_speed = int(300 * stats["speed_mult"])
                                game_state.player_bullet_damage = int(20 * stats["damage_mult"])
                                game_state.player_shoot_cooldown = 0.12 / stats["firerate_mult"]
                                
                                # Set state and persist to game_state so "state = game_state.current_screen" in the play block doesn't overwrite with MENU
                                if endurance_mode_selected == 1:
                                    state = STATE_ENDURANCE
                                    previous_game_state = STATE_ENDURANCE
                                    game_state.lives = 999
                                else:
                                    state = STATE_PLAYING
                                    previous_game_state = STATE_PLAYING
                                game_state.current_screen = state
                                game_state.previous_screen = previous_game_state
                                # So spawn_system and others see current app config
                                if game_state.level_context:
                                    game_state.level_context["telemetry"] = ctx.telemetry_client
                                    game_state.level_context["telemetry_enabled"] = ctx.telemetry_enabled
                                    game_state.level_context["difficulty"] = ctx.difficulty
                                    game_state.level_context["testing_mode"] = ctx.testing_mode
                                    game_state.level_context["invulnerability_mode"] = ctx.invulnerability_mode

                                game_state.run_id = ctx.telemetry_client.start_run(game_state.run_started_at, game_state.player_max_hp) if ctx.telemetry_enabled else None
                                game_state.wave_reset_log.clear()
                                game_state.wave_start_reason = "menu_start"
                                spawn_system_start_wave(game_state.wave_number, game_state)
                    
                    # Controls rebinding
                    if state == STATE_CONTROLS and controls_rebinding:
                        if event.key != pygame.K_ESCAPE:
                            action = controls_actions[controls_selected]
                            ctx.controls[action] = event.key
                            save_controls(ctx.controls)
                            controls_rebinding = False
                        else:
                            controls_rebinding = False
                    
                    # Shield activation (Left Alt) - only activates when recharge bar is full
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_LALT:
                        # Shield can only be activated when recharge bar is full (shield_recharge_timer >= shield_recharge_cooldown)
                        if game_state.shield_recharge_timer >= game_state.shield_recharge_cooldown and not game_state.shield_active:
                            game_state.shield_active = True
                            game_state.shield_duration_remaining = shield_duration
                            game_state.shield_cooldown = shield_recharge_cooldown  # From constants (halved for alt-r)
                            game_state.shield_recharge_cooldown = game_state.shield_cooldown
                            game_state.shield_recharge_timer = 0.0  # Reset recharge timer when shield activates
                            game_state.shield_cooldown_remaining = 0.0
                    
                    # Overshield activation (Tab)
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == pygame.K_TAB:
                        if game_state.overshield_recharge_timer >= overshield_recharge_cooldown:
                            game_state.overshield = game_state.player_max_hp
                            game_state.armor_drain_timer = 0.0  # First 50 HP drains after 0.5s
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
                    
                    # Ally drop (Q key) — multiple allies; do not remove previous
                    if (state == STATE_PLAYING or state == STATE_ENDURANCE) and event.key == ctx.controls.get("ally_drop", pygame.K_q):
                        if game_state.ally_drop_timer >= ally_drop_cooldown:
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
                                ally_hp = max(1, game_state.player_max_hp // 2)
                                friendly["hp"] = ally_hp
                                friendly["max_hp"] = ally_hp
                                friendly["rect"].center = (int(spawn_pos.x), int(spawn_pos.y))
                                friendly["is_dropped_ally"] = True  # Mark so enemies can prioritise it; still updated by same update_friendly_ai
                                game_state.friendly_ai.append(friendly)
                                game_state.dropped_ally = friendly
                            
                            game_state.ally_drop_timer = 0.0
                    
                    # Weapon switching (keys 1-6)
                    if state == STATE_PLAYING or state == STATE_ENDURANCE:
                        if event.key == pygame.K_1 and "basic" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            game_state.current_weapon_mode = "basic"
                        elif event.key == pygame.K_2 and "triple" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "laser":
                                game_state.laser_beams.clear()
                            game_state.current_weapon_mode = "triple"
                        elif event.key == pygame.K_3 and "giant" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "laser":
                                game_state.laser_beams.clear()
                            game_state.current_weapon_mode = "giant"
                        elif event.key == pygame.K_4 and "laser" in game_state.unlocked_weapons:
                            game_state.previous_weapon_mode = game_state.current_weapon_mode
                            if game_state.previous_weapon_mode == "laser":
                                game_state.laser_beams.clear()
                            game_state.current_weapon_mode = "laser"

            # Game state updates (only when playing)
            if state == STATE_PLAYING or state == STATE_ENDURANCE:
                # Update timers
                game_state.player_time_since_shot += dt
                game_state.laser_time_since_shot += dt
                game_state.grenade_time_since_used += dt
                game_state.missile_time_since_used += dt
                game_state.jump_cooldown_timer += dt
                game_state.jump_timer += dt
                game_state.overshield_recharge_timer += dt
                # Armor drains 50 HP every 0.5s; drain stops when armor hits zero; bar hidden when 0
                if game_state.overshield > 0:
                    game_state.armor_drain_timer = getattr(game_state, "armor_drain_timer", 0.0) + dt
                    while game_state.armor_drain_timer >= 0.5 and game_state.overshield > 0:
                        game_state.overshield = max(0, game_state.overshield - 50)
                        game_state.armor_drain_timer -= 0.5
                else:
                    game_state.armor_drain_timer = 0.0
                # Only decrement shield duration when shield is active
                if game_state.shield_active:
                    game_state.shield_duration_remaining -= dt
                game_state.shield_cooldown_remaining -= dt
                game_state.shield_recharge_timer += dt
                game_state.ally_drop_timer += dt
                game_state.ally_command_timer = max(0.0, getattr(game_state, "ally_command_timer", 0.0) - dt)
                game_state.teleporter_cooldown = max(0.0, getattr(game_state, "teleporter_cooldown", 0.0) - dt)
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
                update_hazard_obstacles(dt, hazard_obstacles, game_state.current_level, ctx.width, ctx.height)
                
                # Unified entity update (Enemy/Friendly call no-op update by default; hook for future logic)
                for entity in game_state.enemies:
                    if hasattr(entity, "update"):
                        entity.update(dt, game_state)
                for entity in game_state.friendly_ai:
                    if hasattr(entity, "update"):
                        entity.update(dt, game_state)
                
                # Hazard–enemy collision is in collision_system
                
                # Update enemy defeat message timers
                for msg in game_state.enemy_defeat_messages[:]:
                    msg["timer"] -= dt
                    if msg["timer"] <= 0:
                        game_state.enemy_defeat_messages.remove(msg)
                
                # Update pickup effects
                update_pickup_effects(dt, game_state)
                
                # Player movement input (movement_system applies it)
                keys = pygame.key.get_pressed()
                move_x = 0
                move_y = 0
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
                is_boosting = keys[controls.get("boost", pygame.K_LSHIFT)] and game_state.boost_meter > 0
                is_slowing = keys[controls.get("slow", pygame.K_LCTRL)]
                if is_boosting:
                    game_state.boost_meter = max(0, game_state.boost_meter - boost_drain_per_s * dt)
                    game_state.speed_mult = boost_speed_mult
                    game_state.previous_boost_state = True
                else:
                    game_state.boost_meter = min(boost_meter_max, game_state.boost_meter + boost_regen_per_s * dt)
                    game_state.speed_mult = 1.0
                    game_state.previous_boost_state = False
                if is_slowing:
                    game_state.speed_mult *= slow_speed_mult
                    game_state.previous_slow_state = True
                else:
                    game_state.previous_slow_state = False
                game_state.move_input_x = move_x
                game_state.move_input_y = move_y
                movement_update(game_state, dt)
                collision_update(game_state, dt)
                spawn_update(game_state, dt)
                ai_update(game_state, dt)
                state = game_state.current_screen  # pick up transitions (e.g. game over -> name input, victory)

                # Apply fire rate buff
                effective_fire_rate = game_state.player_shoot_cooldown
                if game_state.fire_rate_buff_t < fire_rate_buff_duration:
                    effective_fire_rate *= fire_rate_mult
                
                # Player shooting
                mouse_buttons = pygame.mouse.get_pressed()
                shoot_input = mouse_buttons[0] or (ctx.aiming_mode == AIM_ARROWS and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]))
                
                if shoot_input and game_state.player_time_since_shot >= effective_fire_rate:
                    spawn_player_bullet_and_log(game_state, ctx)
                    game_state.player_time_since_shot = 0.0
                
                # Laser beam weapon
                if game_state.current_weapon_mode == "laser" and game_state.laser_time_since_shot >= laser_cooldown:
                    if ctx.aiming_mode == AIM_ARROWS:
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
                
                # Laser beam collisions are in collision_system
                # Enemy AI (targeting, queen shield/missiles, suicide, reflector, shooting) is in ai_system.update()
                
                # Bullet/projectile, pickups, health zone, friendly projs, grenades, missiles: collision_system
                # Wave timers and next-wave start (including victory) are in spawn_system.update()
            
            # Rendering
            theme = level_themes.get(game_state.current_level, level_themes[1])
            if state not in (STATE_PLAYING, STATE_ENDURANCE):
                ctx.screen.fill(theme["bg_color"])

            if state == STATE_TITLE:
                # Title screen: same green as options menus (theme already filled above); or "Are you sure?" when ESC pressed
                if game_state.title_confirm_quit:
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Are you sure you want to exit?", ctx.height // 2 - 40, color=(220, 220, 220))
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "ENTER or Y to quit", ctx.height // 2 + 20, (180, 180, 180))
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "ESC or N to stay", ctx.height // 2 + 60, (180, 180, 180))
                else:
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "GAME", ctx.height // 2 - 80, color=(220, 220, 220), use_big=True)
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Main Menu", ctx.height // 2 - 30, (180, 180, 180))
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Press ENTER or SPACE for options", ctx.height // 2 + 30, (180, 180, 180))
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "ESC to quit", ctx.height // 2 + 70, (180, 180, 180))
            elif state == STATE_MENU:
                # Menu rendering (or same quit-confirm dialog when ESC pressed)
                if game_state.menu_confirm_quit:
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Are you sure you want to exit?", ctx.height // 2 - 40, color=(220, 220, 220))
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "ENTER or Y to quit", ctx.height // 2 + 20, (180, 180, 180))
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "ESC or N to stay", ctx.height // 2 + 60, (180, 180, 180))
                else:
                    draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "MOUSE AIM SHOOTER", ctx.height // 4, use_big=True)
                    y_offset = ctx.height // 2
                    if menu_section == 0:
                        # Difficulty selection (options entry: LEFT = back to main menu)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Options — Select Difficulty:", y_offset - 60)
                        for i, diff in enumerate(difficulty_options):
                            color = (255, 255, 0) if i == difficulty_selected else (200, 200, 200)
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if i == difficulty_selected else '  '} {diff}", y_offset + i * 40, color)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "UP/DOWN to select, RIGHT/ENTER to continue, LEFT to return to main menu", ctx.height - 100, (150, 150, 150))
                    elif menu_section == 1.5:
                        # Character profile yes/no
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use Character Profile?", y_offset - 60)
                        options = ["No", "Yes"]
                        for i, opt in enumerate(options):
                            color = (255, 255, 0) if i == use_character_profile_selected else (200, 200, 200)
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if i == use_character_profile_selected else '  '} {opt}", y_offset + i * 40, color)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", ctx.height - 100, (150, 150, 150))
                    elif menu_section == 2:
                        # Character profile selection
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Character Profile:", y_offset - 60)
                        for i, profile in enumerate(character_profile_options):
                            color = (255, 255, 0) if i == character_profile_selected else (200, 200, 200)
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if i == character_profile_selected else '  '} {profile}", y_offset + i * 40, color)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", ctx.height - 100, (150, 150, 150))
                    elif menu_section == 3:
                        # HUD options
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "HUD Options:", y_offset - 60)
                        options = ["Show Metrics", "Hide Metrics"]
                        for i, opt in enumerate(options):
                            color = (255, 255, 0) if i == ui_show_metrics_selected else (200, 200, 200)
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if i == ui_show_metrics_selected else '  '} {opt}", y_offset + i * 40, color)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", ctx.height - 100, (150, 150, 150))
                    elif menu_section == 3.5:
                        # Telemetry options
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Telemetry:", y_offset - 60)
                        options = ["Enabled", "Disabled"]
                        for i, opt in enumerate(options):
                            color = (255, 255, 0) if i == ui_telemetry_enabled_selected else (200, 200, 200)
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if i == ui_telemetry_enabled_selected else '  '} {opt}", y_offset + i * 40, color)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", ctx.height - 100, (150, 150, 150))
                    elif menu_section == 4:
                        # Beam/weapon selection (if testing mode)
                        if ctx.testing_mode:
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Select Weapon:", y_offset - 60)
                            for i, weapon in enumerate(weapon_selection_options):
                                color = (255, 255, 0) if i == beam_selection_selected else (200, 200, 200)
                                draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if i == beam_selection_selected else '  '} {weapon}", y_offset + i * 30, color)
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", ctx.height - 100, (150, 150, 150))
                        else:
                            menu_section = 5  # Skip to start
                    elif menu_section == 4.5:
                        # Testing options (testing mode only)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Testing Options:", y_offset - 60)
                        invuln_color = (255, 255, 0) if ctx.invulnerability_mode else (200, 200, 200)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if ctx.invulnerability_mode else '  '} Invulnerability: {'ON' if ctx.invulnerability_mode else 'OFF'}", y_offset, invuln_color)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use UP/DOWN to toggle, LEFT to go back, RIGHT/ENTER to start", ctx.height - 100, (150, 150, 150))
                    elif menu_section == 5:
                        # Start game
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Ready to Start!", y_offset)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Press ENTER or SPACE to begin", y_offset + 60, (150, 150, 150))
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Press LEFT to go back", y_offset + 100, (150, 150, 150))
                    elif menu_section == 6:
                        # Custom profile creator
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Custom Profile Creator:", y_offset - 100)
                        for i, stat_name in enumerate(custom_profile_stats_list):
                            stat_key = custom_profile_stats_keys[i]
                            stat_value = custom_profile_stats[stat_key]
                            color = (255, 255, 0) if i == custom_profile_stat_selected else (200, 200, 200)
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if i == custom_profile_stat_selected else '  '} {stat_name}: {stat_value:.1f}x", y_offset + i * 35, color)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use UP/DOWN to select stat, LEFT/RIGHT to adjust, ENTER to continue", ctx.height - 100, (150, 150, 150))
                    elif menu_section == 7:
                        # Class selection
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Select Class:", y_offset - 60)
                        for i, cls in enumerate(player_class_options):
                            color = (255, 255, 0) if i == player_class_selected else (200, 200, 200)
                            draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, f"{'->' if i == player_class_selected else '  '} {cls}", y_offset + i * 40, color)
                        draw_centered_text(ctx.screen, ctx.font, ctx.big_font, ctx.width, "Use UP/DOWN to select, LEFT to go back, RIGHT/ENTER to continue", ctx.height - 100, (150, 150, 150))
            elif state == STATE_PLAYING or state == STATE_ENDURANCE:
                gameplay_ctx = {
                    "level_themes": level_themes,
                    "trapezoid_blocks": trapezoid_blocks,
                    "triangle_blocks": triangle_blocks,
                    "destructible_blocks": destructible_blocks,
                    "moveable_destructible_blocks": moveable_destructible_blocks,
                    "giant_blocks": giant_blocks,
                    "super_giant_blocks": super_giant_blocks,
                    "hazard_obstacles": hazard_obstacles,
                    "moving_health_zone": moving_health_zone,
                    "teleporter_pads": teleporter_pads,
                    "small_font": ctx.small_font,
                    "weapon_names": WEAPON_NAMES,
                    "WIDTH": ctx.width,
                    "HEIGHT": ctx.height,
                    "font": ctx.font,
                    "big_font": ctx.big_font,
                    "ui_show_hud": ctx.ui_show_hud,
                    "ui_show_metrics": ctx.ui_show_metrics,
                    "ui_show_health_bars": ctx.ui_show_health_bars,
                    "overshield_max": overshield_max,
                    "grenade_cooldown": grenade_cooldown,
                    "missile_cooldown": missile_cooldown,
                    "ally_drop_cooldown": ally_drop_cooldown,
                    "overshield_recharge_cooldown": overshield_recharge_cooldown,
                    "shield_duration": shield_duration,
                    "aiming_mode": ctx.aiming_mode,
                    "current_state": state,
                }
                gameplay_render(ctx, game_state, gameplay_ctx)
                
                # Clean up expired UI tokens (state updates; timers decremented in update loop)
                for dmg_num in game_state.damage_numbers[:]:
                    if dmg_num["timer"] <= 0:
                        game_state.damage_numbers.remove(dmg_num)
                for msg in game_state.weapon_pickup_messages[:]:
                    if msg["timer"] <= 0:
                        game_state.weapon_pickup_messages.remove(msg)
            elif state in (STATE_PAUSED, STATE_HIGH_SCORES, STATE_NAME_INPUT) and state in SCREEN_HANDLERS and SCREEN_HANDLERS[state].get("render"):
                SCREEN_HANDLERS[state]["render"](ctx, game_state, screen_ctx)
            elif state == STATE_GAME_OVER:
                # Game over screen
                # (Game over rendering would go here)
                pass
            elif state == STATE_VICTORY:
                # Victory screen
                # (Victory rendering would go here)
                pass
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
        if ctx.telemetry_enabled and ctx.telemetry_client:
            ctx.telemetry_client.end_run(
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
            ctx.telemetry_client.close()
            print(f"Saved run_id={game_state.run_id} to game_telemetry.db")
        pygame.quit()


# Controls will be initialized in main() after pygame.init()
# Using a placeholder dict to avoid calling pygame.key.key_code() before pygame.init()
controls = {}

# Telemetry and run_started_at are stored in AppContext (built in main()).

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
beam_selection_selected = 3  # 0 = laser, 1 = triple, 2 = giant, 3 = basic (default)
beam_selection_pattern = "basic"  # Default weapon pattern

# Level system - 3 levels, each with 3 waves (boss on wave 3)
current_level = 1
max_level = 3
wave_in_level = 1  # Track which wave within current level (1, 2, or 3)
# level_themes is now imported from constants.py

# Difficulty / aiming / class: applied values live in AppContext (ctx); only menu selection indices here.
difficulty_selected = 1  # 0 = Easy, 1 = Normal, 2 = Hard
aiming_mode_selected = 0  # 0 = Mouse, 1 = Arrows
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
shield_cooldown = shield_recharge_cooldown  # From constants (5.0, half of original 10)
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
# "basic" = normal bullets, "triple" = triple shot, "giant" = giant bullets, "laser" = laser beam
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

# hazard_obstacles imported from hazards.py

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

# Teleporter pads: one per half of map, nothing overlaps except player (like health zone). ~1.5x player (42).
TELEPORTER_SIZE = 42  # 1.5 * player size (28)
teleporter_pad_a = {"rect": pygame.Rect(0, 0, TELEPORTER_SIZE, TELEPORTER_SIZE), "linked_rect": None}
teleporter_pad_b = {"rect": pygame.Rect(0, 0, TELEPORTER_SIZE, TELEPORTER_SIZE), "linked_rect": None}
teleporter_pad_a["linked_rect"] = teleporter_pad_b["rect"]
teleporter_pad_b["linked_rect"] = teleporter_pad_a["rect"]
teleporter_pads = [teleporter_pad_a, teleporter_pad_b]
for idx, pad in enumerate(teleporter_pads):
    for _ in range(max_health_zone_attempts):
        overlaps = False
        if idx == 0:
            # Top-left quadrant
            pad["rect"].center = (random.randint(80, WIDTH // 2 - 60), random.randint(80, HEIGHT // 2 - 60))
        else:
            # Bottom-right quadrant
            pad["rect"].center = (random.randint(WIDTH // 2 + 60, WIDTH - 80), random.randint(HEIGHT // 2 + 60, HEIGHT - 80))
        for block_list in [destructible_blocks, moveable_destructible_blocks, giant_blocks, super_giant_blocks]:
            for block in block_list:
                if pad["rect"].colliderect(block["rect"]):
                    overlaps = True
                    break
            if overlaps:
                break
        if not overlaps:
            for tb in trapezoid_blocks:
                if pad["rect"].colliderect(tb.get("bounding_rect", tb.get("rect"))):
                    overlaps = True
                    break
        if not overlaps:
            for tr in triangle_blocks:
                if pad["rect"].colliderect(tr.get("bounding_rect", tr.get("rect"))):
                    overlaps = True
                    break
        if not overlaps and not pad["rect"].colliderect(moving_health_zone["rect"]):
            other = teleporter_pads[1 - idx]
            if not pad["rect"].colliderect(other["rect"]):
                break

# ----------------------------
# Enemy templates are now imported from config_enemies.py
# ----------------------------
enemy_templates = ENEMY_TEMPLATES  # Alias for compatibility

# Boss enemy template is now imported from config_enemies.py
# Note: rect position will be set at runtime in spawn_boss()
# boss_template will be created from BOSS_TEMPLATE.copy() when needed in start_wave()
# We keep a reference here for compatibility, but it will be copied at runtime
boss_template = BOSS_TEMPLATE  # Reference (will be copied when spawning boss)

enemies: list[dict] = []

# ----------------------------
# Friendly AI
# ----------------------------
# Friendly AI templates are now imported from config_enemies.py
friendly_ai_templates = FRIENDLY_AI_TEMPLATES  # Alias for compatibility

friendly_ai: list[dict] = []

# Dropped ally system (distracts enemies)
dropped_ally: dict | None = None  # Single dropped ally that distracts enemies
ally_drop_cooldown = 3.0  # Cooldown between ally drops (seconds)
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
    pygame.K_2: "triple",
    pygame.K_3: "giant",
    pygame.K_4: "laser",
}

# Visual effects for pickups
pickup_particles: list[dict] = []  # particles around pickups
collection_effects: list[dict] = []  # effects when pickups are collected


# ----------------------------
# Helpers (geometry/physics moved to geometry_utils)
# ----------------------------
def move_player_with_push(player_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict], width: int, height: int):
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

    clamp_rect_to_screen(player_rect, width, height)


def _enemy_collides(enemy_rect: pygame.Rect, block_list: list[dict], state: GameState) -> bool:
    """Return True if enemy_rect collides with any solid object."""
    for b in block_list:
        if enemy_rect.colliderect(b["rect"]):
            return True
    for b in destructible_blocks:
        if enemy_rect.colliderect(b["rect"]):
            return True
    for b in moveable_destructible_blocks:
        if enemy_rect.colliderect(b["rect"]):
            return True
    for gb in giant_blocks:
        if enemy_rect.colliderect(gb["rect"]):
            return True
    for sgb in super_giant_blocks:
        if enemy_rect.colliderect(sgb["rect"]):
            return True
    for tb in trapezoid_blocks:
        if enemy_rect.colliderect(tb.get("bounding_rect", tb.get("rect"))):
            return True
    for tr in triangle_blocks:
        if enemy_rect.colliderect(tr.get("bounding_rect", tr.get("rect"))):
            return True
    for pickup in state.pickups:
        if enemy_rect.colliderect(pickup["rect"]):
            return True
    if enemy_rect.colliderect(moving_health_zone["rect"]):
        return True
    if state.player_rect is not None and enemy_rect.colliderect(state.player_rect):
        return True
    for f in state.friendly_ai:
        if f.get("hp", 1) > 0 and enemy_rect.colliderect(f["rect"]):
            return True
    for other_e in state.enemies:
        if other_e["rect"] is not enemy_rect and enemy_rect.colliderect(other_e["rect"]):
            return True
    return False


def move_enemy_with_push(enemy_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict], state: GameState, width: int, height: int):
    """Enemy movement - enemies cannot go through objects and must navigate around them.
    When stuck (both axes blocked), tries sliding along walls to avoid getting stuck."""
    start_x, start_y = enemy_rect.x, enemy_rect.y

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
        
        # Check teleporter pads (nothing overlaps except player)
        if not collision:
            for pad in teleporter_pads:
                if enemy_rect.colliderect(pad["rect"]):
                    collision = True
                    break
        
        # Check player
        if not collision and state.player_rect is not None:
            if enemy_rect.colliderect(state.player_rect):
                collision = True

        # Check friendly AI (skip self when rect is a friendly's own rect so allies can move)
        if not collision:
            for f in state.friendly_ai:
                if f["rect"] is enemy_rect:
                    continue
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

    # If stuck (no movement), try sliding along walls to avoid getting stuck
    if enemy_rect.x == start_x and enemy_rect.y == start_y and (move_x != 0 or move_y != 0):
        step = max(1, (abs(move_x) + abs(move_y)) // 2)
        for slide_dx, slide_dy in [(move_y, move_x), (-move_y, -move_x), (move_y, -move_x), (-move_y, move_x)]:
            if slide_dx == 0 and slide_dy == 0:
                continue
            # Scale to same magnitude as step
            try:
                scale = step / (slide_dx * slide_dx + slide_dy * slide_dy) ** 0.5
            except ZeroDivisionError:
                continue
            sx = int(slide_dx * scale) if slide_dx else 0
            sy = int(slide_dy * scale) if slide_dy else 0
            if sx == 0 and sy == 0:
                continue
            enemy_rect.x += sx
            enemy_rect.y += sy
            if not _enemy_collides(enemy_rect, block_list, state):
                break
            enemy_rect.x -= sx
            enemy_rect.y -= sy

    clamp_rect_to_screen(enemy_rect, width, height)


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
        # Prevent spawning on teleporter pads (nothing overlaps except player)
        if any(candidate.colliderect(pad["rect"]) for pad in teleporter_pads):
            continue
        return candidate
    # fallback: top-left corner inside bounds
    return pygame.Rect(max(0, WIDTH // 2 - w), max(0, HEIGHT // 2 - h), w, h)


# Wave start and wave/boss/difficulty logic live in systems.spawn_system (start_wave, update)


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


def spawn_weapon_in_center(weapon_type: str, state: GameState, width: int, height: int):
    """Spawn a weapon pickup in the center of the screen (level completion reward)."""
    # Do not spawn basic beam as a pickup
    if weapon_type == "basic":
        return
    # Weapon colors are now imported from config_weapons.py
    weapon_pickup_size = (80, 80)  # Bigger for level completion rewards (2x from 40x40)
    weapon_pickup_rect = pygame.Rect(
        width // 2 - weapon_pickup_size[0] // 2,
        height // 2 - weapon_pickup_size[1] // 2,
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
        "heavy": "triple",
        "baka": "triple",
        "neko neko desu": "giant",
        "BIG NEKU": "giant",
        "bouncer": "triple",
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
            "triple": (100, 200, 255),
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


def spawn_player_bullet_and_log(state: GameState, ctx: AppContext):
    if state.player_rect is None:
        return
    # Determine aiming direction based on aiming mode
    if ctx.aiming_mode == AIM_ARROWS:
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

    if ctx.telemetry_enabled and ctx.telemetry_client:
        ctx.telemetry_client.log_shot(
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
        ctx.telemetry_client.log_bullet_metadata(
            BulletMetadataEvent(
                t=state.run_time,
                bullet_type="player",
                shape=shape,
                color_r=player_bullets_color[0],
                color_g=player_bullets_color[1],
                color_b=player_bullets_color[2],
            )
        )


def spawn_enemy_projectile(enemy: dict, state: GameState, telemetry_client=None, telemetry_enabled: bool = False):
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
    
    proj_damage = enemy.get("flame_damage", enemy.get("damage", 10))
    state.enemy_projectiles.append({
        "rect": r,
        "vel": d * enemy["projectile_speed"],
        "enemy_type": enemy["type"],
        "color": proj_color,
        "shape": proj_shape,
        "bounces": 10 if bounces else 0,
        "damage": proj_damage,
    })
    
    # Log enemy projectile metadata
    if telemetry_enabled and telemetry_client:
        telemetry_client.log_bullet_metadata(
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


def calculate_kill_score(wave_num: int, run_time: float) -> int:
    """Calculate score for killing an enemy."""
    return SCORE_BASE_POINTS + (wave_num * SCORE_WAVE_MULTIPLIER) + int(run_time * SCORE_TIME_MULTIPLIER)


def spawn_ally_missile(friendly: dict, target_enemy: dict, state: GameState) -> None:
    """Spawn a 3-shot burst of seeking missiles from an ally (e.g. striker) toward target_enemy."""
    burst = friendly.get("missile_burst_count", 3)
    damage = friendly.get("missile_damage", 300)
    radius = friendly.get("missile_explosion_radius", 80)
    speed_val = 500
    burst_offsets = [(-10, -10), (0, -15), (10, -10)]
    for i in range(burst):
        ox, oy = burst_offsets[i % len(burst_offsets)]
        cx, cy = friendly["rect"].centerx, friendly["rect"].centery
        r = pygame.Rect(cx - 8 + ox, cy - 8 + oy, 16, 16)
        state.missiles.append({
            "rect": r,
            "vel": pygame.Vector2(0, 0),
            "target_enemy": target_enemy,
            "speed": speed_val,
            "damage": damage,
            "explosion_radius": radius,
        })


def kill_enemy(enemy: dict, state: GameState, width: int, height: int) -> None:
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
                spawn_weapon_in_center(weapon_to_unlock, state, width, height)
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


def apply_pickup_effect(pickup_type: str, state: GameState, ctx: AppContext):
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
        if state.previous_weapon_mode == "laser":
            state.laser_beams.clear()
        state.current_weapon_mode = "giant"
        # Log weapon switch from pickup
        if state.previous_weapon_mode != state.current_weapon_mode:
            if ctx.telemetry_enabled and ctx.telemetry_client and state.player_rect:
                ctx.telemetry_client.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=state.player_rect.centerx,
                    y=state.player_rect.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type in ["triple_shot", "triple"]:
        state.unlocked_weapons.add("triple")
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
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
            if ctx.telemetry_enabled and ctx.telemetry_client and state.player_rect:
                ctx.telemetry_client.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=state.player_rect.centerx,
                    y=state.player_rect.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type == "laser":
        state.unlocked_weapons.add("laser")
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
        state.current_weapon_mode = "laser"
        # Weapon names and colors are now imported from config_weapons.py
        state.weapon_pickup_messages.append({
            "weapon_name": WEAPON_NAMES.get("laser", "LASER BEAM"),
            "timer": 3.0,
            "color": WEAPON_DISPLAY_COLORS.get("laser", (255, 255, 255))
        })
        if state.previous_weapon_mode != state.current_weapon_mode:
            if ctx.telemetry_enabled and ctx.telemetry_client and state.player_rect:
                ctx.telemetry_client.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=state.player_rect.centerx,
                    y=state.player_rect.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type == "basic":
        state.unlocked_weapons.add("basic")  # Should already be unlocked, but ensure it
        state.previous_weapon_mode = state.current_weapon_mode
        # Clear beams when switching away from beam weapons
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
            if ctx.telemetry_enabled and ctx.telemetry_client and state.player_rect:
                ctx.telemetry_client.log_player_action(PlayerActionEvent(
                    t=state.run_time,
                    action_type="weapon_switch",
                    x=state.player_rect.centerx,
                    y=state.player_rect.centery,
                    duration=None,
                    success=True
                ))
    elif pickup_type == "overshield":
        state.overshield = min(overshield_max, state.overshield + 25)


# render_hud_text is now imported from rendering.py


def reset_after_death(state: GameState, width: int, height: int):
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
    # Keep map as-is on respawn: do not reposition moving_health_zone or hazard_obstacles
    state.overshield = 0  # Reset overshield
    state.armor_drain_timer = 0.0
    state.player_time_since_shot = 999.0
    state.laser_time_since_shot = 999.0
    state.wave_beam_time_since_shot = 999.0
    state.wave_beam_pattern_index = 0
    state.pos_timer = 0.0
    # Keep wave/level and weapons on respawn so the map does not reset
    state.previous_boost_state = False
    state.previous_slow_state = False
    state.player_current_zones = set()
    state.jump_cooldown_timer = 0.0
    state.jump_timer = 0.0
    state.is_jumping = False
    state.jump_velocity = pygame.Vector2(0, 0)
    state.laser_beams.clear()
    state.enemy_laser_beams.clear()
    state.wave_beams.clear()
    # Keep hazard obstacles as-is on respawn (map no longer resets)
    # Reset shield
    state.shield_active = False
    state.shield_duration_remaining = 0.0
    state.shield_cooldown_remaining = 0.0

    # Respawn at death position: do not move player_rect (player stays where they died).
    # Optionally keep on-screen if they died in a weird spot:
    player = state.player_rect
    if player is not None:
        clamp_rect_to_screen(player, width, height)

    state.player_bullets.clear()
    state.enemy_projectiles.clear()
    state.friendly_projectiles.clear()
    # Do not clear friendly_ai or call start_wave: keep current wave and enemies.
    # Respawn = player at death position (unchanged), projectiles/explosions cleared; enemies and wave continue.


if __name__ == "__main__":
    main()
