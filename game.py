# game.py
#pygame library
import pygame
#track events using datetime
from datetime import datetime

#reference telemetry.py for the following classes (you can tell by checking telemetry.py)
from telemetry import Telemetry, EnemySpawnEvent, PlayerPosEvent, ShotEvent

#start pygame
pygame.init()

# ----------------------------
# Window / timing
# ----------------------------
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mouse Aim Shooter + Telemetry (SQLite)")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# ----------------------------
# Telemetry
# ----------------------------
telemetry = Telemetry(db_path="game_telemetry.db", flush_interval_s=0.5, max_buffer=700)
run_started_at = datetime.utcnow().isoformat(timespec="seconds")

# ----------------------------
# Player
# ----------------------------
player = pygame.Rect((WIDTH - 25) // 2, (HEIGHT - 25) // 2, 25, 25)
player_speed = 300  # px/s
player_max_hp = 100
player_hp = player_max_hp
pygame.mouse.set_visible(True)

# ----------------------------
# World blocks (solid + pushable)
# ----------------------------
blocks = [
    {"rect": pygame.Rect(100, 100, 40, 40), "color": (80, 140, 220)},
    {"rect": pygame.Rect(180, 180, 60, 30), "color": (30, 30, 30)},
    {"rect": pygame.Rect(550, 420, 70, 70), "color": (200, 200, 200)},
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

# ----------------------------
# Enemies (rectangles with health)
# ----------------------------
enemies: list[dict] = [
    {
        "type": "grunt",
        "rect": pygame.Rect(120, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "time_since_shot": 999.0,
        "projectile_speed": 320,
    },
    {
        "type": "heavy",
        "rect": pygame.Rect(650, 120, 32, 32),
        "color": (220, 120, 80),
        "hp": 80,
        "max_hp": 80,
        "shoot_cooldown": 1.2,
        "time_since_shot": 999.0,
        "projectile_speed": 280,
    },
    {
        "type": "stinky",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "time_since_shot": 999.0,
        "projectile_speed": 320,
    },
]

# ----------------------------
# Enemy projectiles
# ----------------------------
enemy_projectiles: list[dict] = []
enemy_projectile_size = (10, 10)
enemy_projectile_damage = 10

# ----------------------------
# Counters (for runs table)
# ----------------------------
running = True
run_time = 0.0
shots_fired = 0
hits = 0
damage_taken = 0
enemies_spawned = 0
enemies_killed = 0

# sample player position every N seconds
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

    telemetry.log_shot(ShotEvent(
        t=run_time,
        origin_x=player.centerx,
        origin_y=player.centery,
        target_x=mx,
        target_y=my,
        dir_x=float(d.x),
        dir_y=float(d.y),
    ))


def spawn_enemy_projectile(enemy: dict):
    d = vec_toward(enemy["rect"].centerx, enemy["rect"].centery, player.centerx, player.centery)
    r = pygame.Rect(
        enemy["rect"].centerx - enemy_projectile_size[0] // 2,
        enemy["rect"].centery - enemy_projectile_size[1] // 2,
        enemy_projectile_size[0],
        enemy_projectile_size[1],
    )
    enemy_projectiles.append({"rect": r, "vel": d * enemy["projectile_speed"]})


# ----------------------------
# Start run + log initial enemy spawns
# ----------------------------
run_id = telemetry.start_run(run_started_at, player_max_hp)

for e in enemies:
    enemies_spawned += 1
    telemetry.log_enemy_spawn(EnemySpawnEvent(
        t=0.0,
        enemy_type=e["type"],
        x=e["rect"].x,
        y=e["rect"].y,
        w=e["rect"].w,
        h=e["rect"].h,
        hp=e["hp"],
    ))
telemetry.flush(force=True)


# ----------------------------
# Main loop with safe shutdown
# ----------------------------
try:
    while running:
        dt = clock.tick(60) / 1000.0
        run_time += dt
        player_time_since_shot += dt

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- Input (WASD movement) ---
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

        # --- Shooting: left mouse button ---
        if pygame.mouse.get_pressed(3)[0] and player_time_since_shot >= player_shoot_cooldown:
            spawn_player_bullet_and_log()
            player_time_since_shot = 0.0

        # --- Update: player movement + pushing ---
        move_player_with_push(player, move_x, move_y, blocks)

        # --- Telemetry: sample player position periodically ---
        pos_timer += dt
        if pos_timer >= POS_SAMPLE_INTERVAL:
            pos_timer -= POS_SAMPLE_INTERVAL
            telemetry.log_player_position(PlayerPosEvent(t=run_time, x=player.x, y=player.y))

        # --- Update: enemies shoot projectiles at player ---
        for e in enemies:
            e["time_since_shot"] += dt
            if e["time_since_shot"] >= e["shoot_cooldown"]:
                spawn_enemy_projectile(e)
                e["time_since_shot"] = 0.0

        # --- Update: player bullets ---
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
                enemies[hit_enemy_index]["hp"] -= player_bullet_damage
                player_bullets.remove(b)

                if enemies[hit_enemy_index]["hp"] <= 0:
                    enemies.pop(hit_enemy_index)
                    enemies_killed += 1
                continue

            # bullets stop on blocks
            for blk in blocks:
                if r.colliderect(blk["rect"]):
                    player_bullets.remove(b)
                    break

        # --- Update: enemy projectiles ---
        for p in enemy_projectiles[:]:
            r = p["rect"]
            v = p["vel"]
            r.x += int(v.x * dt)
            r.y += int(v.y * dt)

            if rect_offscreen(r):
                enemy_projectiles.remove(p)
                continue

            if r.colliderect(player):
                player_hp -= enemy_projectile_damage
                damage_taken += enemy_projectile_damage
                enemy_projectiles.remove(p)
                if player_hp <= 0:
                    player_hp = 0
                    running = False
                continue

            # projectiles collide with blocks
            for blk in blocks:
                if r.colliderect(blk["rect"]):
                    enemy_projectiles.remove(p)
                    break

        # --- Telemetry batched flush tick ---
        telemetry.tick(dt)

        # --- Draw ---
        screen.fill((30, 30, 30))

        for blk in blocks:
            pygame.draw.rect(screen, blk["color"], blk["rect"])

        for e in enemies:
            pygame.draw.rect(screen, e["color"], e["rect"])
            draw_health_bar(
                e["rect"].x,
                e["rect"].y - 10,
                e["rect"].w,
                6,
                e["hp"],
                e["max_hp"]
            )

        pygame.draw.rect(screen, (200, 60, 60), player)

        for b in player_bullets:
            pygame.draw.rect(screen, (240, 240, 80), b["rect"])
        for p in enemy_projectiles:
            pygame.draw.rect(screen, (120, 220, 255), p["rect"])

        draw_health_bar(10, 10, 220, 18, player_hp, player_max_hp)
        screen.blit(font.render(f"HP: {player_hp}/{player_max_hp}", True, (230, 230, 230)), (12, 34))
        screen.blit(font.render(f"Enemies: {len(enemies)}", True, (230, 230, 230)), (10, 60))
        screen.blit(font.render(f"Run: {run_time:.1f}s  Shots: {shots_fired}  Hits: {hits}  Kills: {enemies_killed}", True, (230, 230, 230)), (10, 82))

        pygame.display.flip()

except KeyboardInterrupt:
    # If you run from terminal and hit Ctrl+C, we still want a clean save.
    print("Interrupted by user (Ctrl+C). Saving run...")

except Exception as e:
    # Any crash still saves a run record + flushed events
    print("Unhandled exception:", repr(e))
    raise

finally:
    # ----------------------------
    # SAFE SHUTDOWN (ALWAYS RUNS)
    # ----------------------------
    run_ended_at = datetime.utcnow().isoformat(timespec="seconds")
    telemetry.end_run(
        ended_at_iso=run_ended_at,
        seconds_survived=run_time,
        player_hp_end=player_hp,
        shots_fired=shots_fired,
        hits=hits,
        damage_taken=damage_taken,
        enemies_spawned=enemies_spawned,
        enemies_killed=enemies_killed,
    )
    telemetry.close()
    pygame.quit()

    print(f"Saved run_id={run_id} to game_telemetry.db")
