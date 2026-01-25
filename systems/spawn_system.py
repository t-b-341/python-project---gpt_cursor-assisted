"""Enemy spawning, wave updates, spawner minions, and difficulty scaling.

All spawn/wave/boss logic runs here. Game passes callables and runtime data via state.level_context.
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING

import pygame

from config_enemies import (
    BOSS_TEMPLATE,
    BASE_ENEMIES_PER_WAVE,
    MAX_ENEMIES_PER_WAVE,
    ENEMY_SPAWN_MULTIPLIER,
    ENEMY_FIRE_RATE_MULTIPLIER,
    ENEMY_SPEED_SCALE_MULTIPLIER,
    ENEMY_TEMPLATES,
)
from constants import ENEMY_COLOR, STATE_VICTORY, difficulty_multipliers
from enemies import log_enemy_spawns, make_enemy_from_template
from entities import Enemy
from telemetry.events import WaveEnemyTypeEvent, WaveEvent

if TYPE_CHECKING:
    from state import GameState


def update(state: "GameState", dt: float) -> None:
    """Spawn enemies, advance waves, handle spawner minions. Called each gameplay frame."""
    ctx = getattr(state, "level_context", None)
    if ctx is None:
        return

    _handle_spawner_enemies(state, dt, ctx)
    _update_wave_timers(state, dt, ctx)


def start_wave(wave_num: int, state) -> None:
    """Start a new wave (boss or regular). Called from menu "Start game" and from wave timer.
    Requires state.level_context to be set. Set state.wave_start_reason before calling to log it."""
    ctx = getattr(state, "level_context", None)
    if ctx is None:
        _log_wave_reset(state, "start_wave_no_ctx", wave_num, 0)
        return
    if not getattr(state, "wave_start_reason", ""):
        state.wave_start_reason = "start_wave_call"
    _start_wave(wave_num, state, ctx)


def _log_wave_reset(state, trigger: str, wave_num: int, enemies_before: int) -> None:
    """Append to wave_reset_log and print so we can trace spurious resets."""
    entry = {
        "run_time": getattr(state, "run_time", 0.0),
        "trigger": trigger,
        "wave_num": wave_num,
        "enemies_before": enemies_before,
    }
    log = getattr(state, "wave_reset_log", None)
    if log is not None:
        log.append(entry)
        # Keep last 20 entries
        while len(log) > 20:
            log.pop(0)
    msg = (
        f"[WAVE-RESET] run_time={entry['run_time']:.1f}s trigger={trigger!r} "
        f"wave_num={wave_num} enemies_before={enemies_before}"
    )
    print(msg)


def _start_wave(wave_num: int, state, ctx: dict) -> None:
    """Spawn a new wave with scaling. Each level has 3 waves; boss on wave 3."""
    enemies_before = len(state.enemies)
    trigger = getattr(state, "wave_start_reason", "unknown")
    _log_wave_reset(state, trigger, wave_num, enemies_before)
    state.wave_start_reason = ""

    state.enemies = []
    state.boss_active = False
    state.wave_damage_taken = 0
    state.side_quests["no_hit_wave"]["active"] = True
    state.side_quests["no_hit_wave"]["completed"] = False

    if state.lives != 999:
        state.lives = 3

    state.current_level = min(state.max_level, (wave_num - 1) // 3 + 1)
    state.wave_in_level = ((wave_num - 1) % 3) + 1

    difficulty = ctx.get("difficulty", "NORMAL")
    diff_mult = difficulty_multipliers.get(difficulty, difficulty_multipliers["NORMAL"])
    w = ctx.get("width", 1920)
    h = ctx.get("height", 1080)
    random_spawn = ctx.get("random_spawn_position")
    telemetry = ctx.get("telemetry")
    telemetry_enabled = ctx.get("telemetry_enabled", False)
    overshield_cooldown = ctx.get("overshield_recharge_cooldown", 45.0)
    ally_cooldown = ctx.get("ally_drop_cooldown", 30.0)

    # Boss on wave 3 of each level
    if state.wave_in_level == 3:
        _spawn_boss_wave(wave_num, state, ctx, diff_mult, w, h, telemetry, telemetry_enabled, overshield_cooldown)
        return

    # Normal waves (1 and 2)
    hp_scale, speed_scale, count, spawned = _spawn_regular_wave(
        wave_num, state, ctx, diff_mult, random_spawn, telemetry, telemetry_enabled
    )

    state.wave_active = True
    state.overshield_recharge_timer = overshield_cooldown
    state.ally_drop_timer = ally_cooldown
    state.shield_recharge_timer = getattr(state, "shield_recharge_cooldown", 10.0)
    state.shield_cooldown_remaining = 0.0

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


def _spawn_boss_wave(
    wave_num: int,
    state,
    ctx: dict,
    diff_mult: dict,
    w: int,
    h: int,
    telemetry,
    telemetry_enabled: bool,
    overshield_cooldown: float,
) -> None:
    """Spawn boss for wave 3 of the level."""
    boss = BOSS_TEMPLATE.copy()
    boss["color"] = ENEMY_COLOR  # All enemies same color
    boss["rect"] = pygame.Rect(w // 2 - 50, h // 2 - 50, 100, 100)
    boss_hp_scale = 1.0 + (state.current_level - 1) * 0.3
    boss["hp"] = min(int(boss["max_hp"] * boss_hp_scale * diff_mult["enemy_hp"] * 1.1 * 10), 3000)
    boss["max_hp"] = boss["hp"]
    boss["shoot_cooldown"] = BOSS_TEMPLATE["shoot_cooldown"] / ENEMY_FIRE_RATE_MULTIPLIER
    boss["speed"] = BOSS_TEMPLATE["speed"] * ENEMY_SPEED_SCALE_MULTIPLIER
    boss["phase"] = 1
    boss["time_since_shot"] = 0.0
    state.enemies.append(Enemy(boss))
    state.boss_active = True

    if telemetry:
        ref = [state.enemies_spawned]
        log_enemy_spawns([state.enemies[-1]], telemetry, state.run_time, ref)
        state.enemies_spawned = ref[0]
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
    state.overshield_recharge_timer = overshield_cooldown


def _spawn_regular_wave(
    wave_num: int,
    state,
    ctx: dict,
    diff_mult: dict,
    random_spawn,
    telemetry,
    telemetry_enabled: bool,
) -> tuple:
    """Spawn regular enemies for waves 1 and 2. Returns (hp_scale, speed_scale, count, spawned_list)."""
    level_mult = 1.0 + (state.current_level - 1) * 0.3
    wave_in_level_mult = 1.0 + (state.wave_in_level - 1) * 0.15
    hp_scale = (1.0 + 0.15 * (wave_num - 1)) * diff_mult["enemy_hp"] * level_mult * wave_in_level_mult
    speed_scale = (1.0 + 0.05 * (wave_num - 1)) * diff_mult["enemy_speed"] * level_mult * wave_in_level_mult
    base_count = BASE_ENEMIES_PER_WAVE + 2 * (wave_num - 1)
    count = min(int(base_count * diff_mult["enemy_spawn"] * ENEMY_SPAWN_MULTIPLIER), MAX_ENEMIES_PER_WAVE)

    spawned = []
    enemy_type_counts = {}
    queen_count = 0
    max_queens_per_wave = 3

    for _ in range(count):
        tmpl = random.choice(ENEMY_TEMPLATES)
        if tmpl.get("type") == "queen" and queen_count >= max_queens_per_wave:
            non_queen = [t for t in ENEMY_TEMPLATES if t.get("type") != "queen"]
            if non_queen:
                tmpl = random.choice(non_queen)
            else:
                continue
        enemy = make_enemy_from_template(tmpl, hp_scale, speed_scale)
        if random_spawn:
            enemy["rect"] = random_spawn((enemy["rect"].w, enemy["rect"].h), state)
        spawned.append(enemy)
        t = enemy["type"]
        enemy_type_counts[t] = enemy_type_counts.get(t, 0) + 1
        if t == "queen":
            queen_count += 1

    state.enemies.extend(spawned)
    if telemetry:
        ref = [state.enemies_spawned]
        log_enemy_spawns(spawned, telemetry, state.run_time, ref)
        state.enemies_spawned = ref[0]
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
    return (hp_scale, speed_scale, count, spawned)


def _handle_spawner_enemies(state, dt: float, ctx: dict) -> None:
    """Let spawner-type enemies spawn minions on cooldown."""
    random_spawn = ctx.get("random_spawn_position")
    telemetry = ctx.get("telemetry")
    telemetry_enabled = ctx.get("telemetry_enabled", False)
    if not random_spawn:
        return

    for enemy in state.enemies:
        if not enemy.get("is_spawner"):
            continue
        time_since_spawn = enemy.get("time_since_spawn", 0.0) + dt
        spawn_cooldown = enemy.get("spawn_cooldown", 5.0)
        spawn_count = enemy.get("spawn_count", 0)
        max_spawns = enemy.get("max_spawns", 3)

        if time_since_spawn >= spawn_cooldown and spawn_count < max_spawns:
            tmpl = random.choice(ENEMY_TEMPLATES)
            while tmpl.get("type") in ["spawner", "FINAL_BOSS"]:
                tmpl = random.choice(ENEMY_TEMPLATES)
            spawned_enemy = make_enemy_from_template(tmpl, 1.0, 1.0)
            spawned_enemy["rect"] = random_spawn((spawned_enemy["rect"].w, spawned_enemy["rect"].h), state)
            spawned_enemy["spawned_by"] = enemy
            state.enemies.append(spawned_enemy)
            enemy["spawn_count"] = spawn_count + 1
            enemy["time_since_spawn"] = 0.0
            if telemetry_enabled and telemetry:
                ref = [state.enemies_spawned]
                log_enemy_spawns([spawned_enemy], telemetry, state.run_time, ref)
                state.enemies_spawned = ref[0]
        else:
            enemy["time_since_spawn"] = time_since_spawn


def _update_wave_timers(state, dt: float, ctx: dict) -> None:
    """When all enemies are dead, run countdown then start next wave or trigger victory."""
    if not state.wave_active or len(state.enemies) != 0:
        return

    state.time_to_next_wave += dt
    if state.time_to_next_wave < 3.0:
        return

    # Perfect wave bonus
    if state.wave_damage_taken == 0 and state.side_quests["no_hit_wave"]["active"]:
        bonus = state.side_quests["no_hit_wave"]["bonus_points"]
        state.score += bonus
        state.side_quests["no_hit_wave"]["completed"] = True
        w = ctx.get("width", 1920)
        h = ctx.get("height", 1080)
        state.damage_numbers.append({
            "x": w // 2,
            "y": h // 2,
            "value": f"PERFECT WAVE! +{bonus}",
            "timer": 3.0,
            "color": (255, 215, 0),
        })

    state.wave_number += 1
    state.wave_in_level += 1
    if state.wave_in_level > 3:
        state.wave_in_level = 1
        state.current_level += 1
        if state.current_level > state.max_level:
            state.current_screen = STATE_VICTORY
            state.wave_active = False
            state.time_to_next_wave = 0.0
            return

    state.wave_start_reason = "wave_timer_all_dead"
    _start_wave(state.wave_number, state, ctx)
    state.time_to_next_wave = 0.0
