"""Collision detection and damage: player bullets, enemy projectiles, pickups, hazards, beams, explosives."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

import pygame

from constants import STATE_NAME_INPUT

if TYPE_CHECKING:
    from state import GameState


def update(state: "GameState", dt: float) -> None:
    """Process all collisions and apply damage. Called from gameplay."""
    ctx = getattr(state, "level_context", None)
    if ctx is None:
        return
    player = state.player_rect
    if player is None:
        return

    _handle_hazard_enemy_collisions(state, dt, ctx)
    _handle_laser_beam_collisions(state, dt, ctx)
    _handle_enemy_laser_beam_collisions(state, dt, ctx)
    _handle_dead_enemies(state, ctx)
    _handle_player_bullet_offscreen(state, ctx)
    _handle_player_bullet_enemy_collisions(state, ctx)
    _handle_player_bullet_block_collisions(state, dt, ctx)
    _handle_enemy_projectile_lifetime_offscreen(state, ctx)
    _handle_enemy_projectile_block_collisions(state, ctx)
    _handle_enemy_projectile_player_collisions(state, ctx)
    _handle_enemy_projectile_friendly_collisions(state, ctx)
    _handle_teleporter_player(state, ctx)
    _handle_pickup_player_collisions(state, ctx)
    _handle_health_zone_player_dt(state, dt, ctx)
    _handle_friendly_projectile_offscreen_blocks_enemies(state, ctx)
    _handle_grenade_explosion_damage(state, dt, ctx)
    _handle_missile_collisions(state, ctx)


def _apply_player_damage(state, damage: int, ctx: dict) -> None:
    """Apply damage to player (overshield then HP); trigger death/game-over if needed."""
    if damage <= 0:
        return
    if ctx.get("testing_mode") and ctx.get("invulnerability_mode"):
        return
    if state.overshield > 0:
        damage_to_overshield = min(damage, state.overshield)
        state.overshield = max(0, state.overshield - damage)
        damage = damage - damage_to_overshield
    if damage > 0:
        state.player_hp -= damage
    state.damage_taken += damage
    state.wave_damage_taken += damage
    if state.player_hp <= 0:
        reset = ctx.get("reset_after_death")
        if state.lives > 0 and reset:
            state.lives -= 1
            reset(state)
        else:
            state.final_score_for_high_score = state.score
            state.player_name_input = ""
            state.name_input_active = True
            state.current_screen = STATE_NAME_INPUT


def _handle_hazard_enemy_collisions(state, dt: float, ctx: dict) -> None:
    for hazard in ctx.get("hazard_obstacles", []):
        if not hazard.get("points") or len(hazard["points"]) < 3:
            continue
        hazard_damage = hazard.get("damage", 10)
        check = ctx.get("check_point_in_hazard")
        kill = ctx.get("kill_enemy")
        if not check or not kill:
            continue
        for enemy in state.enemies[:]:
            center = pygame.Vector2(enemy["rect"].center)
            if check(center, hazard["points"], hazard["bounding_rect"]):
                enemy["hp"] -= hazard_damage * dt
                if enemy["hp"] <= 0:
                    kill(enemy, state)


def _handle_laser_beam_collisions(state, dt: float, ctx: dict) -> None:
    line_rect = ctx.get("line_rect_intersection")
    kill = ctx.get("kill_enemy")
    if not line_rect or not kill:
        return
    for beam in state.laser_beams[:]:
        beam["timer"] = beam.get("timer", 0.1) - dt
        if beam["timer"] <= 0:
            state.laser_beams.remove(beam)
            continue
        damage = beam.get("damage", 50) * dt * 60
        for enemy in state.enemies[:]:
            if line_rect(beam["start"], beam["end"], enemy["rect"]):
                enemy["hp"] -= damage
                if enemy["hp"] <= 0:
                    kill(enemy, state)


def _handle_enemy_laser_beam_collisions(state, dt: float, ctx: dict) -> None:
    """Enemy laser beams damage the player. Beams have a deploy phase (deploy_timer) where they
    grow visually but deal no damage; after deploy, they deal damage for timer duration."""
    line_rect = ctx.get("line_rect_intersection")
    player = state.player_rect
    if not line_rect or player is None:
        return
    for beam in list(getattr(state, "enemy_laser_beams", [])):
        deploy_timer = beam.get("deploy_timer", 0.0)
        if deploy_timer > 0:
            beam["deploy_timer"] = deploy_timer - dt
            continue  # No damage during deploy; beam is still drawn as growing in rendering
        beam["timer"] = beam.get("timer", 0.2) - dt
        if beam["timer"] <= 0:
            state.enemy_laser_beams.remove(beam)
            continue
        damage_per_sec = beam.get("damage", 80 * 60)
        if line_rect(beam["start"], beam["end"], player):
            _apply_player_damage(state, int(damage_per_sec * dt), ctx)


def _handle_dead_enemies(state, ctx: dict) -> None:
    kill = ctx.get("kill_enemy")
    if not kill:
        return
    for enemy in state.enemies[:]:
        if enemy.get("hp", 1) <= 0:
            kill(enemy, state)


def _handle_player_bullet_offscreen(state, ctx: dict) -> None:
    offscreen = ctx.get("rect_offscreen")
    if not offscreen:
        return
    for bullet in state.player_bullets[:]:
        if offscreen(bullet["rect"]) and bullet in state.player_bullets:
            state.player_bullets.remove(bullet)


def _handle_player_bullet_enemy_collisions(state, ctx: dict) -> None:
    kill = ctx.get("kill_enemy")
    size = ctx.get("enemy_projectile_size", (12, 12))
    color = ctx.get("enemy_projectiles_color", (200, 200, 200))
    if not kill:
        return
    player_damage = state.player_bullet_damage
    for bullet in state.player_bullets[:]:
        for enemy in state.enemies[:]:
            if not bullet["rect"].colliderect(enemy["rect"]):
                continue
            if enemy.get("has_shield") and not enemy.get("has_reflective_shield"):
                # Shield enemy: reflect with extra damage unless player flanks (hits from side/behind)
                center = pygame.Vector2(enemy["rect"].center)
                bcenter = pygame.Vector2(bullet["rect"].center)
                to_bullet = (bcenter - center)
                if to_bullet.length_squared() > 0:
                    to_bullet = to_bullet.normalize()
                sh_angle = enemy.get("shield_angle", 0.0)
                sh_dir = pygame.Vector2(math.cos(sh_angle), math.sin(sh_angle))
                from_front = to_bullet.dot(-sh_dir) > 0.0  # Bullet came from shield-facing side
                if from_front:
                    dmg = int((bullet.get("damage", player_damage)) * enemy.get("reflect_damage_mult", 1.5))
                    ref = pygame.Rect(
                        enemy["rect"].centerx - size[0] // 2,
                        enemy["rect"].centery - size[1] // 2,
                        size[0], size[1],
                    )
                    state.enemy_projectiles.append({
                        "rect": ref,
                        "vel": to_bullet * enemy.get("projectile_speed", 300),
                        "enemy_type": enemy["type"],
                        "color": enemy.get("projectile_color", color),
                        "shape": enemy.get("projectile_shape", "circle"),
                        "bounces": 0,
                        "damage": dmg,
                    })
                    if bullet in state.player_bullets:
                        state.player_bullets.remove(bullet)
                    break
                # else flanked: fall through to normal damage below
            if enemy.get("has_reflective_shield"):
                center = pygame.Vector2(enemy["rect"].center)
                bcenter = pygame.Vector2(bullet["rect"].center)
                bdir = (bcenter - center)
                if bdir.length_squared() > 0:
                    bdir = bdir.normalize()
                sh_angle = enemy.get("shield_angle", 0.0)
                sh_dir = pygame.Vector2(math.cos(sh_angle), math.sin(sh_angle))
                if bdir.dot(-sh_dir) > 0.0:
                    dmg = bullet.get("damage", player_damage)
                    enemy["shield_hp"] = enemy.get("shield_hp", 0) + dmg
                    if enemy["shield_hp"] > 0:
                        ref = pygame.Rect(
                            enemy["rect"].centerx - size[0] // 2,
                            enemy["rect"].centery - size[1] // 2,
                            size[0], size[1],
                        )
                        state.enemy_projectiles.append({
                            "rect": ref,
                            "vel": -bdir * enemy.get("projectile_speed", 300),
                            "enemy_type": enemy["type"],
                            "color": enemy.get("projectile_color", color),
                            "shape": enemy.get("projectile_shape", "circle"),
                            "bounces": 0,
                        })
                        enemy["shield_hp"] = 0
                    if bullet in state.player_bullets:
                        state.player_bullets.remove(bullet)
                    break
                else:
                    dmg = bullet.get("damage", player_damage)
                    enemy["hp"] -= dmg
                    state.damage_numbers.append({
                        "x": enemy["rect"].centerx,
                        "y": enemy["rect"].y - 20,
                        "damage": int(dmg),
                        "timer": 2.0,
                        "color": (255, 255, 100),
                    })
                    if enemy["hp"] <= 0:
                        kill(enemy, state)
                    if bullet.get("penetration", 0) <= 0:
                        if bullet in state.player_bullets:
                            state.player_bullets.remove(bullet)
                        break
                    bullet["penetration"] = bullet.get("penetration", 0) - 1
            else:
                dmg = bullet.get("damage", player_damage)
                enemy["hp"] -= dmg
                state.damage_numbers.append({
                    "x": enemy["rect"].centerx,
                    "y": enemy["rect"].y - 20,
                    "damage": int(dmg),
                    "timer": 2.0,
                    "color": (255, 255, 100),
                })
                if enemy["hp"] <= 0:
                    kill(enemy, state)
                if bullet.get("penetration", 0) <= 0:
                    if bullet in state.player_bullets:
                        state.player_bullets.remove(bullet)
                    break
                bullet["penetration"] = bullet.get("penetration", 0) - 1


def _handle_player_bullet_block_collisions(state, dt: float, ctx: dict) -> None:
    offscreen = ctx.get("rect_offscreen")
    check_hazard = ctx.get("check_point_in_hazard")
    d_blocks = ctx.get("destructible_blocks", [])
    m_blocks = ctx.get("moveable_destructible_blocks", [])
    g_blocks = ctx.get("giant_blocks", []) + ctx.get("super_giant_blocks", [])
    trapezo = ctx.get("trapezoid_blocks", [])
    tri = ctx.get("triangle_blocks", [])
    hazards = ctx.get("hazard_obstacles", [])
    player_damage = state.player_bullet_damage

    for bullet in state.player_bullets[:]:
        if bullet.get("removed"):
            continue
        for block in d_blocks + m_blocks:
            if not block.get("is_destructible") or not bullet["rect"].colliderect(block["rect"]):
                continue
            dmg = bullet.get("damage", player_damage)
            block["hp"] -= dmg
            if block["hp"] <= 0:
                if block in d_blocks:
                    d_blocks.remove(block)
                else:
                    m_blocks.remove(block)
            if bullet.get("penetration", 0) <= 0:
                if not bullet.get("bouncing", False):
                    if bullet in state.player_bullets:
                        state.player_bullets.remove(bullet)
                    bullet["removed"] = True
                    break
                bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
            break
        if bullet.get("removed"):
            continue
        for block in g_blocks:
            if bullet["rect"].colliderect(block["rect"]):
                if not bullet.get("bouncing", False):
                    if bullet in state.player_bullets:
                        state.player_bullets.remove(bullet)
                    bullet["removed"] = True
                    break
                bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
                break
        if bullet.get("removed"):
            continue
        for tb in trapezo:
            br = tb.get("bounding_rect", tb.get("rect"))
            if bullet["rect"].colliderect(br):
                if not bullet.get("bouncing", False):
                    if bullet in state.player_bullets:
                        state.player_bullets.remove(bullet)
                    bullet["removed"] = True
                    break
                bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
                break
        if bullet.get("removed"):
            continue
        for tr in tri:
            br = tr.get("bounding_rect", tr.get("rect"))
            if bullet["rect"].colliderect(br):
                if not bullet.get("bouncing", False):
                    if bullet in state.player_bullets:
                        state.player_bullets.remove(bullet)
                    bullet["removed"] = True
                    break
                bullet["vel"] = bullet["vel"].reflect(pygame.Vector2(1, 0))
                break
        if bullet.get("removed"):
            continue
        if not check_hazard:
            continue
        for hazard in hazards:
            if not hazard.get("points") or len(hazard["points"]) < 3:
                continue
            bc = pygame.Vector2(bullet["rect"].center)
            if check_hazard(bc, hazard["points"], hazard["bounding_rect"]):
                vel = bullet.get("vel", pygame.Vector2(0, 0))
                if vel.length_squared() > 0:
                    v = hazard.get("velocity", pygame.Vector2(0, 0))
                    hazard["velocity"] = v + vel.normalize() * 200.0 * dt
                if bullet in state.player_bullets:
                    state.player_bullets.remove(bullet)
                bullet["removed"] = True
                break


def _handle_enemy_projectile_lifetime_offscreen(state, ctx: dict) -> None:
    offscreen = ctx.get("rect_offscreen")
    for proj in state.enemy_projectiles[:]:
        if "lifetime" in proj and proj["lifetime"] <= 0:
            if proj in state.enemy_projectiles:
                state.enemy_projectiles.remove(proj)
            continue
        if offscreen and offscreen(proj["rect"]) and proj in state.enemy_projectiles:
            state.enemy_projectiles.remove(proj)


def _handle_enemy_projectile_block_collisions(state, ctx: dict) -> None:
    d_blocks = ctx.get("destructible_blocks", [])
    m_blocks = ctx.get("moveable_destructible_blocks", [])
    for proj in state.enemy_projectiles[:]:
        for block in d_blocks + m_blocks:
            if block.get("is_destructible") and proj["rect"].colliderect(block["rect"]):
                block["hp"] -= proj.get("damage", 10)
                if block["hp"] <= 0:
                    if block in d_blocks:
                        d_blocks.remove(block)
                    else:
                        m_blocks.remove(block)
                if proj in state.enemy_projectiles:
                    state.enemy_projectiles.remove(proj)
                break


def _handle_enemy_projectile_player_collisions(state, ctx: dict) -> None:
    player = state.player_rect
    if not player:
        return
    for proj in state.enemy_projectiles[:]:
        if not proj["rect"].colliderect(player):
            continue
        if state.shield_active:
            if proj in state.enemy_projectiles:
                state.enemy_projectiles.remove(proj)
            continue
        damage = proj.get("damage", 10)
        _apply_player_damage(state, damage, ctx)
        if proj in state.enemy_projectiles:
            state.enemy_projectiles.remove(proj)


def _handle_enemy_projectile_friendly_collisions(state, ctx: dict) -> None:
    """Apply enemy projectile damage to friendlies; remove hit projectiles and dead friendlies."""
    for proj in state.enemy_projectiles[:]:
        for friendly in state.friendly_ai[:]:
            if friendly.get("hp", 1) <= 0:
                continue
            if not proj["rect"].colliderect(friendly["rect"]):
                continue
            damage = proj.get("damage", 10)
            friendly["hp"] = friendly.get("hp", friendly.get("max_hp", 100)) - damage
            if proj in state.enemy_projectiles:
                state.enemy_projectiles.remove(proj)
            if friendly["hp"] <= 0 and friendly in state.friendly_ai:
                state.friendly_ai.remove(friendly)
            break


def _handle_teleporter_player(state, ctx: dict) -> None:
    """Teleport player to linked pad when touching a teleporter. Only player can overlap; cooldown prevents instant re-trigger."""
    player = state.player_rect
    pads = ctx.get("teleporter_pads", [])
    if not player or not pads:
        return
    if getattr(state, "teleporter_cooldown", 0) > 0:
        return
    for pad in pads:
        link = pad.get("linked_rect")
        if not link or not player.colliderect(pad["rect"]):
            continue
        player.center = link.center
        state.teleporter_cooldown = 0.5
        break


def _handle_pickup_player_collisions(state, ctx: dict) -> None:
    player = state.player_rect
    create_effect = ctx.get("create_pickup_collection_effect")
    apply_effect = ctx.get("apply_pickup_effect")
    if not player or not apply_effect:
        return
    for pickup in state.pickups[:]:
        if player.colliderect(pickup["rect"]):
            if create_effect:
                create_effect(pickup["rect"].centerx, pickup["rect"].centery, pickup["color"], state)
            apply_effect(pickup["type"], state)
            state.pickups.remove(pickup)


def _handle_health_zone_player_dt(state, dt: float, ctx: dict) -> None:
    player = state.player_rect
    zone = ctx.get("moving_health_zone")
    if not player or not zone or not zone.get("rect"):
        return
    if player.colliderect(zone["rect"]) and state.player_hp < state.player_max_hp:
        state.player_hp = min(state.player_max_hp, state.player_hp + 50 * dt)


def _handle_friendly_projectile_offscreen_blocks_enemies(state, ctx: dict) -> None:
    offscreen = ctx.get("rect_offscreen")
    kill = ctx.get("kill_enemy")
    d_blocks = ctx.get("destructible_blocks", [])
    m_blocks = ctx.get("moveable_destructible_blocks", [])
    for proj in state.friendly_projectiles[:]:
        if offscreen and offscreen(proj["rect"]):
            state.friendly_projectiles.remove(proj)
            continue
        for block in d_blocks + m_blocks:
            if block.get("is_destructible") and proj["rect"].colliderect(block["rect"]):
                block["hp"] -= proj.get("damage", 20)
                if block["hp"] <= 0:
                    if block in d_blocks:
                        d_blocks.remove(block)
                    else:
                        m_blocks.remove(block)
                state.friendly_projectiles.remove(proj)
                break
        else:
            for enemy in state.enemies[:]:
                if proj["rect"].colliderect(enemy["rect"]):
                    dmg = proj.get("damage", 20)
                    enemy["hp"] -= dmg
                    state.damage_numbers.append({
                        "x": enemy["rect"].centerx,
                        "y": enemy["rect"].y - 20,
                        "damage": int(dmg),
                        "timer": 2.0,
                        "color": (255, 255, 100),
                    })
                    if enemy["hp"] <= 0 and kill:
                        kill(enemy, state)
                    state.friendly_projectiles.remove(proj)
                    break


def _handle_grenade_explosion_damage(state, dt: float, ctx: dict) -> None:
    kill = ctx.get("kill_enemy")
    d_blocks = ctx.get("destructible_blocks", [])
    m_blocks = ctx.get("moveable_destructible_blocks", [])
    player = state.player_rect
    missile_damage_val = ctx.get("missile_damage", 800)

    for explosion in state.grenade_explosions[:]:
        explosion["timer"] = explosion.get("timer", 0.3) - dt
        explosion["radius"] = int(explosion.get("max_radius", 150) * (1.0 - explosion["timer"] / 0.3))
        if explosion["timer"] <= 0:
            state.grenade_explosions.remove(explosion)
            continue
        pos = pygame.Vector2(explosion["x"], explosion["y"])
        r = explosion["radius"]
        damage_val = explosion.get("damage", 500)
        source = explosion.get("source", "")
        # "enemy_player_allies_only" does not damage enemies, only player and allies
        if source != "enemy_player_allies_only":
            for enemy in state.enemies[:]:
                d = (pygame.Vector2(enemy["rect"].center) - pos).length()
                if d <= r:
                    enemy["hp"] -= damage_val
                    state.damage_numbers.append({
                        "x": enemy["rect"].centerx,
                        "y": enemy["rect"].y - 20,
                        "damage": int(damage_val),
                        "timer": 2.0,
                        "color": (255, 200, 100),
                    })
                    if enemy["hp"] <= 0 and kill:
                        kill(enemy, state)
        if source == "enemy_player_allies_only":
            for friendly in state.friendly_ai[:]:
                d = (pygame.Vector2(friendly["rect"].center) - pos).length()
                if d <= r:
                    friendly["hp"] = friendly.get("hp", friendly.get("max_hp", 100)) - damage_val
                    if friendly["hp"] <= 0 and friendly in state.friendly_ai:
                        state.friendly_ai.remove(friendly)
        if player:
            pd = (pygame.Vector2(player.center) - pos).length()
            # No player damage from own grenades ("player") or from missiles exploding on walls ("wall_impact")
            if pd <= r and source not in ("player", "wall_impact"):
                if not state.shield_active:
                    _apply_player_damage(state, damage_val, ctx)
        if source != "enemy_player_allies_only":
            for block in list(d_blocks) + list(m_blocks):
                if not block.get("is_destructible"):
                    continue
                bp = pygame.Vector2(block["rect"].center)
                if (bp - pos).length() <= r:
                    block["hp"] -= damage_val
                    if block["hp"] <= 0:
                        if block in d_blocks:
                            d_blocks.remove(block)
                        else:
                            m_blocks.remove(block)


def _handle_missile_collisions(state, ctx: dict) -> None:
    player = state.player_rect
    offscreen = ctx.get("rect_offscreen")
    kill = ctx.get("kill_enemy")
    md = ctx.get("missile_damage", 800)

    for missile in state.missiles[:]:
        if offscreen and offscreen(missile["rect"]):
            if missile in state.missiles:
                state.missiles.remove(missile)
            continue
        hit = False
        if missile.get("target_player") and player and missile["rect"].colliderect(player):
            hit = True
            if not state.shield_active:
                _apply_player_damage(state, missile.get("damage", md), ctx)
        elif missile.get("target_enemy") and missile["target_enemy"] in state.enemies:
            if missile["rect"].colliderect(missile["target_enemy"]["rect"]):
                hit = True
        if hit:
            pos = pygame.Vector2(missile["rect"].center)
            rad = missile.get("explosion_radius", 150)
            for enemy in state.enemies[:]:
                if (pygame.Vector2(enemy["rect"].center) - pos).length() <= rad:
                    dmg = missile.get("damage", md)
                    enemy["hp"] -= dmg
                    state.damage_numbers.append({
                        "x": enemy["rect"].centerx,
                        "y": enemy["rect"].y - 20,
                        "damage": int(dmg),
                        "timer": 2.0,
                        "color": (255, 150, 50),
                    })
                    if enemy["hp"] <= 0 and kill:
                        kill(enemy, state)
            if missile.get("target_player") and player:
                if (pygame.Vector2(player.center) - pos).length() <= rad and not state.shield_active:
                    _apply_player_damage(state, missile.get("damage", md), ctx)
            if missile in state.missiles:
                state.missiles.remove(missile)
