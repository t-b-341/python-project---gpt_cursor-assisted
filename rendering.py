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
