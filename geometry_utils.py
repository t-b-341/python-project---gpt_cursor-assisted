"""Generic geometry and physics helpers. Used by game.py and other modules.

Physics (vec_toward, can_move_rect) is provided by physics_loader. The game must
call physics_loader.resolve_physics() at startup before using these functions.
"""
from __future__ import annotations

import pygame

# Screen dimensions used by rect_offscreen and can_move_rect (set by game.main() at runtime)
_screen_width = 1920
_screen_height = 1080


def set_screen_dimensions(width: int, height: int) -> None:
    """Set the screen dimensions used by rect_offscreen and can_move_rect. Call from game.main() after resolving display size."""
    global _screen_width, _screen_height
    _screen_width, _screen_height = width, height


def clamp_rect_to_screen(r: pygame.Rect, width: int, height: int) -> None:
    r.x = max(0, min(r.x, width - r.w))
    r.y = max(0, min(r.y, height - r.h))


def vec_toward(ax, ay, bx, by) -> pygame.Vector2:
    from physics_loader import get_physics
    p = get_physics()
    if p is not None and hasattr(p, "vec_toward"):
        x, y = p.vec_toward(ax, ay, bx, by)
        return pygame.Vector2(x, y)
    v = pygame.Vector2(bx - ax, by - ay)
    if v.length_squared() == 0:
        return pygame.Vector2(1, 0)
    return v.normalize()


def line_rect_intersection(start: pygame.Vector2, end: pygame.Vector2, rect: pygame.Rect) -> pygame.Vector2 | None:
    """Find the closest intersection point between a line and a rectangle."""
    clipped = rect.clipline(start, end)
    if not clipped:
        return None
    p1, p2 = clipped
    dist1 = (pygame.Vector2(p1) - start).length_squared()
    dist2 = (pygame.Vector2(p2) - start).length_squared()
    return pygame.Vector2(p1) if dist1 < dist2 else pygame.Vector2(p2)


def can_move_rect(rect: pygame.Rect, dx: int, dy: int, other_rects: list[pygame.Rect]) -> bool:
    from physics_loader import get_physics
    p = get_physics()
    if p is not None and hasattr(p, "can_move_rect"):
        return p.can_move_rect(
            rect.x, rect.y, rect.w, rect.h, dx, dy, other_rects, _screen_width, _screen_height
        )
    test = rect.move(dx, dy)
    if test.left < 0 or test.right > _screen_width or test.top < 0 or test.bottom > _screen_height:
        return False
    for o in other_rects:
        if test.colliderect(o):
            return False
    return True


def rect_offscreen(r: pygame.Rect) -> bool:
    return r.right < 0 or r.left > _screen_width or r.bottom < 0 or r.top > _screen_height


def filter_blocks_too_close_to_player(block_list: list[dict], player_center: pygame.Vector2, player_size: int) -> list[dict]:
    """Filter out blocks that are too close to the player (within 10x player size radius)."""
    min_distance = player_size * 10
    filtered = []
    for block in block_list:
        block_center = pygame.Vector2(block["rect"].center)
        distance = block_center.distance_to(player_center)
        if distance >= min_distance:
            filtered.append(block)
    return filtered
