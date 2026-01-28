"""Pause screen: handle_events and render. Uses RenderContext for display/fonts."""
from __future__ import annotations

import pygame
from constants import STATE_PLAYING, STATE_ENDURANCE, STATE_MENU, pause_options
from rendering import RenderContext, draw_centered_text


def handle_events(events, game_state, ctx):
    """
    Process pause-screen events. Mutates game_state.ui.pause_selected.
    Returns dict: {"screen": str|None, "quit": bool, "restart": bool, "restart_to_wave1": bool}.
    """
    out = {"screen": None, "quit": False, "restart": False, "restart_to_wave1": False}
    app_ctx = ctx.get("app_ctx") if isinstance(ctx, dict) else None
    cfg = getattr(app_ctx, "config", None) if app_ctx else None
    if game_state is None:
        return out
    submenu = game_state.ui.pause_submenu

    for event in events:
        if not hasattr(event, "type") or event.type != pygame.KEYDOWN:
            continue
        if submenu == "shaders":
            # Debug: verify we're in shader submenu
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                print(f"[Pause Shader Submenu] Processing {event.key} in submenu='{submenu}'")
            # Ensure row is initialized
            if game_state is not None:
                if not hasattr(game_state.ui, 'pause_shader_options_row'):
                    game_state.ui.pause_shader_options_row = 0
                row = game_state.ui.pause_shader_options_row
            else:
                row = 0
            
            _pp = ["none", "pause_dim_vignette"]
            _gp = ["none", "gameplay_subtle_vignette", "gameplay_retro"]
            
            if event.key == pygame.K_ESCAPE:
                if game_state is not None:
                    game_state.ui.pause_submenu = None
                break
            elif event.key in (pygame.K_UP, pygame.K_w):
                if game_state is not None:
                    # Ensure row is initialized
                    if not hasattr(game_state.ui, 'pause_shader_options_row'):
                        game_state.ui.pause_shader_options_row = 0
                    current = game_state.ui.pause_shader_options_row
                    new = (current - 1) % 4
                    game_state.ui.pause_shader_options_row = new
                    print(f"[Pause Shader Submenu] UP: row {current} -> {new}")
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                if game_state is not None:
                    # Ensure row is initialized
                    if not hasattr(game_state.ui, 'pause_shader_options_row'):
                        game_state.ui.pause_shader_options_row = 0
                    current = game_state.ui.pause_shader_options_row
                    new = (current + 1) % 4
                    game_state.ui.pause_shader_options_row = new
                    print(f"[Pause Shader Submenu] DOWN: row {current} -> {new}")
            elif event.key in (pygame.K_LEFT, pygame.K_a) and cfg is not None:
                # Refresh row value in case it was just updated
                row = game_state.ui.pause_shader_options_row if game_state is not None else 0
                if row == 0:
                    cfg.enable_gameplay_shaders = not cfg.enable_gameplay_shaders
                elif row == 1:
                    cfg.enable_pause_shaders = not cfg.enable_pause_shaders
                elif row == 2:
                    cur = getattr(cfg, "gameplay_shader_profile", "none")
                    i = (_gp.index(cur) if cur in _gp else 0) - 1
                    cfg.gameplay_shader_profile = _gp[i % len(_gp)]
                elif row == 3:
                    cur = getattr(cfg, "pause_shader_profile", "none")
                    i = (_pp.index(cur) if cur in _pp else 0) - 1
                    cfg.pause_shader_profile = _pp[i % len(_pp)]
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and cfg is not None:
                # Refresh row value in case it was just updated
                row = game_state.ui.pause_shader_options_row if game_state is not None else 0
                if row == 0:
                    cfg.enable_gameplay_shaders = not cfg.enable_gameplay_shaders
                elif row == 1:
                    cfg.enable_pause_shaders = not cfg.enable_pause_shaders
                elif row == 2:
                    cur = getattr(cfg, "gameplay_shader_profile", "none")
                    i = (_gp.index(cur) if cur in _gp else 0) + 1
                    cfg.gameplay_shader_profile = _gp[i % len(_gp)]
                elif row == 3:
                    cur = getattr(cfg, "pause_shader_profile", "none")
                    i = (_pp.index(cur) if cur in _pp else 0) + 1
                    cfg.pause_shader_profile = _pp[i % len(_pp)]
            continue
        
        # Handle ESCAPE key
        if event.key == pygame.K_ESCAPE:
            if game_state is not None:
                target = game_state.previous_screen or STATE_PLAYING
            else:
                target = STATE_PLAYING
            if target not in (STATE_PLAYING, STATE_ENDURANCE):
                target = STATE_PLAYING
            out["screen"] = target
            break
        
        # Handle navigation keys (only if not in submenu)
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            if game_state is not None:
                current = game_state.ui.pause_selected
                new = (current - 1) % len(pause_options)
                game_state.ui.pause_selected = new
                # Debug: verify update
                if game_state.ui.pause_selected != new:
                    print(f"[Pause] Warning: pause_selected not updated correctly: expected {new}, got {game_state.ui.pause_selected}")
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if game_state is not None:
                current = game_state.ui.pause_selected
                new = (current + 1) % len(pause_options)
                game_state.ui.pause_selected = new
                # Debug: verify update
                if game_state.ui.pause_selected != new:
                    print(f"[Pause] Warning: pause_selected not updated correctly: expected {new}, got {game_state.ui.pause_selected}")
        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            if game_state is None:
                continue
            choice = pause_options[game_state.ui.pause_selected]
            if choice == "Continue":
                if game_state is not None:
                    target = game_state.previous_screen or STATE_PLAYING
                else:
                    target = STATE_PLAYING
                if target not in (STATE_PLAYING, STATE_ENDURANCE):
                    target = STATE_PLAYING
                out["screen"] = target
            elif choice == "Restart (Wave 1)":
                out["restart_to_wave1"] = True
                out["screen"] = STATE_PLAYING
            elif choice == "Shader options":
                if game_state is not None:
                    game_state.ui.pause_submenu = "shaders"
                    # Initialize shader options row when entering submenu
                    if not hasattr(game_state.ui, 'pause_shader_options_row'):
                        game_state.ui.pause_shader_options_row = 0
                    else:
                        game_state.ui.pause_shader_options_row = 0  # Reset to first option
            elif choice == "Exit to main menu":
                out["screen"] = STATE_MENU
            elif choice == "Quit":
                out["quit"] = True
    return out


