"""Name input screen: handle_events and render."""
import pygame
from constants import STATE_HIGH_SCORES


def handle_events(events, game_state, ctx):
    """
    Handle TEXTINPUT (append to player_name_input), KEYDOWN Backspace/Return/ESC.
    save_high_score and transition to HIGH_SCORES are done by caller using ctx["save_high_score"] and difficulty.
    Returns {"screen": str|None, "quit": bool, "restart": False}.
    """
    out = {"screen": None, "quit": False, "restart": False}
    save_high_score = ctx.get("save_high_score")
    difficulty = ctx.get("difficulty", "NORMAL")

    for event in events:
        if event.type == pygame.TEXTINPUT:
            if len(game_state.player_name_input) < 20:
                game_state.player_name_input += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                game_state.player_name_input = game_state.player_name_input[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if game_state.player_name_input.strip() and save_high_score:
                    save_high_score(
                        game_state.player_name_input.strip(),
                        game_state.final_score_for_high_score,
                        game_state.wave_number - 1,
                        game_state.survival_time,
                        game_state.enemies_killed,
                        difficulty,
                    )
                out["screen"] = STATE_HIGH_SCORES
                game_state.name_input_active = False
            elif event.key == pygame.K_ESCAPE:
                if game_state.player_name_input.strip() and save_high_score:
                    save_high_score(
                        game_state.player_name_input.strip(),
                        game_state.final_score_for_high_score,
                        game_state.wave_number - 1,
                        game_state.survival_time,
                        game_state.enemies_killed,
                        difficulty,
                    )
                out["screen"] = STATE_HIGH_SCORES
                game_state.name_input_active = False
    return out


def render(screen, game_state, ctx):
    """Draw name input prompt and current text."""
    WIDTH = ctx["WIDTH"]
    HEIGHT = ctx["HEIGHT"]
    font = ctx["font"]
    big_font = ctx["big_font"]
    small_font = ctx.get("small_font", font)

    screen.fill((20, 20, 40))
    title = big_font.render("ENTER YOUR NAME", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))

    display_text = game_state.player_name_input + ("_" if int(game_state.run_time * 2) % 2 == 0 else " ")
    input_surface = font.render(display_text, True, (255, 255, 255))
    screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT // 2))

    score_text = font.render(f"Score: {game_state.final_score_for_high_score}", True, (200, 200, 200))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))

    instruction1 = small_font.render("Type your name and press ENTER to save", True, (150, 150, 150))
    instruction2 = small_font.render("Press ESC to skip", True, (150, 150, 150))
    screen.blit(instruction1, (WIDTH // 2 - instruction1.get_width() // 2, HEIGHT // 2 + 100))
    screen.blit(instruction2, (WIDTH // 2 - instruction2.get_width() // 2, HEIGHT // 2 + 125))
