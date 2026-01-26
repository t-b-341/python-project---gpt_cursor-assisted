"""
RenderContext: screen, fonts, and layout for a single frame.
Build from AppContext via RenderContext.from_app_ctx(app_ctx).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pygame

from asset_manager import get_font


def _default_font(size: int) -> pygame.font.Font:
    """Fallback font when ctx has no font; uses centralized asset_manager."""
    return get_font("main", size)


@dataclass
class RenderContext:
    """Screen, fonts, and layout constants for a single frame. Build from AppContext for consistency."""
    screen: pygame.Surface
    font: pygame.font.Font
    big_font: pygame.font.Font
    small_font: pygame.font.Font
    width: int
    height: int

    @classmethod
    def from_app_ctx(cls, app_ctx: Any) -> RenderContext:
        """Build a RenderContext from AppContext (screen, fonts, width, height)."""
        return cls(
            screen=app_ctx.screen,
            font=app_ctx.font,
            big_font=app_ctx.big_font,
            small_font=app_ctx.small_font,
            width=app_ctx.width,
            height=app_ctx.height,
        )

    @classmethod
    def from_screen_and_ctx(cls, screen: pygame.Surface, ctx: dict) -> RenderContext:
        """Build from (screen, ctx) when app_ctx is not available. ctx must have font, big_font, small_font, WIDTH, HEIGHT."""
        return cls(
            screen=screen,
            font=ctx.get("font") or _default_font(28),
            big_font=ctx.get("big_font") or _default_font(56),
            small_font=ctx.get("small_font") or _default_font(20),
            width=ctx.get("WIDTH", 1920),
            height=ctx.get("HEIGHT", 1080),
        )
