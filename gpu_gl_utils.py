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

# u_effect: 0 = shader_test (desaturate), 1 = gameplay (contrast + pulse)
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
    } else {
        float t = 0.5 + 0.5 * sin(u_time * 0.5);
        vec3 base = c.rgb;
        vec3 out_color = mix(base, base * 1.2, t * 0.3);
        fragColor = vec4(clamp(out_color, 0.0, 1.0), 1.0);
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


def get_fullscreen_quad(size: Tuple[int, int]) -> Optional["FullscreenQuad"]:
    ctx = get_gl_context()
    if ctx is None:
        return None
    if size not in _quad_cache:
        _quad_cache[size] = FullscreenQuad(ctx, size)
    else:
        _quad_cache[size].ensure_size(size)
    return _quad_cache[size]
