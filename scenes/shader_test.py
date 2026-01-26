"""ShaderTestScene: minimal placeholder to test shader mode entry. No GPU calls yet."""
from __future__ import annotations

import pygame

from rendering import draw_centered_text


# State id used when this scene is active (game.py treats it like PAUSED/NAME_INPUT for input/render).
SHADER_TEST_STATE_ID = "SHADER_TEST"


class ShaderTestScene:
    """Placeholder scene shown first when use_shaders=True. ESC pops back to gameplay."""

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
        pass

    def render(self, render_ctx, game_state, ctx: dict) -> None:
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
