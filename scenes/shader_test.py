"""ShaderTestScene: minimal placeholder to test shader mode entry. Optional moderngl fullscreen quad."""
from __future__ import annotations

import struct
import pygame

from rendering import draw_centered_text

try:
    import moderngl  # type: ignore[import-untyped]
    HAS_MODERNGL = True
except ImportError:
    HAS_MODERNGL = False

# State id used when this scene is active (game.py treats it like PAUSED/NAME_INPUT for input/render).
SHADER_TEST_STATE_ID = "SHADER_TEST"

# Fullscreen quad in NDC, triangle strip: (-1,-1), (1,-1), (-1,1), (1,1)
_QUAD_NDC = struct.pack("8f", -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0)

_VERTEX_SHADER = """
#version 330
in vec2 in_position;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

_FRAGMENT_SHADER = """
#version 330
uniform float u_time;
out vec4 fragColor;
void main() {
    float t = 0.5 + 0.5 * sin(u_time);
    vec3 base = vec3(0.2, 0.8, 0.4);
    fragColor = vec4(base * t, 1.0);
}
"""


class ShaderTestScene:
    """Placeholder scene shown first when use_shaders=True. ESC pops back to gameplay."""

    def __init__(self) -> None:
        self._logged = False
        self.time = 0.0
        self.gl = None
        self.program = None
        self.vbo = None
        self.vao = None
        if HAS_MODERNGL:
            try:
                self.gl = moderngl.create_context()
            except Exception:
                self.gl = None
            if self.gl is not None:
                try:
                    self.program = self.gl.program(
                        vertex_shader=_VERTEX_SHADER,
                        fragment_shader=_FRAGMENT_SHADER,
                    )
                    self.vbo = self.gl.buffer(_QUAD_NDC)
                    self.vao = self.gl.vertex_array(
                        self.program,
                        [(self.vbo, "2f", "in_position")],
                    )
                except Exception:
                    self.gl = None
                    self.program = None
                    self.vbo = None
                    self.vao = None

    def state_id(self) -> str:
        return SHADER_TEST_STATE_ID

    def handle_input(self, events, game_state, ctx: dict) -> dict:
        out = {"screen": None, "quit": False, "restart": False, "restart_to_wave1": False, "replay": False, "pop": False}
        for e in events:
            if getattr(e, "type", None) == pygame.KEYDOWN and getattr(e, "key", None) == pygame.K_ESCAPE:
                out["pop"] = True
                break
        return out

    def update(self, dt: float, game_state, ctx: dict) -> None:
        if self.gl is not None:
            self.time += dt

    def render(self, render_ctx, game_state, ctx: dict) -> None:
        if not self._logged:
            if self.gl is not None and self.vao is not None:
                print("ShaderTestScene: moderngl active")
            else:
                print("ShaderTestScene: moderngl not available, using fallback.")
            self._logged = True

        if self.gl is not None and self.program is not None and self.vao is not None:
            self.program["u_time"] = self.time
            self.gl.clear(0.15, 0.15, 0.2, 1.0)
            self.vao.render(moderngl.TRIANGLE_STRIP)
            # Overlay text on top via existing 2D path (render_ctx.screen may not show GL output
            # if context is not the window; drawing anyway keeps UI consistent when it is)
        else:
            render_ctx.screen.fill((30, 30, 45))

        draw_centered_text(
            render_ctx.screen,
            render_ctx.font,
            render_ctx.big_font,
            render_ctx.width,
            "Shader Test Scene (Shaders OFF — placeholder)",
            render_ctx.height // 2 - 30,
            color=(220, 220, 220),
            use_big=False,
        )
        draw_centered_text(
            render_ctx.screen,
            render_ctx.font,
            render_ctx.big_font,
            render_ctx.width,
            "Press ESC to return to gameplay",
            render_ctx.height // 2 + 30,
            color=(160, 160, 160),
        )

    def on_enter(self, game_state, ctx: dict) -> None:
        pass

    def on_exit(self, game_state, ctx: dict) -> None:
        pass
