"""High scores screen: handle_events and render."""
import pygame
from constants import STATE_PLAYING


def handle_events(events, game_state, ctx):
    """On ESC quit; on Space/Enter replay (new run from wave 1). Returns screen, quit, replay."""
    out = {"screen": None, "quit": False, "restart": False, "replay": False}
    for event in events:
        if event.type != pygame.KEYDOWN:
            continue
        if event.key == pygame.K_ESCAPE:
            out["quit"] = True
            break
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            out["replay"] = True
            out["screen"] = STATE_PLAYING
            break
    return out


def render(screen, game_state, ctx):
    """Draw high scores list. ctx must provide get_high_scores, font, big_font, small_font, WIDTH, HEIGHT."""
    WIDTH = ctx["WIDTH"]
    HEIGHT = ctx["HEIGHT"]
    font = ctx["font"]
    big_font = ctx["big_font"]
    small_font = ctx.get("small_font", font)
    get_high_scores = ctx["get_high_scores"]

    screen.fill((20, 20, 40))
    title = big_font.render("HIGH SCORES", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    scores = get_high_scores(10)
    y_offset = 150
    if scores:
        header = font.render("Rank  Name          Score    Waves  Time    Kills   Difficulty", True, (200, 200, 200))
        screen.blit(header, (WIDTH // 2 - header.get_width() // 2, y_offset))
        y_offset += 40
        for i, score_data in enumerate(scores, 1):
            name = score_data["name"][:12]
            score_val = score_data["score"]
            waves = score_data["waves"]
            time_val = score_data["time"]
            minutes = int(time_val // 60)
            seconds = int(time_val % 60)
            kills = score_data["kills"]
            diff = score_data["difficulty"]
            rank_color = (255, 215, 0) if i == 1 else (255, 255, 255) if i <= 3 else (200, 200, 200)
            text = font.render(f"{i:2d}.  {name:12s}  {score_val:8d}  {waves:3d}  {minutes:02d}:{seconds:02d}  {kills:5d}  {diff:8s}", True, rank_color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 35
    else:
        no_scores = font.render("No high scores yet!", True, (150, 150, 150))
        screen.blit(no_scores, (WIDTH // 2 - no_scores.get_width() // 2, y_offset))

    instruction = small_font.render("Press SPACE/ENTER to play again, ESC to exit", True, (100, 100, 100))
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, HEIGHT - 50))
