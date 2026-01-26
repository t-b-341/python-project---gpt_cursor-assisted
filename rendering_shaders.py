"""Optional shader-based gameplay rendering wrapper. Renders to offscreen then blit; ready for future GPU pass."""
from __future__ import annotations

import struct
import time
import pygame

from rendering import RenderContext

try:
    import moderngl  # type: ignore[import-untyped]
    HAS_MODERNGL = True
except ImportError:
    moderngl = None  # type: ignore[assignment]
    HAS_MODERNGL = False

_gl_start_time = time.perf_counter()

# Module-level GL cache for post-process path
_gl_ctx = None
_gl_program = None
_gl_vao = None
_gl_texture = None
_gl_fbo = None
_gl_size: tuple[int, int] | None = None

# Fullscreen quad NDC pos+uv, triangle strip
_QUAD_POS_UV = struct.pack(
    "16f",
    -1.0, -1.0, 0.0, 0.0,
    1.0, -1.0, 1.0, 0.0,
    -1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0,
)

_GL_VERTEX_SHADER = """
#version 330
in vec2 in_pos;
in vec2 in_uv;
out vec2 v_uv;
void main() {
    gl_Position = vec4(in_pos, 0.0, 1.0);
    v_uv = in_uv;
}
"""

_GL_FRAGMENT_SHADER = """
#version 330
uniform sampler2D u_frame_texture;
uniform float u_time;
in vec2 v_uv;
out vec4 fragColor;
void main() {
    float t = 0.5 + 0.5 * sin(u_time * 0.5);
    vec3 base = texture(u_frame_texture, v_uv).rgb;
    vec3 out_color = mix(base, base * 1.2, t * 0.3);
    fragColor = vec4(clamp(out_color, 0.0, 1.0), 1.0);
}
"""


def _init_gl_if_needed(width: int, height: int) -> bool:
    global _gl_ctx, _gl_program, _gl_vao, _gl_texture, _gl_fbo, _gl_size
    if not HAS_MODERNGL or moderngl is None:
        return False
    if _gl_ctx is None:
        try:
            _gl_ctx = moderngl.create_context()
        except Exception:
            _gl_ctx = None
            return False
    if _gl_program is None:
        try:
            _gl_program = _gl_ctx.program(
                vertex_shader=_GL_VERTEX_SHADER,
                fragment_shader=_GL_FRAGMENT_SHADER,
            )
            vbo = _gl_ctx.buffer(_QUAD_POS_UV)
            _gl_vao = _gl_ctx.vertex_array(
                _gl_program,
                [(vbo, "2f 2f", "in_pos", "in_uv")],
            )
        except Exception:
            _gl_program = None
            _gl_vao = None
            return False
    size_changed = _gl_size != (width, height)
    if size_changed or _gl_texture is None:
        try:
            if _gl_fbo is not None:
                try:
                    _gl_fbo.release()
                except Exception:
                    pass
                _gl_fbo = None
            if _gl_texture is not None:
                try:
                    _gl_texture.release()
                except Exception:
                    pass
                _gl_texture = None
            _gl_texture = _gl_ctx.texture((width, height), 4)
            out_tex = _gl_ctx.texture((width, height), 4)
            _gl_fbo = _gl_ctx.framebuffer(color_attachments=[out_tex])
            _gl_size = (width, height)
        except Exception:
            _gl_fbo = None
            _gl_texture = None
            _gl_size = None
            return False
    return _gl_program is not None and _gl_vao is not None and _gl_texture is not None and _gl_fbo is not None


def _gl_postprocess_offscreen_surface(offscreen_surface, render_ctx, ctx) -> bool:
    if not HAS_MODERNGL:
        return False
    try:
        width, height = offscreen_surface.get_size()
        if not _init_gl_if_needed(width, height):
            return False
        try:
            tex_bytes = pygame.image.tostring(offscreen_surface, "RGBA", False)
        except AttributeError:
            tex_bytes = bytes(offscreen_surface.get_view("0"))
        _gl_texture.write(tex_bytes)
        _gl_fbo.use()
        _gl_ctx.viewport = (0, 0, width, height)
        _gl_fbo.clear(0.0, 0.0, 0.0, 1.0)
        _gl_texture.use(0)
        _gl_program["u_frame_texture"] = 0
        now = time.perf_counter()
        elapsed = float(now - _gl_start_time)
        _gl_program["u_time"] = elapsed
        _gl_vao.render(moderngl.TRIANGLE_STRIP)
        data = _gl_fbo.read(components=4)
        out_surf = pygame.image.frombuffer(data, (width, height), "RGBA")
        out_surf = pygame.transform.flip(out_surf, False, True)
        render_ctx.screen.blit(out_surf, (0, 0))
        return True
    except Exception:
        return False


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
    Renders to an offscreen surface, then blits to render_ctx.screen (or runs GL post-process when shaders enabled).
    """
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

    if use_shaders and HAS_MODERNGL:
        ok = _gl_postprocess_offscreen_surface(offscreen_surface, render_ctx, ctx)
        if ok:
            return

    if use_shaders:
        overlay = pygame.Surface(offscreen_surface.get_size(), flags=pygame.SRCALPHA)
        overlay.fill((80, 0, 120, 60))  # RGBA: mild purple tint, low alpha
        offscreen_surface.blit(overlay, (0, 0))
    render_ctx.screen.blit(offscreen_surface, (0, 0))