def render(render_ctx: RenderContext, game_state, screen_ctx) -> None:
    """Draw pause overlay and menu. render_ctx: screen, fonts, width, height."""
    screen = render_ctx.screen
    WIDTH = render_ctx.width
    HEIGHT = render_ctx.height
    font = render_ctx.font
    big_font = render_ctx.big_font
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    if game_state is None:
        return
    submenu = game_state.ui.pause_submenu
    if submenu == "shaders":
        app_ctx = screen_ctx.get("app_ctx") if isinstance(screen_ctx, dict) else None
        cfg = getattr(app_ctx, "config", None) if app_ctx else None
        # Ensure row is initialized
        if not hasattr(game_state.ui, 'pause_shader_options_row'):
            game_state.ui.pause_shader_options_row = 0
        row = game_state.ui.pause_shader_options_row
        if cfg is not None:
            lines = [
                f"Gameplay Shaders: {'On' if getattr(cfg, 'enable_gameplay_shaders', False) else 'Off'}",
                f"Pause Shaders: {'On' if getattr(cfg, 'enable_pause_shaders', False) else 'Off'}",
                f"Gameplay Profile: {getattr(cfg, 'gameplay_shader_profile', 'none')}",
                f"Pause Profile: {getattr(cfg, 'pause_shader_profile', 'none')}",
            ]
        else:
            lines = ["Gameplay Shaders", "Pause Shaders", "Gameplay Profile", "Pause Profile"]
        draw_centered_text(screen, font, big_font, WIDTH, "Shader options", HEIGHT // 2 - 120, use_big=True)
        for i, line in enumerate(lines):
            color = (255, 255, 0) if i == row else (200, 200, 200)
            draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == row else '  '} {line}", HEIGHT // 2 - 60 + i * 40, color)
        draw_centered_text(screen, font, big_font, WIDTH, "LEFT/RIGHT change value, ESC back", HEIGHT - 80, (150, 150, 150))
        return

    draw_centered_text(screen, font, big_font, WIDTH, "PAUSED", HEIGHT // 2 - 100, use_big=True)
    y_offset = HEIGHT // 2
    pause_selected = game_state.ui.pause_selected if game_state is not None else 0
    for i, option in enumerate(pause_options):
        color = (255, 255, 0) if i == pause_selected else (200, 200, 200)
        draw_centered_text(screen, font, big_font, WIDTH, f"{'->' if i == pause_selected else '  '} {option}", y_offset + i * 50, color)
    draw_centered_text(screen, font, big_font, WIDTH, "Press ENTER to select, ESC to unpause", HEIGHT - 100, (150, 150, 150))
