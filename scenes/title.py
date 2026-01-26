"""TitleScene: title screen and quit-confirm. ESC toggles quit dialog; Enter/Space to options."""
from __future__ import annotations

import pygame

from constants import STATE_MENU, STATE_TITLE
from rendering import RenderContext, draw_centered_text


class TitleScene:
    """Title screen. Enter/Space -> MENU; ESC -> quit confirm or stay."""

    def state_id(self) -> str:
        return STATE_TITLE

    def handle_input(self, events, game_state, ctx: dict) -> dict:
        out = {"screen": None, "quit": False, "restart": False, "restart_to_wave1": False, "replay": False, "pop": False}
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                if game_state.title_confirm_quit:
                    game_state.title_confirm_quit = False
                else:
                    game_state.title_confirm_quit = True
                continue
            if game_state.title_confirm_quit:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_y):
                    out["quit"] = True
                    return out
                if event.key == pygame.K_n:
                    game_state.title_confirm_quit = False
            else:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    out["screen"] = STATE_MENU
                    return out
        return out

    def update(self, dt: float, game_state, ctx: dict) -> None:
        pass

    def render(self, render_ctx: RenderContext, game_state, ctx: dict) -> None:
        screen = render_ctx.screen
        w, h = render_ctx.width, render_ctx.height
        font, big_font = render_ctx.font, render_ctx.big_font
        if game_state.title_confirm_quit:
            draw_centered_text(screen, font, big_font, w, "Are you sure you want to exit?", h // 2 - 40, color=(220, 220, 220))
            draw_centered_text(screen, font, big_font, w, "ENTER or Y to quit", h // 2 + 20, (180, 180, 180))
            draw_centered_text(screen, font, big_font, w, "ESC or N to stay", h // 2 + 60, (180, 180, 180))
        else:
            draw_centered_text(screen, font, big_font, w, "GAME", h // 2 - 80, color=(220, 220, 220), use_big=True)
            draw_centered_text(screen, font, big_font, w, "Main Menu", h // 2 - 30, (180, 180, 180))
            draw_centered_text(screen, font, big_font, w, "Press ENTER or SPACE for options", h // 2 + 30, (180, 180, 180))
            draw_centered_text(screen, font, big_font, w, "ESC to quit", h // 2 + 70, (180, 180, 180))

    def on_enter(self, game_state, ctx: dict) -> None:
        pass

    def on_exit(self, game_state, ctx: dict) -> None:
        pass
