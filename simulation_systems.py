"""
Simulation update steps for one fixed timestep. Run in order via SIMULATION_SYSTEMS.
Each function has signature (gs, sim_dt, app_ctx). game.py calls these from _update_simulation.
"""
from __future__ import annotations

import pygame

from constants import jump_duration
from context import AppContext
from game_utils import update_pickup_effects
from hazards import update_hazard_obstacles
from state import GameState
from systems.registry import SIMULATION_SYSTEMS as REGISTRY_SYSTEMS


def _sim_player_and_ability_timers(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    gs.player_time_since_shot += sim_dt
    gs.laser_time_since_shot += sim_dt
    gs.grenade_time_since_used += sim_dt
    gs.missile_time_since_used += sim_dt
    gs.jump_cooldown_timer += sim_dt
    gs.jump_timer += sim_dt
    gs.overshield_recharge_timer += sim_dt
    if gs.overshield > 0:
        gs.armor_drain_timer = getattr(gs, "armor_drain_timer", 0.0) + sim_dt
        while gs.armor_drain_timer >= 0.5 and gs.overshield > 0:
            gs.overshield = max(0, gs.overshield - 50)
            gs.armor_drain_timer -= 0.5
    else:
        gs.armor_drain_timer = 0.0
    if gs.shield_active:
        gs.shield_duration_remaining -= sim_dt
    gs.shield_cooldown_remaining -= sim_dt
    gs.shield_recharge_timer += sim_dt
    gs.ally_drop_timer += sim_dt
    gs.ally_command_timer = max(0.0, getattr(gs, "ally_command_timer", 0.0) - sim_dt)
    gs.teleporter_cooldown = max(0.0, getattr(gs, "teleporter_cooldown", 0.0) - sim_dt)
    gs.fire_rate_buff_t += sim_dt
    gs.pos_timer += sim_dt
    gs.continue_blink_t += sim_dt


def _sim_damage_and_weapon_message_cleanup(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    for dmg_num in gs.damage_numbers[:]:
        dmg_num["timer"] -= sim_dt
        if dmg_num["timer"] <= 0:
            gs.damage_numbers.remove(dmg_num)
    for msg in gs.weapon_pickup_messages[:]:
        msg["timer"] -= sim_dt
        if msg["timer"] <= 0:
            gs.weapon_pickup_messages.remove(msg)


def _sim_shield_and_jump_state(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    if gs.shield_active and gs.shield_duration_remaining <= 0.0:
        gs.shield_active = False
        gs.shield_cooldown_remaining = gs.shield_cooldown
        gs.shield_recharge_timer = 0.0
    if gs.is_jumping:
        gs.jump_timer += sim_dt
        if gs.jump_timer >= jump_duration:
            gs.is_jumping = False
            gs.jump_velocity = pygame.Vector2(0, 0)


def _sim_hazards(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    if gs.level:
        update_hazard_obstacles(sim_dt, gs.level.hazard_obstacles, gs.current_level, app_ctx.width, app_ctx.height)


def _sim_entity_updates(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    for entity in gs.enemies:
        if hasattr(entity, "update"):
            entity.update(sim_dt, gs)
    for entity in gs.friendly_ai:
        if hasattr(entity, "update"):
            entity.update(sim_dt, gs)


def _sim_defeat_messages_cleanup(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    for msg in gs.enemy_defeat_messages[:]:
        msg["timer"] -= sim_dt
        if msg["timer"] <= 0:
            gs.enemy_defeat_messages.remove(msg)


def _sim_pickup_effects(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    update_pickup_effects(sim_dt, gs)


def _sim_registry_systems(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    for system_update in REGISTRY_SYSTEMS:
        system_update(gs, sim_dt)


def _sim_juice_timers(gs: GameState, sim_dt: float, app_ctx: AppContext) -> None:
    gs.screen_damage_flash_timer = max(0.0, gs.screen_damage_flash_timer - sim_dt)
    gs.damage_wobble_timer = max(0.0, getattr(gs, "damage_wobble_timer", 0.0) - sim_dt)
    gs.wave_banner_timer = max(0.0, gs.wave_banner_timer - sim_dt)
    for e in gs.enemies:
        if isinstance(e, dict) and "damage_flash_timer" in e:
            e["damage_flash_timer"] = max(0.0, e["damage_flash_timer"] - sim_dt)


SIMULATION_SYSTEMS = [
    _sim_player_and_ability_timers,
    _sim_damage_and_weapon_message_cleanup,
    _sim_shield_and_jump_state,
    _sim_hazards,
    _sim_entity_updates,
    _sim_defeat_messages_cleanup,
    _sim_pickup_effects,
    _sim_registry_systems,
    _sim_juice_timers,
]
