"""Optional shader-based gameplay rendering wrapper. Renders to offscreen then blit; ready for future GPU pass."""
from __future__ import annotations

import pygame

from rendering import RenderContext

try:
    import moderngl  # type: ignore[import-untyped]
    HAS_MODERNGL = True
except ImportError:
    moderngl = None  # type: ignore[assignment]
    HAS_MODERNGL = False

_logged_shader_mode = False
_offscreen_surface = None
_offscreen_size: tuple[int, int] | None = None


def _get_offscreen_surface(render_ctx: RenderContext) -> pygame.Surface:
    """Return a surface sized to render_ctx; (re)create if size changed."""
    global _offscreen_surface, _offscreen_size
    size = (render_ctx.width, render_ctx.height)
    if _offscreen_surface is None or _offscreen_size != size:
        _offscreen_surface = pygame.Surface(size).convert_alpha()
        _offscreen_surface.fill((0, 0, 0, 255))
        _offscreen_size = size
    return _offscreen_surface


def _render_gameplay_frame(render_ctx, game_state, ctx) -> None:
    """Invoke the normal gameplay renderer into the given render_ctx (caller may pass temp ctx with offscreen screen)."""
    from screens import gameplay as gameplay_screen

    gameplay_ctx = ctx.get("gameplay_ctx") if isinstance(ctx, dict) else getattr(ctx, "gameplay_ctx", None)
    if gameplay_ctx is not None:
        gameplay_screen.render(render_ctx, game_state, gameplay_ctx)


def render_gameplay_with_optional_shaders(render_ctx, game_state, ctx) -> None:
    """
    Wrapper that checks config.use_shaders and HAS_MODERNGL.
    Renders to an offscreen surface, then blits to render_ctx.screen (identical output; hook for future GPU pass).
    """
    global _logged_shader_mode

    config = getattr(ctx, "config", None)
    if config is None and isinstance(ctx, dict):
        app_ctx = ctx.get("app_ctx")
        config = getattr(app_ctx, "config", None) if app_ctx else None
    use_shaders = bool(getattr(config, "use_shaders", False))

    offscreen_surface = _get_offscreen_surface(render_ctx)
    temp_ctx = RenderContext(
        screen=offscreen_surface,
        width=render_ctx.width,
        height=render_ctx.height,
        font=render_ctx.font,
        big_font=render_ctx.big_font,
        small_font=render_ctx.small_font,
    )
    offscreen_surface.fill((0, 0, 0, 255))
    _render_gameplay_frame(temp_ctx, game_state, ctx)
    render_ctx.screen.blit(offscreen_surface, (0, 0))

    if use_shaders and HAS_MODERNGL:
        if not _logged_shader_mode:
            print("rendering_shaders: shader mode requested, but using fallback renderer (no GL integration yet).")
            _logged_shader_mode = True
