"""
HUD/UI rendering during gameplay.
Split into render_hud (health, score, metrics, cooldown bars) and render_overlays
(damage numbers, defeat/pickup messages, wave countdown). Read state only.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pygame

from constants import STATE_PLAYING, AIM_ARROWS
from rendering import RenderContext, draw_health_bar, draw_centered_text, render_hud_text

if TYPE_CHECKING:
    from state import GameState


def render_hud(state: "GameState", ctx: dict, render_ctx: RenderContext) -> None:
    """Draw HUD layer: entity health bars, score, metrics, and cooldown bars."""
    if not ctx or not render_ctx:
        return
    screen = render_ctx.screen
    font, big_font, small_font = render_ctx.font, render_ctx.big_font, render_ctx.small_font
    WIDTH, HEIGHT = render_ctx.width, render_ctx.height
    ui_show_health_bars = ctx.get("ui_show_health_bars", True)
    ui_show_hud = ctx.get("ui_show_hud", True)
    ui_show_metrics = ctx.get("ui_show_metrics", True)
    if not font or not big_font or not small_font:
        return
    _draw_entity_health_bars(screen, state, ui_show_health_bars)
    if ui_show_hud:
        _draw_score(screen, state, big_font, WIDTH)
        if ui_show_metrics:
            _draw_metrics_and_bars(screen, state, ctx, font, small_font, WIDTH, HEIGHT)


def render_overlays(state: "GameState", ctx: dict, render_ctx: RenderContext) -> None:
    """Draw overlay layer: damage numbers, defeat/pickup messages, wave countdown, wave-reset debug."""
    if not ctx or not render_ctx:
        return
    screen = render_ctx.screen
    font, big_font, small_font = render_ctx.font, render_ctx.big_font, render_ctx.small_font
    WIDTH, HEIGHT = render_ctx.width, render_ctx.height
    ui_show_metrics = ctx.get("ui_show_metrics", True)
    if not font or not small_font:
        return
    _draw_damage_numbers(screen, state, font, small_font)
    _draw_defeat_messages(screen, state, small_font, WIDTH, HEIGHT)
    _draw_weapon_pickup_messages(screen, state, font, WIDTH, HEIGHT)
    _draw_wave_countdown(screen, state, font, big_font, WIDTH, HEIGHT)
    if ui_show_metrics:
        _draw_wave_reset_debug(screen, state, small_font, WIDTH, HEIGHT)


def render(state: "GameState", screen: pygame.Surface, ctx: dict) -> None:
    """Draw all gameplay HUD/UI (HUD + overlays). Backward compat: builds RenderContext from (screen, ctx)."""
    if not ctx:
        return
    render_ctx = RenderContext.from_screen_and_ctx(screen, ctx)
    render_hud(state, ctx, render_ctx)
    render_overlays(state, ctx, render_ctx)


def _draw_entity_health_bars(screen: pygame.Surface, state, show: bool) -> None:
    if not show:
        return
    for friendly in getattr(state, "friendly_ai", []):
        if friendly.get("hp", 0) > 0:
            r = friendly.get("rect")
            if r:
                draw_health_bar(screen, r.x, r.y - 10, r.w, 5, friendly["hp"], friendly.get("max_hp", friendly["hp"]))
    for enemy in getattr(state, "enemies", []):
        if enemy.get("hp", 0) > 0:
            r = enemy.get("rect")
            if r:
                draw_health_bar(screen, r.x, r.y - 10, r.w, 5, enemy["hp"], enemy.get("max_hp", enemy["hp"]))


def _draw_score(screen: pygame.Surface, state, big_font, WIDTH: int) -> None:
    score_text = f"Score: {state.score}"
    score_surface = big_font.render(score_text, True, (255, 255, 0))
    outline_surface = big_font.render(score_text, True, (0, 0, 0))
    score_x = WIDTH // 2 - score_surface.get_width() // 2
    score_y = 10
    for dx, dy in [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]:
        screen.blit(outline_surface, (score_x + dx, score_y + dy))
    screen.blit(score_surface, (score_x, score_y))


def _draw_metrics_and_bars(
    screen: pygame.Surface, state, ctx: dict,
    font, small_font, WIDTH: int, HEIGHT: int,
) -> None:
    overshield_max = ctx.get("overshield_max", state.player_max_hp)
    grenade_cooldown = ctx.get("grenade_cooldown", 5.0)
    missile_cooldown = ctx.get("missile_cooldown", 8.0)
    ally_drop_cooldown = ctx.get("ally_drop_cooldown", 30.0)
    overshield_recharge_cooldown = ctx.get("overshield_recharge_cooldown", 60.0)
    shield_duration = ctx.get("shield_duration", 3.0)
    aiming_mode = ctx.get("aiming_mode", "MOUSE")
    current_state = ctx.get("current_state", "")

    y_pos = 10
    y_pos = render_hud_text(screen, font, f"HP: {state.player_hp}/{state.player_max_hp}", y_pos)
    # Armor/overshield is shown on the armor bar above the health bar; no extra line here
    y_pos = render_hud_text(screen, font, f"Wave: {state.wave_number} | Level: {state.current_level}", y_pos)
    minutes = int(state.survival_time // 60)
    seconds = int(state.survival_time % 60)
    y_pos = render_hud_text(screen, font, f"Time: {minutes:02d}:{seconds:02d}", y_pos)
    if current_state == STATE_PLAYING:
        y_pos = render_hud_text(screen, font, f"Lives: {state.lives}", y_pos)
    y_pos = render_hud_text(screen, font, f"Enemies: {len(state.enemies)}", y_pos)
    y_pos = render_hud_text(screen, font, f"Weapon: {state.current_weapon_mode.upper()}", y_pos)
    if state.shield_active:
        y_pos = render_hud_text(screen, font, "SHIELD ACTIVU", y_pos, (255, 100, 100))
    if state.random_damage_multiplier != 1.0:
        multiplier_color = (255, 255, 0) if state.random_damage_multiplier > 1.0 else (255, 150, 150)
        y_pos = render_hud_text(screen, font, f"DMG MULT: {state.random_damage_multiplier:.2f}x", y_pos, multiplier_color)

    health_bar_x = 10
    health_bar_y = HEIGHT - 80
    health_bar_height = 20
    health_bar_width = 300
    armor_health_gap = 6  # pixels between armor bar bottom and health bar top

    if state.overshield > 0:
        # Armor bar: same length (width) and height as health, placed slightly above
        armor_bar_y = health_bar_y - health_bar_height - armor_health_gap
        overshield_fill = int((state.overshield / max(1, overshield_max)) * health_bar_width)
        pygame.draw.rect(screen, (60, 60, 60), (health_bar_x, armor_bar_y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (255, 150, 0), (health_bar_x, armor_bar_y, overshield_fill, health_bar_height))
        pygame.draw.rect(screen, (20, 20, 20), (health_bar_x, armor_bar_y, health_bar_width, health_bar_height), 2)
        overshield_text = small_font.render(f"Armor: {int(state.overshield)}/{int(overshield_max)}", True, (255, 255, 255))
        screen.blit(overshield_text, (health_bar_x + 5, armor_bar_y + 2))

    health_fill = int((state.player_hp / state.player_max_hp) * health_bar_width)
    pygame.draw.rect(screen, (60, 60, 60), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, (100, 255, 100), (health_bar_x, health_bar_y, health_fill, health_bar_height))
    pygame.draw.rect(screen, (20, 20, 20), (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
    health_text = small_font.render(f"HP: {int(state.player_hp)}/{int(state.player_max_hp)}", True, (255, 255, 255))
    screen.blit(health_text, (health_bar_x + 5, health_bar_y + 2))

    bar_y = HEIGHT - 30
    bar_height = 20
    bar_width = min(200, (WIDTH - 60) // 5)

    grenade_progress = min(1.0, state.grenade_time_since_used / grenade_cooldown)
    grenade_x = 10
    pygame.draw.rect(screen, (60, 60, 60), (grenade_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (200, 100, 255) if grenade_progress >= 1.0 else (255, 50, 50),
                     (grenade_x, bar_y, int(bar_width * grenade_progress), bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (grenade_x, bar_y, bar_width, bar_height), 2)
    screen.blit(small_font.render("BOMB (E)", True, (255, 255, 255)), (grenade_x + 5, bar_y + 2))

    missile_progress = min(1.0, state.missile_time_since_used / missile_cooldown)
    missile_x = grenade_x + bar_width + 10
    pygame.draw.rect(screen, (60, 60, 60), (missile_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (255, 200, 0) if missile_progress >= 1.0 else (100, 100, 100),
                     (missile_x, bar_y, int(bar_width * missile_progress), bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (missile_x, bar_y, bar_width, bar_height), 2)
    screen.blit(small_font.render("MISSILE (R)", True, (255, 255, 255)), (missile_x + 5, bar_y + 2))

    ally_progress = min(1.0, state.ally_drop_timer / ally_drop_cooldown)
    ally_x = missile_x + bar_width + 10
    pygame.draw.rect(screen, (60, 60, 60), (ally_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, (200, 100, 255) if ally_progress >= 1.0 else (100, 100, 100),
                     (ally_x, bar_y, int(bar_width * ally_progress), bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (ally_x, bar_y, bar_width, bar_height), 2)
    screen.blit(small_font.render("ALLY DROP (Q)", True, (255, 255, 255)), (ally_x + 5, bar_y + 2))

    overshield_progress = min(1.0, state.overshield_recharge_timer / overshield_recharge_cooldown)
    overshield_x = ally_x + bar_width + 10
    pygame.draw.rect(screen, (60, 60, 60), (overshield_x, bar_y, bar_width, bar_height))
    # Use cyan when ready so it’s distinct from the orange armor meter (current overshield)
    overshield_bar_color = (100, 220, 255) if overshield_progress >= 1.0 else (100, 100, 100)
    pygame.draw.rect(screen, overshield_bar_color,
                     (overshield_x, bar_y, int(bar_width * overshield_progress), bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (overshield_x, bar_y, bar_width, bar_height), 2)
    screen.blit(small_font.render("OVERSHIELD (TAB)", True, (255, 255, 255)), (overshield_x + 5, bar_y + 2))

    if state.shield_active:
        shield_progress = min(1.0, state.shield_duration_remaining / shield_duration)
    else:
        if getattr(state, "shield_recharge_cooldown", 0) > 0:
            shield_progress = min(1.0, state.shield_recharge_timer / state.shield_recharge_cooldown)
        else:
            shield_progress = 1.0
    shield_ready = shield_progress >= 1.0 and not state.shield_active
    shield_x = overshield_x + bar_width + 10
    pygame.draw.rect(screen, (60, 60, 60), (shield_x, bar_y, bar_width, bar_height))
    if state.shield_active:
        shield_color = (255, 255, 100)
    elif shield_ready:
        shield_color = (100, 200, 255)
    else:
        shield_color = (255, 50, 50)
    pygame.draw.rect(screen, shield_color, (shield_x, bar_y, int(bar_width * shield_progress), bar_height))
    pygame.draw.rect(screen, (255, 255, 255), (shield_x, bar_y, bar_width, bar_height), 2)
    screen.blit(small_font.render("SHIELD (LALT)", True, (255, 255, 255)), (shield_x + 5, bar_y + 2))

    controls_y = HEIGHT - 10
    if aiming_mode == AIM_ARROWS:
        controls_text = "WASD: Move | Arrow Keys: Aim & Shoot | E: Bomb | R: Missile | Q: Ally Drop | TAB: Overshield | LALT: Shield | SPACE: Dash"
    else:
        controls_text = "WASD: Move | Mouse + Click: Aim & Shoot | E: Bomb | R: Missile | Q: Ally Drop | TAB: Overshield | LALT: Shield | SPACE: Dash"
    controls_surf = small_font.render(controls_text, True, (150, 150, 150))
    controls_rect = controls_surf.get_rect(center=(WIDTH // 2, controls_y))
    screen.blit(controls_surf, controls_rect)


def _draw_damage_numbers(screen: pygame.Surface, state, font, small_font) -> None:
    for dmg_num in getattr(state, "damage_numbers", []):
        if dmg_num.get("timer", 0) > 0:
            alpha = int(255 * (dmg_num["timer"] / 2.0))
            color = (*dmg_num["color"][:3], alpha) if len(dmg_num.get("color", (0, 0, 0))) > 3 else dmg_num.get("color", (255, 255, 255))
            if "value" in dmg_num:
                text_surf = font.render(dmg_num["value"], True, color[:3])
            else:
                text_surf = small_font.render(str(int(dmg_num.get("damage", 0))), True, color[:3])
            screen.blit(text_surf, (dmg_num["x"], dmg_num["y"]))


def _draw_defeat_messages(screen: pygame.Surface, state, small_font, WIDTH: int, HEIGHT: int) -> None:
    defeat_y_start = HEIGHT - 100
    messages = getattr(state, "enemy_defeat_messages", [])[-5:]
    for i, msg in enumerate(messages):
        if msg.get("timer", 0) > 0:
            enemy_type = msg.get("enemy_type", "enemy")
            text = f"{enemy_type.upper()} DEFEATED!"
            text_surf = small_font.render(text, True, (255, 200, 100))
            text_rect = text_surf.get_rect()
            x_pos = WIDTH - text_rect.width - 20
            y_pos = defeat_y_start - (i * 25)
            screen.blit(text_surf, (x_pos, y_pos))


def _draw_weapon_pickup_messages(screen: pygame.Surface, state, font, WIDTH: int, HEIGHT: int) -> None:
    messages = [m for m in getattr(state, "weapon_pickup_messages", []) if m.get("timer", 0) > 0]
    line_height = 28
    total_h = (len(messages) - 1) * line_height
    y_start = HEIGHT // 2 - total_h // 2
    for i, msg in enumerate(messages):
        alpha = int(255 * (msg["timer"] / 3.0))
        color = (*msg.get("color", (255, 255, 255))[:3], alpha) if len(msg.get("color", (0, 0, 0))) > 3 else msg.get("color", (255, 255, 255))
        text_surf = font.render(f"PICKED UP: {msg.get('weapon_name', '')}", True, color[:3])
        text_rect = text_surf.get_rect(center=(WIDTH // 2, y_start + i * line_height))
        screen.blit(text_surf, text_rect)


def _draw_wave_reset_debug(screen: pygame.Surface, state, font, WIDTH: int, HEIGHT: int) -> None:
    """Show last wave-reset events (trigger, wave_num, enemies_before) to debug spurious resets."""
    log = getattr(state, "wave_reset_log", None)
    if not log:
        return
    x = WIDTH - 420
    y = 10
    title = font.render("Wave resets (trigger | wave | enemies_before):", True, (255, 200, 100))
    screen.blit(title, (x, y))
    y += 18
    for entry in log[-5:]:  # last 5
        t = entry.get("trigger", "?")
        w = entry.get("wave_num", "?")
        e = entry.get("enemies_before", "?")
        rt = entry.get("run_time", 0)
        color = (255, 100, 100) if e and e > 0 else (150, 255, 150)
        line = font.render(f"  t={rt:.1f}s {t!r} wave={w} enemies_before={e}", True, color)
        screen.blit(line, (x, y))
        y += 16


def _draw_wave_countdown(screen: pygame.Surface, state, font, big_font, WIDTH: int, HEIGHT: int) -> None:
    if not (getattr(state, "wave_active", False) and len(getattr(state, "enemies", [])) == 0):
        return
    time_to_next = getattr(state, "time_to_next_wave", 0)
    if time_to_next >= 3.0:
        return
    countdown_number = max(1, min(3, 3 - int(time_to_next)))
    next_wave_num = state.wave_number + 1
    countdown_text = f"WAVE {next_wave_num} STARTING IN {countdown_number}"
    draw_centered_text(screen, font, big_font, WIDTH, countdown_text, HEIGHT // 2, (255, 255, 0), use_big=True)
