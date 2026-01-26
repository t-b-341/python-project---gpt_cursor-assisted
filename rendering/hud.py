"""
HUD-related drawing: health bars, centered text, HUD text.
"""
from __future__ import annotations

import pygame

# Module-level caches for rendering optimization
_health_bar_cache = {}
_hud_text_cache = {}


def draw_health_bar(screen: pygame.Surface, x: int, y: int, w: int, h: int, hp: float, max_hp: float) -> None:
    """Draw health bar (uses cached surface for common sizes/ratios when possible)."""
    hp = max(0, min(hp, max_hp))
    hp_ratio = hp / max_hp if max_hp > 0 else 0.0

    if w <= 200 and h <= 20:
        rounded_ratio = int(hp_ratio * 10)
        actual_fill = int(w * hp_ratio)
        cached_fill = int(w * (rounded_ratio / 10.0))

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

            if cache_key[0] == w and cache_key[1] == h:
                screen.blit(_health_bar_cache[cache_key], (x, y))
                return

    pygame.draw.rect(screen, (60, 60, 60), (x, y, w, h))
    fill_w = int(w * hp_ratio)
    if fill_w > 0:
        pygame.draw.rect(screen, (60, 200, 60), (x, y, fill_w, h))
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), 2)


def draw_centered_text(
    screen: pygame.Surface,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
    width: int,
    text: str,
    y: int,
    color=(235, 235, 235),
    use_big=False,
) -> None:
    """Draw centered text on screen."""
    f = big_font if use_big else font
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(width // 2, y))
    screen.blit(surf, rect)


def render_hud_text(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    y: int,
    color=(230, 230, 230),
) -> int:
    """Render HUD text at position and return next Y position (uses cached surface when possible)."""
    cache_key = (text, color)
    if cache_key not in _hud_text_cache:
        _hud_text_cache[cache_key] = font.render(text, True, color)
    screen.blit(_hud_text_cache[cache_key], (10, y))
    return y + 24
