"""
Rendering helper functions - pure drawing utilities extracted from game.py.
These functions handle drawing textures, projectiles, health bars, and text.
"""
import math

import pygame


# Module-level caches for rendering optimization
_wall_texture_cache = {}
_health_bar_cache = {}
_hud_text_cache = {}


def _create_cached_silver_wall_texture(width: int, height: int) -> pygame.Surface:
    """Create a cached silver wall texture surface."""
    surf = pygame.Surface((width, height))
    silver_base = (192, 192, 192)
    silver_dark = (160, 160, 160)
    silver_light = (220, 220, 220)
    
    # Fill base
    surf.fill(silver_base)
    
    # Draw metallic grid pattern
    brick_width = max(8, width // 4)
    brick_height = max(6, height // 3)
    
    # Horizontal mortar lines
    for y in range(brick_height, height, brick_height):
        pygame.draw.line(surf, silver_dark, (0, y), (width, y), 1)
    
    # Vertical mortar lines (staggered)
    offset = 0
    for y in range(0, height, brick_height * 2):
        for x in range(offset, width, brick_width):
            pygame.draw.line(surf, silver_dark, (x, y), (x, min(y + brick_height, height)), 1)
        offset = brick_width // 2 if offset == 0 else 0
    
    # Add highlights for metallic shine
    for i in range(0, width, brick_width):
        for j in range(0, height, brick_height):
            highlight_x = i + brick_width // 4
            highlight_y = j + brick_height // 4
            if highlight_x < width and highlight_y < height:
                pygame.draw.circle(surf, silver_light, (highlight_x, highlight_y), 2)
    
    return surf


def _create_cached_cracked_brick_texture(width: int, height: int, crack_level: int) -> pygame.Surface:
    """Create a cached cracked brick wall texture surface."""
    surf = pygame.Surface((width, height))
    brick_red = (180, 80, 60)
    brick_dark = (140, 60, 40)
    brick_light = (200, 100, 80)
    mortar = (100, 100, 100)
    
    # Fill base brick color
    surf.fill(brick_red)
    
    # Draw brick pattern
    brick_width = max(10, width // 4)
    brick_height = max(8, height // 3)
    
    # Horizontal mortar lines
    for y in range(brick_height, height, brick_height):
        pygame.draw.line(surf, mortar, (0, y), (width, y), 2)
    
    # Vertical mortar lines (staggered brick pattern)
    offset = 0
    for y in range(0, height, brick_height * 2):
        for x in range(offset, width, brick_width):
            pygame.draw.line(surf, mortar, (x, y), (x, min(y + brick_height, height)), 2)
        offset = brick_width // 2 if offset == 0 else 0
    
    # Add individual brick highlights
    offset = 0
    for y in range(0, height, brick_height):
        for x in range(offset, width, brick_width):
            brick_rect = pygame.Rect(x + 1, y + 1, min(brick_width - 2, width - x - 1), min(brick_height - 2, height - y - 1))
            if brick_rect.w > 0 and brick_rect.h > 0:
                # Light highlight on top-left of each brick
                pygame.draw.line(surf, brick_light, (brick_rect.left, brick_rect.top), (brick_rect.right, brick_rect.top), 1)
                pygame.draw.line(surf, brick_light, (brick_rect.left, brick_rect.top), (brick_rect.left, brick_rect.bottom), 1)
                # Dark shadow on bottom-right
                pygame.draw.line(surf, brick_dark, (brick_rect.right, brick_rect.top), (brick_rect.right, brick_rect.bottom), 1)
                pygame.draw.line(surf, brick_dark, (brick_rect.left, brick_rect.bottom), (brick_rect.right, brick_rect.bottom), 1)
        offset = brick_width // 2 if offset == 0 else 0
    
    # Draw cracks based on damage level
    if crack_level >= 1:
        center = (width // 2, height // 2)
        crack_color = (40, 40, 40)
        # Main crack from center
        for i in range(crack_level):
            angle = (i * 2.4) * math.pi / 3
            end_x = center[0] + math.cos(angle) * (width // 2)
            end_y = center[1] + math.sin(angle) * (height // 2)
            pygame.draw.line(surf, crack_color, center, (end_x, end_y), 2)
        
        # Additional smaller cracks for higher damage
        if crack_level >= 2:
            for i in range(crack_level):
                angle = (i * 1.8 + 0.5) * math.pi / 3
                start_x = center[0] + math.cos(angle) * (width // 4)
                start_y = center[1] + math.sin(angle) * (height // 4)
                end_x = start_x + math.cos(angle) * (width // 3)
                end_y = start_y + math.sin(angle) * (height // 3)
                pygame.draw.line(surf, crack_color, (start_x, start_y), (end_x, end_y), 1)
    
    return surf


def draw_silver_wall_texture(screen: pygame.Surface, rect: pygame.Rect):
    """Draw a silver wall texture for indestructible blocks (uses cached surface when possible)."""
    # Use cache for common sizes (round to nearest 10 for better cache hit rate)
    cache_key = (rect.w // 10 * 10, rect.h // 10 * 10)
    
    if cache_key not in _wall_texture_cache:
        _wall_texture_cache[cache_key] = _create_cached_silver_wall_texture(cache_key[0], cache_key[1])
    
    cached_surf = _wall_texture_cache[cache_key]
    # Blit cached surface, scaling if needed
    if cache_key[0] == rect.w and cache_key[1] == rect.h:
        screen.blit(cached_surf, rect.topleft)
    else:
        # Scale if size doesn't match exactly
        scaled = pygame.transform.scale(cached_surf, (rect.w, rect.h))
        screen.blit(scaled, rect.topleft)


def draw_cracked_brick_wall_texture(screen: pygame.Surface, rect: pygame.Rect, crack_level: int = 1):
    """Draw a cracked brick wall texture for destructible blocks (uses cached surface when possible)."""
    # Use cache for common sizes (round to nearest 10 for better cache hit rate)
    cache_key = (rect.w // 10 * 10, rect.h // 10 * 10, crack_level)
    
    if cache_key not in _wall_texture_cache:
        _wall_texture_cache[cache_key] = _create_cached_cracked_brick_texture(cache_key[0], cache_key[1], crack_level)
    
    cached_surf = _wall_texture_cache[cache_key]
    # Blit cached surface, scaling if needed
    if cache_key[0] == rect.w and cache_key[1] == rect.h:
        screen.blit(cached_surf, rect.topleft)
    else:
        # Scale if size doesn't match exactly
        scaled = pygame.transform.scale(cached_surf, (rect.w, rect.h))
        screen.blit(scaled, rect.topleft)


def draw_health_bar(screen: pygame.Surface, x: int, y: int, w: int, h: int, hp: float, max_hp: float):
    """Draw health bar (uses cached surface for common sizes/ratios when possible)."""
    hp = max(0, min(hp, max_hp))
    hp_ratio = hp / max_hp if max_hp > 0 else 0.0
    
    # Cache for common health bar sizes (round to nearest 5 for better cache hits)
    # Only cache if bar is reasonably sized (not too many variations)
    # Only use cache if the rounded ratio matches the actual ratio (to avoid visual inaccuracies)
    if w <= 200 and h <= 20:
        rounded_ratio = int(hp_ratio * 10)  # Round to 10% increments
        actual_fill = int(w * hp_ratio)
        cached_fill = int(w * (rounded_ratio / 10.0))
        
        # Only use cache if rounded ratio produces the same visual result
        if actual_fill == cached_fill:
            cache_key = (w // 5 * 5, h, rounded_ratio)
            if cache_key not in _health_bar_cache:
                cached_w, cached_h, cached_ratio = cache_key
                cached_surf = pygame.Surface((cached_w, cached_h))
                cached_surf.fill((60, 60, 60))
                fill_w = int(cached_w * (cached_ratio / 10.0))
                if fill_w > 0:
                    pygame.draw.rect(cached_surf, (60, 200, 60), (0, 0, fill_w, cached_h))
                pygame.draw.rect(cached_surf, (20, 20, 20), (0, 0, cached_w, cached_h), 2)
                _health_bar_cache[cache_key] = cached_surf
            
            # Use cached surface if size matches exactly
            if cache_key[0] == w and cache_key[1] == h:
                screen.blit(_health_bar_cache[cache_key], (x, y))
                return
    
    # Fallback to direct drawing for non-cached sizes or when ratio doesn't match
    pygame.draw.rect(screen, (60, 60, 60), (x, y, w, h))
    fill_w = int(w * hp_ratio)
    if fill_w > 0:
        pygame.draw.rect(screen, (60, 200, 60), (x, y, fill_w, h))
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), 2)


def draw_centered_text(screen: pygame.Surface, font: pygame.font.Font, big_font: pygame.font.Font, width: int, text: str, y: int, color=(235, 235, 235), use_big=False):
    """Draw centered text on screen."""
    f = big_font if use_big else font
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(width // 2, y))
    screen.blit(surf, rect)


def draw_projectile(screen: pygame.Surface, rect: pygame.Rect, color: tuple[int, int, int], shape: str):
    """Draw a projectile with the specified shape."""
    if shape == "circle":
        pygame.draw.circle(screen, color, rect.center, rect.w // 2)
    elif shape == "diamond":
        cx, cy = rect.center
        hw, hh = rect.w // 2, rect.h // 2
        points = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
        pygame.draw.polygon(screen, color, points)
    else:
        pygame.draw.rect(screen, color, rect)


def render_hud_text(screen: pygame.Surface, font: pygame.font.Font, text: str, y: int, color=(230, 230, 230)) -> int:
    """Render HUD text at position and return next Y position (uses cached surface when possible)."""
    cache_key = (text, color)
    if cache_key not in _hud_text_cache:
        _hud_text_cache[cache_key] = font.render(text, True, color)
    screen.blit(_hud_text_cache[cache_key], (10, y))
    return y + 24


# Caches for trapezoid/triangle block surfaces (used by render_gameplay)
_trapezoid_surface_cache: dict = {}
_triangle_surface_cache: dict = {}


def render_gameplay(state, screen: pygame.Surface, ctx: dict) -> None:
    """Central entry for gameplay/world rendering. Read-only: does not modify state.

    Draw order: (1) background, (2) terrain/obstacles, (3) pickups, (4) projectiles,
    (5) allies and enemies, (6) effects (explosions, missiles), (7) player, (8) beams.
    HUD/UI is drawn by the caller via ui_system after this returns.

    ctx must contain: level_themes, trapezoid_blocks, triangle_blocks, destructible_blocks,
    moveable_destructible_blocks, giant_blocks, super_giant_blocks, hazard_obstacles,
    moving_health_zone, small_font, weapon_names.
    """
    if not ctx:
        return
    level_themes = ctx.get("level_themes", {})
    default_theme = level_themes.get(1, {})
    theme = level_themes.get(getattr(state, "current_level", 1), default_theme)
    bg = theme.get("bg_color", (0, 0, 0))
    screen.fill(bg)

    _draw_terrain(screen, state, ctx)
    _draw_pickups(screen, state, ctx)
    _draw_projectiles(screen, state)
    _draw_allies_and_enemies(screen, state)
    _draw_effects(screen, state)
    _draw_player(screen, state)
    _draw_beams(screen, state)


def _draw_terrain(screen: pygame.Surface, state, ctx: dict) -> None:
    """Draw static obstacles: trapezoid/triangle blocks, destructible/giant blocks, hazards, health zone."""
    trapezoid_blocks = ctx.get("trapezoid_blocks", [])
    triangle_blocks = ctx.get("triangle_blocks", [])
    for tr in trapezoid_blocks:
        block_id = f"trap_{id(tr)}"
        if block_id not in _trapezoid_surface_cache:
            points = tr.get("points", [])
            if points:
                min_x = min(p[0] for p in points)
                max_x = max(p[0] for p in points)
                min_y = min(p[1] for p in points)
                max_y = max(p[1] for p in points)
                cached_surf = pygame.Surface((max_x - min_x + 10, max_y - min_y + 10), pygame.SRCALPHA)
                offset_pts = [(p[0] - min_x + 5, p[1] - min_y + 5) for p in points]
                pygame.draw.polygon(cached_surf, tr["color"], offset_pts)
                pygame.draw.polygon(cached_surf, (255, 255, 255), offset_pts, 2)
                _trapezoid_surface_cache[block_id] = (cached_surf, (min_x - 5, min_y - 5))
        if block_id in _trapezoid_surface_cache:
            surf, offset = _trapezoid_surface_cache[block_id]
            screen.blit(surf, offset)

    for tr in triangle_blocks:
        block_id = f"tri_{id(tr)}"
        if block_id not in _triangle_surface_cache:
            points = tr.get("points", [])
            if points:
                min_x = min(p[0] for p in points)
                max_x = max(p[0] for p in points)
                min_y = min(p[1] for p in points)
                max_y = max(p[1] for p in points)
                cached_surf = pygame.Surface((max_x - min_x + 10, max_y - min_y + 10), pygame.SRCALPHA)
                offset_pts = [(p[0] - min_x + 5, p[1] - min_y + 5) for p in points]
                pygame.draw.polygon(cached_surf, tr["color"], offset_pts)
                pygame.draw.polygon(cached_surf, (255, 255, 255), offset_pts, 2)
                _triangle_surface_cache[block_id] = (cached_surf, (min_x - 5, min_y - 5))
        if block_id in _triangle_surface_cache:
            surf, offset = _triangle_surface_cache[block_id]
            screen.blit(surf, offset)

    for block in ctx.get("destructible_blocks", []):
        if block.get("is_destructible") and block.get("hp", 0) > 0:
            draw_cracked_brick_wall_texture(screen, block["rect"], block.get("crack_level", 0))
        else:
            draw_silver_wall_texture(screen, block["rect"])
    for block in ctx.get("moveable_destructible_blocks", []):
        if block.get("is_destructible") and block.get("hp", 0) > 0:
            draw_cracked_brick_wall_texture(screen, block["rect"], block.get("crack_level", 0))
        else:
            draw_silver_wall_texture(screen, block["rect"])
    for block in ctx.get("giant_blocks", []):
        draw_silver_wall_texture(screen, block["rect"])
    for block in ctx.get("super_giant_blocks", []):
        draw_silver_wall_texture(screen, block["rect"])

    for hazard in ctx.get("hazard_obstacles", []):
        points = hazard.get("points", [])
        if len(points) >= 3:
            pygame.draw.polygon(screen, hazard["color"], points)
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)

    zone = ctx.get("moving_health_zone")
    if zone:
        zone_width = zone["rect"].w
        zone_height = zone["rect"].h
        use_triangle = (getattr(state, "wave_in_level", 1) % 2 == 0)
        zone_surf = pygame.Surface((zone["rect"].w + 20, zone["rect"].h + 20), pygame.SRCALPHA)
        if use_triangle:
            triangle_points = [
                (zone_width // 2, 10),
                (10, zone_height + 10),
                (zone_width + 10, zone_height + 10),
            ]
            pygame.draw.polygon(zone_surf, zone["color"], triangle_points)
            screen.blit(zone_surf, (zone["rect"].x - 10, zone["rect"].y - 10))
            pulse = 0.5 + 0.5 * math.sin(getattr(state, "run_time", 0) * 3.0)
            border_color = (50, 255, 50)
            zone_center = (zone["rect"].centerx, zone["rect"].centery)
            pygame.draw.polygon(screen, border_color, [
                (zone_center[0], zone["rect"].y),
                (zone["rect"].x, zone["rect"].bottom),
                (zone["rect"].right, zone["rect"].bottom),
            ], 3)
        else:
            pygame.draw.rect(zone_surf, zone["color"], (10, 10, zone["rect"].w, zone["rect"].h))
            screen.blit(zone_surf, (zone["rect"].x - 10, zone["rect"].y - 10))
            border_color = (50, 255, 50)
            pygame.draw.rect(screen, border_color, zone["rect"], 3)


def _draw_pickups(screen: pygame.Surface, state, ctx: dict) -> None:
    """Draw pickups and their labels."""
    weapon_names = ctx.get("weapon_names", {})
    small_font = ctx.get("small_font")
    for pickup in getattr(state, "pickups", []):
        pygame.draw.circle(screen, pickup["color"], pickup["rect"].center, pickup["rect"].w // 2)
        pygame.draw.circle(screen, (255, 255, 255), pickup["rect"].center, pickup["rect"].w // 2, 2)
        if small_font:
            if pickup.get("is_weapon_drop", False):
                pickup_name = weapon_names.get(pickup.get("type", ""), pickup.get("type", "").upper())
            else:
                pickup_name = pickup.get("type", "").upper().replace("_", " ")
            name_surf = small_font.render(pickup_name, True, (255, 255, 255))
            name_rect = name_surf.get_rect(center=(pickup["rect"].centerx, pickup["rect"].y - 20))
            outline_surf = small_font.render(pickup_name, True, (0, 0, 0))
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                screen.blit(outline_surf, (name_rect.x + dx, name_rect.y + dy))
            screen.blit(name_surf, name_rect)


def _draw_projectiles(screen: pygame.Surface, state) -> None:
    """Draw enemy, player, and friendly projectiles."""
    for proj in getattr(state, "enemy_projectiles", []):
        draw_projectile(screen, proj["rect"], proj["color"], proj.get("shape", "circle"))
    for bullet in getattr(state, "player_bullets", []):
        draw_projectile(screen, bullet["rect"], bullet["color"], bullet.get("shape", "circle"))
    for proj in getattr(state, "friendly_projectiles", []):
        draw_projectile(screen, proj["rect"], proj["color"], proj.get("shape", "circle"))


def _draw_allies_and_enemies(screen: pygame.Surface, state) -> None:
    """Draw friendly AI and enemies (unified entity.draw or rect fallback)."""
    for friendly in getattr(state, "friendly_ai", []):
        if hasattr(friendly, "draw"):
            friendly.draw(screen)
        else:
            r = friendly.get("rect")
            if r:
                pygame.draw.rect(screen, friendly.get("color", (100, 200, 100)), r)
    enemies_list = getattr(state, "enemies", [])
    highlight_when_few = len(enemies_list) <= 5
    for enemy in enemies_list:
        r = enemy.get("rect") if isinstance(enemy, dict) else getattr(enemy, "rect", None)
        if hasattr(enemy, "draw"):
            enemy.draw(screen)
        elif r:
            pygame.draw.rect(screen, enemy.get("color", (200, 50, 50)), r)
        if highlight_when_few and r:
            out = r.inflate(8, 8)
            pygame.draw.rect(screen, (255, 255, 0), out, 3)


def _draw_effects(screen: pygame.Surface, state) -> None:
    """Draw grenade explosions and missiles."""
    for explosion in getattr(state, "grenade_explosions", []):
        pygame.draw.circle(screen, (255, 100, 0), (explosion["x"], explosion["y"]), explosion["radius"], 3)
        pygame.draw.circle(screen, (255, 200, 0), (explosion["x"], explosion["y"]), explosion["radius"] // 2)
    for missile in getattr(state, "missiles", []):
        pygame.draw.rect(screen, (255, 200, 0), missile["rect"])
        pygame.draw.rect(screen, (255, 100, 0), missile["rect"], 2)


def _draw_player(screen: pygame.Surface, state) -> None:
    """Draw player circle (and border); shield-active uses red tint."""
    player = getattr(state, "player_rect", None)
    if player is None:
        return
    player_color = (255, 255, 255)
    border_color = (200, 200, 200)
    if getattr(state, "shield_active", False):
        player_color = (255, 100, 100)
        border_color = (255, 150, 150)
    pygame.draw.circle(screen, border_color, player.center, player.w // 2 + 2, 2)
    pygame.draw.circle(screen, player_color, player.center, player.w // 2)


def _draw_beams(screen: pygame.Surface, state) -> None:
    """Draw laser and wave beams."""
    for beam in getattr(state, "laser_beams", []):
        if "start" in beam and "end" in beam:
            pygame.draw.line(
                screen, beam.get("color", (255, 50, 50)), beam["start"], beam["end"], beam.get("width", 5)
            )
