#FEATURES TO ADD
#--------
#change player bullet color
#change enemy bullet colors
#enemy movement
#enemy respawn timer
#survival timer, waves, multiple levels
#movement direction overwrites to most recent move direction
#player path prediction
#different shapes for shots (circle, squares, etc., like 2hu)

import pygame
from datetime import datetime, timezone

from telemetry import (
    Telemetry,
    EnemySpawnEvent,
    PlayerPosEvent,
    ShotEvent,
    EnemyHitEvent,
    PlayerDamageEvent,
    PlayerDeathEvent,
)

pygame.init()

# ----------------------------
# Window / timing
# ----------------------------
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Aim Shooter + Telemetry (SQLite)")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 56)

# ----------------------------
# Telemetry
# ----------------------------
telemetry = Telemetry(db_path="game_telemetry.db", flush_interval_s=0.5, max_buffer=700)
run_started_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

# ----------------------------
# Game state
# ----------------------------
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_CONTINUE = "CONTINUE"

state = STATE_PLAYING

pause_options = ["Continue", "Quit"]
pause_selected = 0
continue_blink_t = 0.0

# ----------------------------
# Player
# ----------------------------
player = pygame.Rect((WIDTH - 25) // 2, (HEIGHT - 25) // 2, 25, 25)
player_speed = 300  # px/s
player_max_hp = 100
player_hp = player_max_hp
pygame.mouse.set_visible(True)

LIVES_START = 1
lives = LIVES_START

# ----------------------------
# World blocks
# ----------------------------
blocks = [
    {"rect": pygame.Rect(100, 100, 100, 100), "color": (80, 140, 220)},
    {"rect": pygame.Rect(180, 180, 60, 30), "color": (30, 30, 30)},
    {"rect": pygame.Rect(550, 420, 70, 70), "color": (200, 200, 200)},
    {"rect": pygame.Rect(700, 420, 70, 70), "color": (220, 200, 10)},
]

# ----------------------------
# Player bullets
# ----------------------------
player_bullets: list[dict] = []
player_bullet_speed = 900
player_bullet_size = (8, 8)
player_bullet_damage = 20
player_shoot_cooldown = 0.12
player_time_since_shot = 999.0
player_bullets_color = (10, 200, 200)

# ----------------------------
# Enemy templates + cloning
# ----------------------------
enemy_templates: list[dict] = [
    {
        "type": "grunt",
        "rect": pygame.Rect(120, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "projectile_speed": 320,
    },
    {
        "type": "heavy",
        "rect": pygame.Rect(650, 120, 32, 32),
        "color": (220, 120, 80),
        "hp": 80,
        "max_hp": 80,
        "shoot_cooldown": 1.2,
        "projectile_speed": 280,
    },
    {
        "type": "stinky",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "projectile_speed": 320,
    },
    {
        "type": "baka",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (100, 80, 80),
        "hp": 400,
        "max_hp": 400,
        "shoot_cooldown": 0.1,
        "projectile_speed": 500,
    },
    {
        "type": "neko neko desu",
        "rect": pygame.Rect(100, 450, 28, 28),
        "color": (100, 80, 0),
        "hp": 20,
        "max_hp": 20,
        "shoot_cooldown": 0.01,
        "projectile_speed": 500,
    },
    {
        "type": "BIG NEKU",
        "rect": pygame.Rect(400, 450, 28, 28),
        "color": (100, 200, 0),
        "hp": 1000,
        "max_hp": 1000,
        "shoot_cooldown": 1,
        "projectile_speed": 700,
    },

]


def clone_enemies_from_templates() -> list[dict]:
    out: list[dict] = []
    for t in enemy_templates:
        out.append(
            {
                "type": t["type"],
                "rect": pygame.Rect(t["rect"].x, t["rect"].y, t["rect"].w, t["rect"].h),
                "color": t["color"],
                "hp": t["hp"],
                "max_hp": t["max_hp"],
                "shoot_cooldown": t["shoot_cooldown"],
                "time_since_shot": 999.0,
                "projectile_speed": t["projectile_speed"],
            }
        )
    return out


enemies: list[dict] = clone_enemies_from_templates()

# ----------------------------
# Enemy projectiles
# ----------------------------
enemy_projectiles: list[dict] = []
enemy_projectile_size = (10, 10)
enemy_projectile_damage = 10
enemy_projectiles_color = (200, 200, 200)

# ----------------------------
# Run counters (runs table)
# ----------------------------
running = True
run_time = 0.0

shots_fired = 0
hits = 0

damage_taken = 0
damage_dealt = 0

enemies_spawned = 0
enemies_killed = 0
deaths = 0

POS_SAMPLE_INTERVAL = 0.10
pos_timer = 0.0


# ----------------------------
# Helpers
# ----------------------------
def clamp_rect_to_screen(r: pygame.Rect):
    r.x = max(0, min(r.x, WIDTH - r.w))
    r.y = max(0, min(r.y, HEIGHT - r.h))


def vec_toward(ax, ay, bx, by) -> pygame.Vector2:
    v = pygame.Vector2(bx - ax, by - ay)
    if v.length_squared() == 0:
        return pygame.Vector2(1, 0)
    return v.normalize()


def can_move_rect(rect: pygame.Rect, dx: int, dy: int, other_rects: list[pygame.Rect]) -> bool:
    test = rect.move(dx, dy)
    if test.left < 0 or test.right > WIDTH or test.top < 0 or test.bottom > HEIGHT:
        return False
    for o in other_rects:
        if test.colliderect(o):
            return False
    return True


def move_player_with_push(player_rect: pygame.Rect, move_x: int, move_y: int, block_list: list[dict]):
    """Solid collision + pushing blocks (single block push; no chain pushing)."""
    block_rects = [b["rect"] for b in block_list]

    for axis_dx, axis_dy in [(move_x, 0), (0, move_y)]:
        if axis_dx == 0 and axis_dy == 0:
            continue

        player_rect.x += axis_dx
        player_rect.y += axis_dy

        hit_block = None
        for b in block_list:
            if player_rect.colliderect(b["rect"]):
                hit_block = b
                break

        if hit_block is None:
            continue

        hit_rect = hit_block["rect"]
        other_rects = [r for r in block_rects if r is not hit_rect]

        if can_move_rect(hit_rect, axis_dx, axis_dy, other_rects):
            hit_rect.x += axis_dx
            hit_rect.y += axis_dy
        else:
            player_rect.x -= axis_dx
            player_rect.y -= axis_dy

    clamp_rect_to_screen(player_rect)


def rect_offscreen(r: pygame.Rect) -> bool:
    return r.right < 0 or r.left > WIDTH or r.bottom < 0 or r.top > HEIGHT


def draw_health_bar(x, y, w, h, hp, max_hp):
    hp = max(0, min(hp, max_hp))
    pygame.draw.rect(screen, (60, 60, 60), (x, y, w, h))
    fill_w = int(w * (hp / max_hp)) if max_hp > 0 else 0
    pygame.draw.rect(screen, (60, 200, 60), (x, y, fill_w, h))
    pygame.draw.rect(screen, (20, 20, 20), (x, y, w, h), 2)


def draw_centered_text(text: str, y: int, color=(235, 235, 235), use_big=False):
    f = big_font if use_big else font
    surf = f.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH // 2, y))
    screen.blit(surf, rect)


def spawn_player_bullet_and_log():
    global shots_fired

    mx, my = pygame.mouse.get_pos()
    d = vec_toward(player.centerx, player.centery, mx, my)

    r = pygame.Rect(
        player.centerx - player_bullet_size[0] // 2,
        player.centery - player_bullet_size[1] // 2,
        player_bullet_size[0],
        player_bullet_size[1],
    )
    player_bullets.append({"rect": r, "vel": d * player_bullet_speed})
    shots_fired += 1

    telemetry.log_shot(
        ShotEvent(
            t=run_time,
            origin_x=player.centerx,
            origin_y=player.centery,
            target_x=mx,
            target_y=my,
            dir_x=float(d.x),
            dir_y=float(d.y),
        )
    )


def spawn_enemy_projectile(enemy: dict):
    d = vec_toward(enemy["rect"].centerx, enemy["rect"].centery, player.centerx, player.centery)
    r = pygame.Rect(
        enemy["rect"].centerx - enemy_projectile_size[0] // 2,
        enemy["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    enemy_projectiles.append(
        {
            "rect": r,
            "vel": d * enemy["projectile_speed"],
            "enemy_type": enemy["type"],  # attribute damage source
        }
    )


def log_enemy_spawns_for_current_wave():
    global enemies_spawned
    for e in enemies:
        enemies_spawned += 1
        telemetry.log_enemy_spawn(
            EnemySpawnEvent(
                t=run_time,
                enemy_type=e["type"],
                x=e["rect"].x,
                y=e["rect"].y,
                w=e["rect"].w,
                h=e["rect"].h,
                hp=e["hp"],
            )
        )
    telemetry.flush(force=True)


def reset_after_death():
    global player_hp, player_time_since_shot, pos_timer
    global enemies, player_bullets, enemy_projectiles

    player_hp = player_max_hp
    player_time_since_shot = 999.0
    pos_timer = 0.0

    player.x = (WIDTH - player.w) // 2
    player.y = (HEIGHT - player.h) // 2
    clamp_rect_to_screen(player)

    player_bullets.clear()
    enemy_projectiles.clear()

    enemies = clone_enemies_from_templates()
    log_enemy_spawns_for_current_wave()


# ----------------------------
# Start run + log initial spawns
# ----------------------------
run_id = telemetry.start_run(run_started_at, player_max_hp)
log_enemy_spawns_for_current_wave()


# ----------------------------
# Main loop with safe shutdown
# ----------------------------
try:
    while running:
        dt_real = clock.tick(60) / 1000.0
        dt = dt_real if state == STATE_PLAYING else 0.0

        if state == STATE_PLAYING:
            run_time += dt
            player_time_since_shot += dt

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_PLAYING:
                        state = STATE_PAUSED
                        pause_selected = 0
                    elif state == STATE_PAUSED:
                        state = STATE_PLAYING
                    elif state == STATE_CONTINUE:
                        running = False

                if event.key == pygame.K_p:
                    if state == STATE_PLAYING:
                        state = STATE_PAUSED
                        pause_selected = 0
                    elif state == STATE_PAUSED:
                        state = STATE_PLAYING

                # Pause menu
                if state == STATE_PAUSED:
                    if event.key == pygame.K_UP:
                        pause_selected = (pause_selected - 1) % len(pause_options)
                    elif event.key == pygame.K_DOWN:
                        pause_selected = (pause_selected + 1) % len(pause_options)
                    elif event.key == pygame.K_RETURN:
                        choice = pause_options[pause_selected]
                        if choice == "Continue":
                            state = STATE_PLAYING
                        elif choice == "Quit":
                            running = False

                # Continue screen
                if state == STATE_CONTINUE:
                    if event.key == pygame.K_RETURN:
                        reset_after_death()
                        state = STATE_PLAYING

        # --- Simulation ---
        if state == STATE_PLAYING:
            # Movement
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_a]:
                dx -= 1
            if keys[pygame.K_d]:
                dx += 1
            if keys[pygame.K_w]:
                dy -= 1
            if keys[pygame.K_s]:
                dy += 1

            move_x = int(dx * player_speed * dt)
            move_y = int(dy * player_speed * dt)

            # Shooting
            if pygame.mouse.get_pressed(3)[0] and player_time_since_shot >= player_shoot_cooldown:
                spawn_player_bullet_and_log()
                player_time_since_shot = 0.0

            move_player_with_push(player, move_x, move_y, blocks)

            # Position sampling
            pos_timer += dt
            if pos_timer >= POS_SAMPLE_INTERVAL:
                pos_timer -= POS_SAMPLE_INTERVAL
                telemetry.log_player_position(PlayerPosEvent(t=run_time, x=player.x, y=player.y))

            # Enemy shooting
            for e in enemies:
                e["time_since_shot"] += dt
                if e["time_since_shot"] >= e["shoot_cooldown"]:
                    spawn_enemy_projectile(e)
                    e["time_since_shot"] = 0.0

            # Player bullets update
            for b in player_bullets[:]:
                r = b["rect"]
                v = b["vel"]
                r.x += int(v.x * dt)
                r.y += int(v.y * dt)

                if rect_offscreen(r):
                    player_bullets.remove(b)
                    continue

                # bullet hits enemy
                hit_enemy_index = None
                for i, e in enumerate(enemies):
                    if r.colliderect(e["rect"]):
                        hit_enemy_index = i
                        break

                if hit_enemy_index is not None:
                    hits += 1
                    e = enemies[hit_enemy_index]

                    # apply damage
                    e["hp"] -= player_bullet_damage
                    damage_dealt += player_bullet_damage

                    killed = e["hp"] <= 0
                    hp_after = max(0, e["hp"])

                    telemetry.log_enemy_hit(
                        EnemyHitEvent(
                            t=run_time,
                            enemy_type=e["type"],
                            enemy_x=e["rect"].x,
                            enemy_y=e["rect"].y,
                            damage=player_bullet_damage,
                            enemy_hp_after=hp_after,
                            killed=killed,
                        )
                    )

                    player_bullets.remove(b)

                    if killed:
                        enemies.pop(hit_enemy_index)
                        enemies_killed += 1

                    continue

                # bullets stop on blocks
                for blk in blocks:
                    if r.colliderect(blk["rect"]):
                        player_bullets.remove(b)
                        break

            # Enemy projectiles update
            for p in enemy_projectiles[:]:
                r = p["rect"]
                v = p["vel"]
                r.x += int(v.x * dt)
                r.y += int(v.y * dt)

                if rect_offscreen(r):
                    enemy_projectiles.remove(p)
                    continue

                if r.colliderect(player):
                    # apply damage
                    player_hp -= enemy_projectile_damage
                    damage_taken += enemy_projectile_damage

                    if player_hp < 0:
                        player_hp = 0

                    telemetry.log_player_damage(
                        PlayerDamageEvent(
                            t=run_time,
                            amount=enemy_projectile_damage,
                            source_type="enemy_projectile",
                            source_enemy_type=p.get("enemy_type"),
                            player_x=player.x,
                            player_y=player.y,
                            player_hp_after=player_hp,
                        )
                    )

                    enemy_projectiles.remove(p)

                    # death handling
                    if player_hp <= 0:
                        deaths += 1
                        lives -= 1

                        telemetry.log_player_death(
                            PlayerDeathEvent(
                                t=run_time,
                                player_x=player.x,
                                player_y=player.y,
                                lives_left=lives,
                            )
                        )

                        if lives > 0:
                            state = STATE_CONTINUE
                            continue_blink_t = 0.0
                            continue
                        else:
                            running = False

                    continue

                # projectiles collide with blocks
                for blk in blocks:
                    if r.colliderect(blk["rect"]):
                        enemy_projectiles.remove(p)
                        break

            telemetry.tick(dt)

        else:
            # allow background flush timing while paused/continue screen
            telemetry.tick(dt_real)

        # --- Draw ---
        screen.fill((30, 30, 30))

        for blk in blocks:
            pygame.draw.rect(screen, blk["color"], blk["rect"])

        for e in enemies:
            pygame.draw.rect(screen, e["color"], e["rect"])
            draw_health_bar(e["rect"].x, e["rect"].y - 10, e["rect"].w, 6, e["hp"], e["max_hp"])

        pygame.draw.rect(screen, (200, 60, 60), player)

        for b in player_bullets:
            pygame.draw.rect(screen, (240, 240, 80), b["rect"])
        for p in enemy_projectiles:
            pygame.draw.rect(screen, (120, 220, 255), p["rect"])

        # HUD
        draw_health_bar(10, 10, 220, 18, player_hp, player_max_hp)
        screen.blit(font.render(f"HP: {player_hp}/{player_max_hp}", True, (230, 230, 230)), (12, 34))
        screen.blit(font.render(f"Lives: {lives}", True, (230, 230, 230)), (10, 58))
        screen.blit(font.render(f"Enemies: {len(enemies)}", True, (230, 230, 230)), (10, 80))
        screen.blit(font.render(f"Damage dealt: {damage_dealt}", True, (230, 230, 230)), (10, 102))
        screen.blit(font.render(f"Damage taken: {damage_taken}", True, (230, 230, 230)), (10, 124))
        screen.blit(
            font.render(
                f"Run: {run_time:.1f}s  Shots: {shots_fired}  Hits: {hits}  Kills: {enemies_killed}  Deaths: {deaths}",
                True,
                (230, 230, 230),
            ),
            (10, 146),
        )

        # Pause overlay
        if state == STATE_PAUSED:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            draw_centered_text("Paused", HEIGHT // 2 - 140, use_big=True)

            for i, opt in enumerate(pause_options):
                prefix = "> " if i == pause_selected else "  "
                draw_centered_text(prefix + opt, HEIGHT // 2 - 40 + i * 40)

            draw_centered_text("Up/Down + Enter.  P or Esc to resume.", HEIGHT // 2 + 120, color=(190, 190, 190))

        # Continue overlay
        elif state == STATE_CONTINUE:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            draw_centered_text("You Died", HEIGHT // 2 - 150, use_big=True)
            draw_centered_text(f"Lives left: {lives}", HEIGHT // 2 - 90)

            continue_blink_t += dt_real
            show = (int(continue_blink_t * 2) % 2) == 0
            if show:
                draw_centered_text("Press Enter to continue", HEIGHT // 2 + 10)
            draw_centered_text("Press Esc to quit", HEIGHT // 2 + 60, color=(190, 190, 190))

        pygame.display.flip()

except KeyboardInterrupt:
    print("Interrupted by user (Ctrl+C). Saving run...")

except Exception as e:
    print("Unhandled exception:", repr(e))
    raise

finally:
    run_ended_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    telemetry.end_run(
        ended_at_iso=run_ended_at,
        seconds_survived=run_time,
        player_hp_end=player_hp,
        shots_fired=shots_fired,
        hits=hits,
        damage_taken=damage_taken,
        damage_dealt=damage_dealt,
        enemies_spawned=enemies_spawned,
        enemies_killed=enemies_killed,
        deaths=deaths,
    )
    telemetry.close()
    pygame.quit()

    print(f"Saved run_id={run_id} to game_telemetry.db")
