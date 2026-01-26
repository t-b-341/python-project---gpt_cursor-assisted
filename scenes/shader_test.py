"""ShaderTestScene: Pygame 2D -> moderngl texture -> fullscreen quad with post-process."""
from __future__ import annotations

import pygame

from rendering import draw_centered_text

try:
    from gpu_gl_utils import get_gl_context, get_fullscreen_quad, HAS_MODERNGL
except ImportError:
    HAS_MODERNGL = False
    get_gl_context = None  # type: ignore[assignment]
    get_fullscreen_quad = None  # type: ignore[assignment]

# State id used when this scene is active (game.py treats it like PAUSED/NAME_INPUT for input/render).
SHADER_TEST_STATE_ID = "SHADER_TEST"


class ShaderTestScene:
    """Placeholder scene shown first when use_shaders=True. ESC pops back to gameplay."""

    def __init__(self) -> None:
        self._logged = False
        self.time = 0.0
        self.gl = get_gl_context() if (get_gl_context is not None and HAS_MODERNGL) else None
        self.quad = None  # FullscreenQuad from get_fullscreen_quad, set in render
        self.offscreen_surface = None

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
            if self.gl is not None and get_fullscreen_quad is not None:
                q = get_fullscreen_quad((render_ctx.width, render_ctx.height))
                if q is not None:
                    print("ShaderTestScene: moderngl active")
                else:
                    print("ShaderTestScene: moderngl not available, using fallback.")
            else:
                print("ShaderTestScene: moderngl not available, using fallback.")
            self._logged = True

        target_size = (render_ctx.width, render_ctx.height)
        quad = get_fullscreen_quad(target_size) if get_fullscreen_quad is not None else None
        if self.gl is not None and quad is not None:
            if self.offscreen_surface is None or self.offscreen_surface.get_size() != target_size:
                self.offscreen_surface = pygame.Surface(target_size)

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
            try:
                tex_bytes = pygame.image.tostring(self.offscreen_surface, "RGBA", False)
            except AttributeError:
                tex_bytes = bytes(self.offscreen_surface.get_view("0"))
            quad.texture.write(tex_bytes)
            quad.program["u_effect"] = 0
            quad.program["u_time"] = self.time
            quad.texture.use(0)
            quad.program["u_frame_texture"] = 0
            self.gl.viewport = (0, 0, render_ctx.width, render_ctx.height)
            self.gl.clear(0.15, 0.15, 0.2, 1.0)
            quad.render()
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
