"""Resolve and expose the physics implementation (C extension or Python fallback).

Call resolve_physics(force_python) at startup; then geometry_utils and other
consumers use get_physics() for vec_toward / can_move_rect. The main game sets
ctx.using_c_physics from the returned flag.
"""
from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pygame

_impl: Any = None
_using_c: bool = False


def _python_vec_toward(ax: float, ay: float, bx: float, by: float) -> tuple[float, float]:
    v = pygame.Vector2(bx - ax, by - ay)
    if v.length_squared() < 1e-12:
        return (1.0, 0.0)
    v = v.normalize()
    return (v.x, v.y)


def _python_can_move_rect(
    x: int, y: int, w: int, h: int,
    dx: int, dy: int,
    other_rects: list[Any],
    screen_width: int, screen_height: int,
) -> bool:
    test = pygame.Rect(x + dx, y + dy, w, h)
    if test.left < 0 or test.right > screen_width or test.top < 0 or test.bottom > screen_height:
        return False
    for o in other_rects:
        if test.colliderect(o):
            return False
    return True


def _python_physics_namespace() -> SimpleNamespace:
    return SimpleNamespace(
        vec_toward=_python_vec_toward,
        can_move_rect=_python_can_move_rect,
    )


def resolve_physics(force_python: bool = False) -> tuple[Any, bool]:
    """Resolve the physics implementation. Call once at startup before using geometry_utils.

    Returns:
        (physics_impl, using_c): impl has vec_toward(ax,ay,bx,by)->(x,y) and
        can_move_rect(x,y,w,h,dx,dy,other_rects,sw,sh)->bool. using_c is True
        iff the C-accelerated module is in use.
    """
    global _impl, _using_c
    if force_python:
        _impl = _python_physics_namespace()
        _using_c = False
        print("C-accelerated physics unavailable; using Python fallback.")
        return (_impl, False)
    try:
        import game_physics  # type: ignore
        _impl = game_physics
        _using_c = True
        print("Using C-accelerated physics module.")
        return (_impl, True)
    except ImportError:
        _impl = _python_physics_namespace()
        _using_c = False
        print("C-accelerated physics unavailable; using Python fallback.")
        return (_impl, False)


def get_physics() -> Any:
    """Return the resolved physics implementation. resolve_physics() must have been called first."""
    return _impl
