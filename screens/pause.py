"""Pause screen: handle_events and render. Uses AppContext for display/fonts."""
from __future__ import annotations

import pygame
from constants import STATE_PLAYING, STATE_ENDURANCE, STATE_MENU, pause_options
from context import AppContext
from rendering import draw_centered_text


def handle_events(events, game_state, ctx):
    """
    Process pause-screen events. Mutates game_state.pause_selected.
    Returns dict: {"screen": str|None, "quit": bool, "restart": bool, "restart_to_wave1": bool}.
    """
    out = {"screen": None, "quit": False, "restart": False, "restart_to_wave1": False}
    for event in events:
        if event.type != pygame.KEYDOWN:
            continue
        if event.key == pygame.K_ESCAPE:
            target = game_state.previous_screen or STATE_PLAYING
            if target not in (STATE_PLAYING, STATE_ENDURANCE):
                target = STATE_PLAYING
            out["screen"] = target
            break
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            game_state.pause_selected = (game_state.pause_selected - 1) % len(pause_options)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            game_state.pause_selected = (game_state.pause_selected + 1) % len(pause_options)
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            choice = pause_options[game_state.pause_selected]
            if choice == "Continue":
                target = game_state.previous_screen or STATE_PLAYING
                if target not in (STATE_PLAYING, STATE_ENDURANCE):
                    target = STATE_PLAYING
                out["screen"] = target
            elif choice == "Restart (Wave 1)":
                out["restart_to_wave1"] = True
                out["screen"] = STATE_PLAYING
            elif choice == "Exit to main menu":
                out["screen"] = STATE_MENU
            elif choice == "Quit":
                out["quit"] = True
    return out


def render(app_ctx: AppContext, game_state, screen_ctx) -> None:
    """Draw pause overlay and menu. app_ctx: AppContext (screen, font, big_font, width, height)."""
    screen = app_ctx.screen
    WIDTH = app_ctx.width
    HEIGHT = app_ctx.height
    font = app_ctx.font
    big_font = app_ctx.big_font
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    draw_centered_text(screen, font, big_font, WIDTH, "PAUSED", HEIGHT // 2 - 100, use_big=True)
    y_offset = HEIGHT // 2
    for i, option in enumerate(pause_options):
        color = (255, 255, 0) if i == game_state.pause_selected else (200, 200, 200)
        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == game_state.pause_selected else '  '} {option}", y_offset + i * 50, color)
    draw_centered_text(screen, font, big_font, WIDTH, "Press ENTER to select, ESC to unpause", HEIGHT - 100, (150, 150, 150))
