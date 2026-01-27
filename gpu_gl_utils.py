"""Shared moderngl helpers: context, fullscreen quad geometry, texture, and a basic program.
Used by ShaderTestScene and rendering_shaders for post-process.
"""
from __future__ import annotations

import struct
from typing import Optional, Tuple

try:
    import moderngl  # type: ignore[import-untyped]
    HAS_MODERNGL = True
except ImportError:
    moderngl = None  # type: ignore[assignment]
    HAS_MODERNGL = False

_gl_ctx: Optional["moderngl.Context"] = None

# Fullscreen quad NDC pos+uv, triangle strip (same layout for all callers)
QUAD_POS_UV = struct.pack(
    "16f",
    -1.0, -1.0, 0.0, 0.0,
    1.0, -1.0, 1.0, 0.0,
    -1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0,
)

VERTEX_SHADER = """
#version 330
in vec2 in_pos;
in vec2 in_uv;
out vec2 v_uv;
void main() {
    gl_Position = vec4(in_pos, 0.0, 1.0);
    v_uv = in_uv;
}
"""

# u_effect: 0 = shader_test (desaturate), 1 = gameplay (contrast + pulse), 2 = passthrough/upscale
FRAGMENT_SHADER = """
#version 330
uniform sampler2D u_frame_texture;
uniform float u_time;
uniform int u_effect;
in vec2 v_uv;
out vec4 fragColor;
void main() {
    vec4 c = texture(u_frame_texture, v_uv);
    if (u_effect == 0) {
        float gray = dot(c.rgb, vec3(0.299, 0.587, 0.114));
        vec3 mixed = mix(c.rgb, vec3(gray), 0.3);
        fragColor = vec4(mixed, c.a);
    } else if (u_effect == 1) {
        vec2 centered = v_uv - 0.5;
        float dist = length(centered);
        float vignette = smoothstep(0.7, 0.3, dist);
        float pulse = 0.9 + 0.1 * sin(u_time * 2.0);
        vec3 base = c.rgb * pulse;
        vec3 final_rgb = base * vignette;
        fragColor = vec4(final_rgb, c.a);
    } else {
        fragColor = c;
    }
}
"""


def get_gl_context() -> Optional["moderngl.Context"]:
    global _gl_ctx
    if moderngl is None:
        return None
    if _gl_ctx is None:
        try:
            _gl_ctx = moderngl.create_context()
        except Exception:
            _gl_ctx = None
    return _gl_ctx


class FullscreenQuad:
    """Holds texture, VBO, VAO, and program for a fullscreen quad at a given size."""

    def __init__(self, ctx: "moderngl.Context", size: Tuple[int, int]) -> None:
        self.ctx = ctx
        self.size = size
        self.texture = ctx.texture(size, 4)
        self.vbo = ctx.buffer(QUAD_POS_UV)
        self.program = ctx.program(
            vertex_shader=VERTEX_SHADER,
            fragment_shader=FRAGMENT_SHADER,
        )
        self.vao = ctx.vertex_array(
            self.program,
            [(self.vbo, "2f 2f", "in_pos", "in_uv")],
        )

    def ensure_size(self, size: Tuple[int, int]) -> None:
        if size == self.size:
            return
        try:
            self.texture.release()
        except Exception:
            pass
        self.size = size
        self.texture = self.ctx.texture(size, 4)

    def render(self) -> None:
        if moderngl is not None:
            self.vao.render(moderngl.TRIANGLE_STRIP)


_quad_cache: dict[Tuple[int, int], "FullscreenQuad"] = {}
_upscale_fbo = None
_upscale_fbo_size: Optional[Tuple[int, int]] = None


def gpu_upscale_surface(surface: "object", target_size: Tuple[int, int]) -> Optional["object"]:
    """Upscale a pygame Surface to target_size on the GPU (bilinear). Returns new Surface or None on failure."""
    global _upscale_fbo, _upscale_fbo_size
    try:
        import pygame
    except ImportError:
        return None
    ctx = get_gl_context()
    if ctx is None:
        return None
    src_size = (surface.get_width(), surface.get_height())
    if src_size[0] < 1 or src_size[1] < 1 or target_size[0] < 1 or target_size[1] < 1:
        return None
    quad = get_fullscreen_quad(src_size)
    if quad is None:
        return None
    if _upscale_fbo is None or _upscale_fbo_size != target_size:
        if _upscale_fbo is not None:
            try:
                _upscale_fbo.release()
            except Exception:
                pass
            _upscale_fbo = None
        try:
            out_tex = ctx.texture(target_size, 4)
            _upscale_fbo = ctx.framebuffer(color_attachments=[out_tex])
            _upscale_fbo_size = target_size
        except Exception:
            _upscale_fbo_size = None
            return None
    try:
        tex_bytes = pygame.image.tostring(surface, "RGBA", False)
    except Exception:
        try:
            tex_bytes = bytes(surface.get_view("0"))
        except Exception:
            return None
    quad.texture.write(tex_bytes)
    quad.program["u_effect"] = 2
    quad.texture.use(0)
    quad.program["u_frame_texture"] = 0
    _upscale_fbo.use()
    ctx.viewport = (0, 0, target_size[0], target_size[1])
    _upscale_fbo.clear(0.0, 0.0, 0.0, 1.0)
    quad.render()
    data = _upscale_fbo.read(components=4)
    out_surf = pygame.image.frombuffer(data, target_size, "RGBA")
    out_surf = pygame.transform.flip(out_surf, False, True)
    return out_surf


def get_fullscreen_quad(size: Tuple[int, int]) -> Optional["FullscreenQuad"]:
    ctx = get_gl_context()
    if ctx is None:
        return None
    if size not in _quad_cache:
        _quad_cache[size] = FullscreenQuad(ctx, size)
    else:
        _quad_cache[size].ensure_size(size)
    return _quad_cache[size]
