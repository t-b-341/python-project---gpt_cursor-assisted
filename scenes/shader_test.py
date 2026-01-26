"""ShaderTestScene: Pygame 2D -> moderngl texture -> fullscreen quad with post-process."""
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

# Fallback size when window size is not available in __init__ (e.g. 800x600).
_OFFSCREEN_SIZE = (800, 600)

# Fullscreen quad in NDC, triangle strip: pos (x,y) + texcoord (u,v) per vertex
# (-1,-1,0,0), (1,-1,1,0), (-1,1,0,1), (1,1,1,1)
_QUAD_POS_UV = struct.pack(
    "16f",
    -1.0, -1.0, 0.0, 0.0,
     1.0, -1.0, 1.0, 0.0,
    -1.0,  1.0, 0.0, 1.0,
     1.0,  1.0, 1.0, 1.0,
)

_VERTEX_SHADER = """
#version 330
in vec2 in_position;
in vec2 in_texcoord;
out vec2 v_texcoord;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
    v_texcoord = in_texcoord;
}
"""

_FRAGMENT_SHADER = """
#version 330
uniform sampler2D u_frame_texture;
uniform float u_time;
in vec2 v_texcoord;
out vec4 fragColor;
void main() {
    vec4 color = texture(u_frame_texture, v_texcoord);
    float gray = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    vec3 mixed = mix(color.rgb, vec3(gray), 0.3);
    fragColor = vec4(mixed, color.a);
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
        self.offscreen_surface = None
        self.frame_texture = None
        if HAS_MODERNGL:
            try:
                self.gl = moderngl.create_context()
            except Exception:
                self.gl = None
            if self.gl is not None:
                try:
                    w, h = _OFFSCREEN_SIZE
                    self.offscreen_surface = pygame.Surface(_OFFSCREEN_SIZE)
                    self.program = self.gl.program(
                        vertex_shader=_VERTEX_SHADER,
                        fragment_shader=_FRAGMENT_SHADER,
                    )
                    self.vbo = self.gl.buffer(_QUAD_POS_UV)
                    self.vao = self.gl.vertex_array(
                        self.program,
                        [(self.vbo, "2f 2f", "in_position", "in_texcoord")],
                    )
                    self.frame_texture = self.gl.texture((w, h), 4)
                except Exception:
                    self.gl = None
                    self.program = None
                    self.vbo = None
                    self.vao = None
                    self.offscreen_surface = None
                    self.frame_texture = None

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

        if self.gl is not None and self.program is not None and self.vao is not None and self.offscreen_surface is not None and self.frame_texture is not None:
            # 1) Draw Pygame-style content into offscreen surface
            w, h = self.offscreen_surface.get_size()
            self.offscreen_surface.fill((30, 30, 45))
            draw_centered_text(
                self.offscreen_surface,
                render_ctx.font,
                render_ctx.big_font,
                w,
                "Shader Test Scene (Shaders OFF — placeholder)",
                h // 2 - 30,
                color=(220, 220, 220),
                use_big=False,
            )
            draw_centered_text(
                self.offscreen_surface,
                render_ctx.font,
                render_ctx.big_font,
                w,
                "Press ESC to return to gameplay",
                h // 2 + 30,
                color=(160, 160, 160),
            )
            # 2) Upload to GL texture (RGBA)
            try:
                tex_bytes = pygame.image.tostring(self.offscreen_surface, "RGBA", False)
            except AttributeError:
                tex_bytes = bytes(self.offscreen_surface.get_view("0"))
            self.frame_texture.write(tex_bytes)
            # 3) Draw fullscreen quad sampling texture with post-process
            self.program["u_time"] = self.time
            self.frame_texture.use(0)
            self.program["u_frame_texture"] = 0
            self.gl.clear(0.15, 0.15, 0.2, 1.0)
            self.vao.render(moderngl.TRIANGLE_STRIP)
        else:
            # Fallback: draw directly to screen
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
