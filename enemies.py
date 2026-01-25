"""Enemy behavior and helper functions."""
import math
import random
import pygame
from entities import Enemy
from config_enemies import (
    ENEMY_HP_SCALE_MULTIPLIER,
    ENEMY_SPEED_SCALE_MULTIPLIER,
    ENEMY_FIRE_RATE_MULTIPLIER,
    ENEMY_HP_CAP,
    QUEEN_FIXED_HP,
)
from constants import ENEMY_COLOR, ENEMY_PROJECTILES_COLOR
from telemetry import EnemySpawnEvent


def clamp_rect_to_screen(r: pygame.Rect, width: int, height: int):
    """Clamp a rect to screen boundaries."""
    r.x = max(0, min(r.x, width - r.w))
    r.y = max(0, min(r.y, height - r.h))


def move_enemy_with_push_cached(
    enemy_rect: pygame.Rect,
    move_x: int,
    move_y: int,
    block_list: list[dict],
    cached_moveable_destructible_rects: list,
    cached_trapezoid_rects: list,
    cached_triangle_rects: list,
    destructible_blocks: list[dict],
    giant_blocks: list[dict],
    super_giant_blocks: list[dict],
    pickups: list[dict],
    friendly_ai: list[dict],
    enemies: list[dict],
    player: pygame.Rect,
    moving_health_zone: dict,
    width: int,
    height: int,
):
    """Optimized enemy movement - enemies cannot go through objects and must navigate around them."""
    # Cache rects for performance
    block_rects = [b["rect"] for b in block_list]
    cached_destructible_rects = [b["rect"] for b in destructible_blocks]
    cached_giant_rects = [gb["rect"] for gb in giant_blocks]
    cached_super_giant_rects = [sgb["rect"] for sgb in super_giant_blocks]
    cached_pickup_rects = [p["rect"] for p in pickups]
    cached_friendly_rects = [f["rect"] for f in friendly_ai if f.get("hp", 1) > 0]
    cached_enemy_rects = [e["rect"] for e in enemies if e["rect"] is not enemy_rect]

    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        enemy_rect.x += axis_dx
        enemy_rect.y += axis_dy

        # Check collisions with all objects - enemies cannot pass through anything
        collision = False
        
        # Check regular blocks
        for rect in block_rects:
            if enemy_rect.colliderect(rect):
                collision = True
                break
        
        # Check destructible blocks
        if not collision:
            for rect in cached_destructible_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check moveable destructible blocks
        if not collision:
            for rect in cached_moveable_destructible_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check giant blocks (unmovable)
        if not collision:
            for rect in cached_giant_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check super giant blocks (unmovable)
        if not collision:
            for rect in cached_super_giant_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check trapezoid blocks
        if not collision:
            for rect in cached_trapezoid_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check triangle blocks
        if not collision:
            for rect in cached_triangle_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check pickups
        if not collision:
            for rect in cached_pickup_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check health zone
        if not collision:
            if enemy_rect.colliderect(moving_health_zone["rect"]):
                collision = True
        
        # Check player
        if not collision:
            if enemy_rect.colliderect(player):
                collision = True
        
        # Check friendly AI
        if not collision:
            for rect in cached_friendly_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break
        
        # Check other enemies (prevent enemy stacking)
        if not collision:
            for rect in cached_enemy_rects:
                if enemy_rect.colliderect(rect):
                    collision = True
                    break

        # If collision detected, revert movement
        if collision:
            enemy_rect.x -= axis_dx
            enemy_rect.y -= axis_dy

    clamp_rect_to_screen(enemy_rect, width, height)


def find_nearest_threat(
    enemy_pos: pygame.Vector2,
    player: pygame.Rect | None,
    friendly_ai: list[dict],
) -> tuple[pygame.Vector2, str] | None:
    """Find the nearest threat (player or friendly AI) to an enemy.
    Prioritizes dropped ally if within radius, otherwise prioritizes player."""
    if player is None:
        player_pos = None
        player_dist_sq = float("inf")
        player_dist = float("inf")
    else:
        player_pos = pygame.Vector2(player.center)
        player_dist_sq = (player_pos - enemy_pos).length_squared()
        player_dist = math.sqrt(player_dist_sq)

    # Collect friendly AI threats
    dropped_ally_threats = []
    other_friendly_threats = []
    for f in friendly_ai:
        if f["hp"] <= 0:
            continue
        friendly_pos = pygame.Vector2(f["rect"].center)
        friendly_dist_sq = (friendly_pos - enemy_pos).length_squared()
        friendly_dist = math.sqrt(friendly_dist_sq)
        if f.get("is_dropped_ally", False):
            dropped_ally_threats.append((friendly_pos, friendly_dist_sq, "dropped_ally", friendly_dist))
        else:
            other_friendly_threats.append((friendly_pos, friendly_dist_sq, "friendly", friendly_dist))
    
    # Priority: Dropped ally if within 350 pixels, otherwise player
    ALLY_FOCUS_RADIUS = 350.0  # Enemies focus on ally if within this radius
    ALLY_FOCUS_RADIUS_SQ = ALLY_FOCUS_RADIUS * ALLY_FOCUS_RADIUS
    
    # Check if there's a dropped ally within focus radius
    if dropped_ally_threats:
        dropped_ally_threats.sort(key=lambda x: x[1])  # Sort by distance
        nearest_ally = dropped_ally_threats[0]
        if nearest_ally[1] <= ALLY_FOCUS_RADIUS_SQ:
            # Focus on dropped ally if within radius
            return (nearest_ally[0], nearest_ally[2])

    # Otherwise, prioritize player (if present)
    if player_pos is not None:
        return (player_pos, "player")
    # No player; return nearest friendly if any
    if other_friendly_threats:
        other_friendly_threats.sort(key=lambda x: x[1])
        return (other_friendly_threats[0][0], other_friendly_threats[0][2])
    return None


def make_enemy_from_template(t: dict, hp_scale: float, speed_scale: float) -> Enemy:
    """Create an enemy from a template with scaling applied."""
    # Apply scaling multipliers from config
    # Exception: Queen (player clone) has fixed HP and special speed multiplier
    if t.get("type") == "queen":
        hp = QUEEN_FIXED_HP  # Fixed health for queen
        base_speed = t.get("speed", 80)
        final_speed = base_speed * ENEMY_SPEED_SCALE_MULTIPLIER  # Still apply speed multiplier
    else:
        hp = int(t["hp"] * hp_scale * ENEMY_HP_SCALE_MULTIPLIER * 10)  # Apply HP scale multiplier and x10
        # Cap HP at maximum (except queen)
        hp = min(hp, ENEMY_HP_CAP * 10)
        final_speed = t.get("speed", 80) * speed_scale * ENEMY_SPEED_SCALE_MULTIPLIER  # Apply speed multiplier
    
    enemy = {
        "type": t["type"],
        "rect": pygame.Rect(t["rect"].x, t["rect"].y, t["rect"].w, t["rect"].h),
        "color": ENEMY_COLOR,  # All enemies same color
        "hp": hp,
        "max_hp": hp,
        "shoot_cooldown": t["shoot_cooldown"] / ENEMY_FIRE_RATE_MULTIPLIER,  # Faster fire rate (lower cooldown)
        "time_since_shot": random.uniform(0.0, t["shoot_cooldown"] / ENEMY_FIRE_RATE_MULTIPLIER),
        "projectile_speed": t["projectile_speed"],
        "projectile_color": t.get("projectile_color", ENEMY_PROJECTILES_COLOR),
        "projectile_shape": t.get("projectile_shape", "circle"),
        "speed": final_speed,  # Speed (queen gets special multiplier, others get normal scaling)
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
    # Add predictive enemy property (for enemies that predict player position)
    if t.get("is_predictive"):
        enemy["is_predictive"] = True
    
    # Add queen-specific properties
    if t.get("type") == "queen":
        enemy["name"] = t.get("name", "queen")
        enemy["can_use_grenades"] = t.get("can_use_grenades", False)
        enemy["grenade_cooldown"] = t.get("grenade_cooldown", 5.0)
        enemy["time_since_grenade"] = t.get("time_since_grenade", 999.0)
        enemy["damage_taken_since_rage"] = 0
        enemy["rage_mode_active"] = False
        enemy["rage_mode_timer"] = 0.0
        # rage_damage_threshold is set in template (randomized at module load time)
        enemy["rage_damage_threshold"] = t.get("rage_damage_threshold", random.randint(300, 500))
        enemy["predicts_player"] = t.get("predicts_player", False)
    return Enemy(enemy)


def log_enemy_spawns(
    new_enemies: list[dict],
    telemetry,
    run_time: float,
    enemies_spawned_ref: list[int],  # List with one element to simulate global variable
):
    """Log enemy spawns to telemetry."""
    for e in new_enemies:
        enemies_spawned_ref[0] += 1
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


def find_threats_in_dodge_range(
    enemy_pos: pygame.Vector2,
    player_bullets: list[dict],
    friendly_projectiles: list[dict],
    dodge_range: float = 200.0,
) -> list[pygame.Vector2]:
    """Find bullets (player or friendly) that are close enough to dodge."""
    threats = []
    enemy_v2 = pygame.Vector2(enemy_pos)
    dodge_range_sq = dodge_range * dodge_range  # Use squared distance for faster comparison
    
    # Check player bullets
    for b in player_bullets:
        bullet_pos = pygame.Vector2(b["rect"].center)
        dist_sq = (bullet_pos - enemy_v2).length_squared()
        if dist_sq < dodge_range_sq:
            # Only compute actual distance if in range
            dist = math.sqrt(dist_sq)
            # Predict where bullet will be
            bullet_vel = b.get("vel", pygame.Vector2(0, 0))
            vel_length = bullet_vel.length()
            time_to_reach = dist / vel_length if vel_length > 0 else 999
            if time_to_reach < 0.5:  # Only dodge if bullet will reach soon
                threats.append(bullet_pos)
    
    # Check friendly projectiles
    for fp in friendly_projectiles:
        bullet_pos = pygame.Vector2(fp["rect"].center)
        dist_sq = (bullet_pos - enemy_v2).length_squared()
        if dist_sq < dodge_range_sq:
            # Only compute actual distance if in range
            dist = math.sqrt(dist_sq)
            bullet_vel = fp.get("vel", pygame.Vector2(0, 0))
            vel_length = bullet_vel.length()
            time_to_reach = dist / vel_length if vel_length > 0 else 999
            if time_to_reach < 0.5:
                threats.append(bullet_pos)
    
    return threats
