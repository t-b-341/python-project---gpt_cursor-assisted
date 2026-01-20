#FEATURES TO ADD
#--------------------------------------------------------
#change player bullet color
#change enemy bullet colors
#enemy movement
#enemy respawn timer
#survival timer, waves, multiple levels
#movement direction overwrites to most recent move direction
#player path prediction
#different shapes for shots (circle, squares, etc., like 2hu)
#--------------------------------------------------------
#add boost mechanic using shift, and slow down mechanic using ctrl
#add a control mapping system, so the player can map the keys to the actions
#add a pickup for boost
#add a pickup for more firing speed
#add a pickup for enemies spawn more often, that enemies can pick up, and that you have to shoot to destroy the pickup
#--------------------------------------------------------
#make pickups bigger, add in another pickup that increases the player's max health 
#add a pickup that increases the player's speed
#add a pickup that increases the player's firing rate
#add a pickup that increases the player's bullet size
#add a pickup that increases the player's bullet speed
#add a pickup that increases the player's bullet damage
#add a pickup that increases the player's bullet knockback
#add a pickup that increases the player's bullet penetration
#add a pickup that increases the player's bullet explosion radius
#randomize the pickups, so that the player never knows what they will get
#--------------------------------------------------------
#make pickup that increases the shot size to 10x regular size, and another pickup that increase the shot beams to 3 beams
#--------------------------------------------------------
#add a pickup that bounces shots around on the walls
#add an enemy that shoots shots that bounce around on the walls
#stack pickups so that the player can get a combo of pickups
#add in more squares and rectangles that can be moved around, but have health bars that enemies can shoot at to destroy them


import math
import random
import json
import os

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
    WaveEvent,
    EnemyPositionEvent,
    PlayerVelocityEvent,
    BulletMetadataEvent,
)

pygame.init()

# ----------------------------
# Controls (remappable)
# ----------------------------
CONTROLS_PATH = "controls.json"
DEFAULT_CONTROLS = {
    "move_left": "a",
    "move_right": "d",
    "move_up": "w",
    "move_down": "s",
    "boost": "left shift",
    "slow": "left ctrl",
}


def _key_name_to_code(name: str) -> int:
    name = (name or "").lower().strip()
    try:
        return pygame.key.key_code(name)
    except Exception:
        return pygame.K_UNKNOWN


def load_controls() -> dict[str, int]:
    data = {}
    if os.path.exists(CONTROLS_PATH):
        try:
            with open(CONTROLS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f) or {}
        except Exception:
            data = {}

    merged = {**DEFAULT_CONTROLS, **{k: v for k, v in data.items() if isinstance(v, str)}}
    return {action: _key_name_to_code(key_name) for action, key_name in merged.items()}


def save_controls(controls: dict[str, int]) -> None:
    # Persist as human-readable key names so players can edit the file too
    out: dict[str, str] = {}
    for action, key_code in controls.items():
        try:
            out[action] = pygame.key.name(key_code)
        except Exception:
            out[action] = "unknown"
    with open(CONTROLS_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)


controls = load_controls()

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

# Controls menu state
STATE_CONTROLS = "CONTROLS"
controls_actions = ["move_left", "move_right", "move_up", "move_down", "boost", "slow"]
controls_selected = 0
controls_rebinding = False

# ----------------------------
# Player
# ----------------------------
player = pygame.Rect((WIDTH - 25) // 2, (HEIGHT - 25) // 2, 25, 25)
player_speed = 300  # px/s
player_max_hp = 100
player_hp = player_max_hp
pygame.mouse.set_visible(True)

LIVES_START = 10
lives = LIVES_START

# Track most recent movement keys so latest press wins on conflicts
last_horizontal_key = None  # keycode of current "latest" horizontal key
last_vertical_key = None  # keycode of current "latest" vertical key
last_move_velocity = pygame.Vector2(0, 0)

# Boost / slow
boost_meter_max = 100.0
boost_meter = boost_meter_max
boost_drain_per_s = 45.0
boost_regen_per_s = 25.0
boost_speed_mult = 1.7
slow_speed_mult = 0.45

# Fire-rate pickup buff
fire_rate_buff_t = 0.0
fire_rate_buff_duration = 10.0
fire_rate_mult = 0.55  # reduces cooldown while active

# Permanent player stat multipliers (from pickups)
player_stat_multipliers = {
    "speed": 1.0,
    "firerate": 1.0,  # permanent firerate boost (stacks with temporary buff)
    "bullet_size": 1.0,
    "bullet_speed": 1.0,
    "bullet_damage": 1.0,
    "bullet_knockback": 1.0,
    "bullet_penetration": 0,  # number of enemies bullet can pierce through
    "bullet_explosion_radius": 0.0,  # explosion radius in pixels (0 = no explosion)
}

# Special bullet modifiers
giant_bullets_active = False  # 10x bullet size
triple_shot_active = False  # shoot 3 beams instead of 1
bouncing_bullets_active = False  # bullets bounce off walls

# ----------------------------
# World blocks
# ----------------------------
blocks = [
    {"rect": pygame.Rect(100, 100, 100, 100), "color": (80, 140, 220), "hp": None, "max_hp": None},  # indestructible
    {"rect": pygame.Rect(180, 180, 60, 30), "color": (30, 30, 30), "hp": None, "max_hp": None},  # indestructible
    {"rect": pygame.Rect(550, 420, 70, 70), "color": (200, 200, 200), "hp": None, "max_hp": None},  # indestructible
    {"rect": pygame.Rect(700, 420, 70, 70), "color": (220, 200, 10), "hp": None, "max_hp": None},  # indestructible
]

# Add more destructible blocks
destructible_blocks = [
    {"rect": pygame.Rect(300, 200, 80, 80), "color": (150, 100, 200), "hp": 50, "max_hp": 50},
    {"rect": pygame.Rect(450, 300, 60, 60), "color": (100, 200, 150), "hp": 40, "max_hp": 40},
    {"rect": pygame.Rect(200, 500, 90, 50), "color": (200, 150, 100), "hp": 60, "max_hp": 60},
    {"rect": pygame.Rect(750, 600, 70, 70), "color": (150, 150, 200), "hp": 45, "max_hp": 45},
    {"rect": pygame.Rect(150, 700, 100, 40), "color": (200, 200, 100), "hp": 55, "max_hp": 55},
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
player_bullet_shapes = ["circle", "square", "diamond"]
player_bullet_shape_index = 0

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
        "projectile_color": (180, 220, 255),
        "projectile_shape": "square",
        "speed": 90,
    },
    {
        "type": "heavy",
        "rect": pygame.Rect(650, 120, 32, 32),
        "color": (220, 120, 80),
        "hp": 80,
        "max_hp": 80,
        "shoot_cooldown": 1.2,
        "projectile_speed": 280,
        "projectile_color": (255, 190, 120),
        "projectile_shape": "circle",
        "speed": 70,
    },
    {
        "type": "stinky",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (220, 80, 80),
        "hp": 60,
        "max_hp": 60,
        "shoot_cooldown": 0.9,
        "projectile_speed": 320,
        "projectile_color": (180, 220, 255),
        "projectile_shape": "diamond",
        "speed": 110,
    },
    {
        "type": "baka",
        "rect": pygame.Rect(90, 450, 28, 28),
        "color": (100, 80, 80),
        "hp": 400,
        "max_hp": 400,
        "shoot_cooldown": 0.1,
        "projectile_speed": 500,
        "projectile_color": (255, 120, 180),
        "projectile_shape": "square",
        "speed": 150,
    },
    {
        "type": "neko neko desu",
        "rect": pygame.Rect(100, 450, 28, 28),
        "color": (100, 80, 0),
        "hp": 20,
        "max_hp": 20,
        "shoot_cooldown": 0.01,
        "projectile_speed": 500,
        "projectile_color": (200, 255, 140),
        "projectile_shape": "circle",
        "speed": 160,
    },
    {
        "type": "BIG NEKU",
        "rect": pygame.Rect(400, 450, 28, 28),
        "color": (100, 200, 0),
        "hp": 1000,
        "max_hp": 1000,
        "shoot_cooldown": 1,
        "projectile_speed": 700,
        "projectile_color": (160, 200, 255),
        "projectile_shape": "diamond",
        "speed": 60,
    },
    {
        "type": "bouncer",
        "rect": pygame.Rect(500, 500, 30, 30),
        "color": (255, 100, 100),
        "hp": 70,
        "max_hp": 70,
        "shoot_cooldown": 1.5,
        "projectile_speed": 350,
        "projectile_color": (255, 150, 150),
        "projectile_shape": "square",
        "speed": 85,
        "bouncing_projectiles": True,  # shoots bouncing projectiles
    },

]


def clone_enemies_from_templates() -> list[dict]:
    # Kept for compatibility but waves use start_wave() instead.
    return [make_enemy_from_template(t, 1.0, 1.0) for t in enemy_templates]


enemies: list[dict] = []

# ----------------------------
# Enemy projectiles
# ----------------------------
enemy_projectiles: list[dict] = []
enemy_projectile_size = (10, 10)
enemy_projectile_damage = 10
enemy_projectiles_color = (200, 200, 200)
enemy_projectile_shapes = ["circle", "square", "diamond"]

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

# Waves / progression
wave_number = 1
wave_respawn_delay = 2.5  # seconds between waves
time_to_next_wave = 0.0
wave_active = True
base_enemies_per_wave = 4
max_enemies_per_wave = 24

# Pickups
pickups: list[dict] = []
pickup_spawn_timer = 0.0
PICKUP_SPAWN_INTERVAL = 7.5
enemy_spawn_boost_level = 0  # enemies can increase this by collecting "spawn_boost" pickups


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


def random_spawn_position(size: tuple[int, int], max_attempts: int = 25) -> pygame.Rect:
    """Find a spawn position not overlapping player or blocks."""
    w, h = size
    for _ in range(max_attempts):
        x = random.randint(0, WIDTH - w)
        y = random.randint(0, HEIGHT - h)
        candidate = pygame.Rect(x, y, w, h)
        if candidate.colliderect(player):
            continue
        if any(candidate.colliderect(b["rect"]) for b in blocks):
            continue
        if any(candidate.colliderect(p["rect"]) for p in pickups):
            continue
        return candidate
    # fallback: top-left corner inside bounds
    return pygame.Rect(max(0, WIDTH // 2 - w), max(0, HEIGHT // 2 - h), w, h)


def make_enemy_from_template(t: dict, hp_scale: float, speed_scale: float) -> dict:
    hp = int(t["hp"] * hp_scale)
    return {
        "type": t["type"],
        "rect": pygame.Rect(t["rect"].x, t["rect"].y, t["rect"].w, t["rect"].h),
        "color": t["color"],
        "hp": hp,
        "max_hp": hp,
        "shoot_cooldown": t["shoot_cooldown"],
        "time_since_shot": random.uniform(0.0, t["shoot_cooldown"]),
        "projectile_speed": t["projectile_speed"],
        "projectile_color": t.get("projectile_color", enemy_projectiles_color),
        "projectile_shape": t.get("projectile_shape", "circle"),
        "speed": t.get("speed", 80) * speed_scale,
    }


def log_enemy_spawns(new_enemies: list[dict]):
    global enemies_spawned
    for e in new_enemies:
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


def start_wave(wave_num: int):
    """Spawn a new wave with scaling."""
    global enemies, wave_active
    enemies = []
    hp_scale = 1.0 + 0.15 * (wave_num - 1)
    speed_scale = 1.0 + 0.05 * (wave_num - 1)
    count = min(base_enemies_per_wave + enemy_spawn_boost_level + 2 * (wave_num - 1), max_enemies_per_wave)

    spawned: list[dict] = []
    for _ in range(count):
        tmpl = random.choice(enemy_templates)
        enemy = make_enemy_from_template(tmpl, hp_scale, speed_scale)
        enemy["rect"] = random_spawn_position((enemy["rect"].w, enemy["rect"].h))
        spawned.append(enemy)

    enemies.extend(spawned)
    log_enemy_spawns(spawned)
    wave_active = True
    
    # Log wave start event
    telemetry.log_wave(
        WaveEvent(
            t=run_time,
            wave_number=wave_num,
            event_type="start",
            enemies_spawned=count,
            hp_scale=hp_scale,
            speed_scale=speed_scale,
        )
    )


def spawn_pickup(pickup_type: str):
    # Make pickups bigger
    size = (32, 32)
    r = random_spawn_position(size)
    # All pickups look the same (mystery) - randomized color so player doesn't know what they're getting
    mystery_colors = [
        (180, 100, 255),  # purple
        (100, 255, 180),  # green
        (255, 180, 100),  # orange
        (180, 255, 255),  # cyan
        (255, 100, 180),  # pink
        (255, 255, 100),  # yellow
    ]
    color = random.choice(mystery_colors)
    pickups.append({"type": pickup_type, "rect": r, "color": color})


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


def draw_projectile(rect: pygame.Rect, color: tuple[int, int, int], shape: str):
    if shape == "circle":
        pygame.draw.circle(screen, color, rect.center, rect.w // 2)
    elif shape == "diamond":
        cx, cy = rect.center
        hw, hh = rect.w // 2, rect.h // 2
        points = [(cx, cy - hh), (cx + hw, cy), (cx, cy + hh), (cx - hw, cy)]
        pygame.draw.polygon(screen, color, points)
    else:
        pygame.draw.rect(screen, color, rect)


def spawn_player_bullet_and_log():
    global shots_fired, player_bullet_shape_index

    mx, my = pygame.mouse.get_pos()
    base_dir = vec_toward(player.centerx, player.centery, mx, my)

    shape = player_bullet_shapes[player_bullet_shape_index % len(player_bullet_shapes)]
    player_bullet_shape_index = (player_bullet_shape_index + 1) % len(player_bullet_shapes)

    # Determine shot pattern (single or triple)
    if triple_shot_active:
        # Triple shot: center + left + right spread
        spread_angle_deg = 8.6  # degrees
        directions = [
            base_dir,  # center
            base_dir.rotate(-spread_angle_deg),  # left
            base_dir.rotate(spread_angle_deg),  # right
        ]
    else:
        directions = [base_dir]

    # Spawn bullets for each direction
    for d in directions:
        # Apply stat multipliers
        size_mult = player_stat_multipliers["bullet_size"]
        if giant_bullets_active:
            size_mult *= 10.0  # 10x size multiplier
        
        effective_size = (
            int(player_bullet_size[0] * size_mult),
            int(player_bullet_size[1] * size_mult),
        )
        effective_speed = player_bullet_speed * player_stat_multipliers["bullet_speed"]
        effective_damage = int(player_bullet_damage * player_stat_multipliers["bullet_damage"])

        r = pygame.Rect(
            player.centerx - effective_size[0] // 2,
            player.centery - effective_size[1] // 2,
            effective_size[0],
            effective_size[1],
        )
        player_bullets.append({
            "rect": r,
            "vel": d * effective_speed,
            "shape": shape,
            "color": player_bullets_color,
            "damage": effective_damage,
            "penetration": int(player_stat_multipliers["bullet_penetration"]),
            "explosion_radius": player_stat_multipliers["bullet_explosion_radius"],
            "knockback": player_stat_multipliers["bullet_knockback"],
            "bounces": 10 if bouncing_bullets_active else 0,  # max bounces
        })
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
    
    # Log bullet metadata
    telemetry.log_bullet_metadata(
        BulletMetadataEvent(
            t=run_time,
            bullet_type="player",
            shape=shape,
            color_r=player_bullets_color[0],
            color_g=player_bullets_color[1],
            color_b=player_bullets_color[2],
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
    proj_color = enemy.get("projectile_color", enemy_projectiles_color)
    proj_shape = enemy.get("projectile_shape", "circle")
    bounces = enemy.get("bouncing_projectiles", False)
    enemy_projectiles.append(
        {
            "rect": r,
            "vel": d * enemy["projectile_speed"],
            "enemy_type": enemy["type"],  # attribute damage source
            "color": proj_color,
            "shape": proj_shape,
            "bounces": 10 if bounces else 0,  # max bounces for bouncing enemy type
        }
    )
    
    # Log enemy projectile metadata
    telemetry.log_bullet_metadata(
        BulletMetadataEvent(
            t=run_time,
            bullet_type="enemy",
            shape=proj_shape,
            color_r=proj_color[0],
            color_g=proj_color[1],
            color_b=proj_color[2],
            source_enemy_type=enemy["type"],
        )
    )


def log_enemy_spawns_for_current_wave():
    log_enemy_spawns(enemies)


def reset_after_death():
    global player_hp, player_time_since_shot, pos_timer
    global enemies, player_bullets, enemy_projectiles, wave_number, time_to_next_wave, wave_active

    player_hp = player_max_hp
    player_time_since_shot = 999.0
    pos_timer = 0.0

    player.x = (WIDTH - player.w) // 2
    player.y = (HEIGHT - player.h) // 2
    clamp_rect_to_screen(player)

    player_bullets.clear()
    enemy_projectiles.clear()

    wave_number = 1
    time_to_next_wave = 0.0
    start_wave(wave_number)


# ----------------------------
# Start run + log initial spawns
# ----------------------------
run_id = telemetry.start_run(run_started_at, player_max_hp)
start_wave(wave_number)


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
                # Controls rebinding mode
                if state == STATE_CONTROLS and controls_rebinding:
                    action = controls_actions[controls_selected]
                    controls[action] = event.key
                    save_controls(controls)
                    controls_rebinding = False
                    continue

                # Update last-pressed direction for conflict resolution
                if event.key in (controls["move_left"], controls["move_right"]):
                    last_horizontal_key = event.key
                if event.key in (controls["move_up"], controls["move_down"]):
                    last_vertical_key = event.key

                if event.key == pygame.K_ESCAPE:
                    if state == STATE_PLAYING:
                        state = STATE_PAUSED
                        pause_selected = 0
                    elif state == STATE_PAUSED:
                        state = STATE_PLAYING
                    elif state == STATE_CONTINUE:
                        running = False
                    elif state == STATE_CONTROLS:
                        state = STATE_PAUSED

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
                    elif event.key == pygame.K_c:
                        state = STATE_CONTROLS
                        controls_selected = 0
                        controls_rebinding = False

                # Controls menu
                if state == STATE_CONTROLS and not controls_rebinding:
                    if event.key == pygame.K_UP:
                        controls_selected = (controls_selected - 1) % len(controls_actions)
                    elif event.key == pygame.K_DOWN:
                        controls_selected = (controls_selected + 1) % len(controls_actions)
                    elif event.key == pygame.K_RETURN:
                        controls_rebinding = True

                # Continue screen
                if state == STATE_CONTINUE:
                    if event.key == pygame.K_RETURN:
                        reset_after_death()
                        state = STATE_PLAYING

            if event.type == pygame.KEYUP:
                keys_now = pygame.key.get_pressed()
                if event.key in (controls["move_left"], controls["move_right"]):
                    if last_horizontal_key == event.key:
                        left_k = controls["move_left"]
                        right_k = controls["move_right"]
                        if keys_now[left_k] and not keys_now[right_k]:
                            last_horizontal_key = left_k
                        elif keys_now[right_k] and not keys_now[left_k]:
                            last_horizontal_key = right_k
                        else:
                            last_horizontal_key = None
                if event.key in (controls["move_up"], controls["move_down"]):
                    if last_vertical_key == event.key:
                        up_k = controls["move_up"]
                        down_k = controls["move_down"]
                        if keys_now[up_k] and not keys_now[down_k]:
                            last_vertical_key = up_k
                        elif keys_now[down_k] and not keys_now[up_k]:
                            last_vertical_key = down_k
                        else:
                            last_vertical_key = None

        # --- Simulation ---
        if state == STATE_PLAYING:
            # Movement
            if not enemies and wave_active:
                wave_active = False
                time_to_next_wave = max(0.5, wave_respawn_delay - 0.25 * enemy_spawn_boost_level)
                # Log wave end event
                telemetry.log_wave(
                    WaveEvent(
                        t=run_time,
                        wave_number=wave_number,
                        event_type="end",
                        enemies_spawned=0,
                        hp_scale=1.0 + 0.15 * (wave_number - 1),
                        speed_scale=1.0 + 0.05 * (wave_number - 1),
                    )
                )

            if not wave_active:
                time_to_next_wave = max(0.0, time_to_next_wave - dt)
                if time_to_next_wave <= 0.0:
                    wave_number += 1
                    start_wave(wave_number)

            keys = pygame.key.get_pressed()
            dx = dy = 0
            left_k = controls["move_left"]
            right_k = controls["move_right"]
            up_k = controls["move_up"]
            down_k = controls["move_down"]
            boost_k = controls["boost"]
            slow_k = controls["slow"]

            left = keys[left_k]
            right = keys[right_k]
            up = keys[up_k]
            down = keys[down_k]
            wants_boost = keys[boost_k]
            wants_slow = keys[slow_k]

            if left and right:
                dx = -1 if last_horizontal_key == left_k else 1
            elif left:
                dx = -1
            elif right:
                dx = 1

            if up and down:
                dy = -1 if last_vertical_key == up_k else 1
            elif up:
                dy = -1
            elif down:
                dy = 1

            move_dir = pygame.Vector2(dx, dy)
            speed_mult = player_stat_multipliers["speed"]  # Apply permanent speed multiplier
            if wants_slow:
                speed_mult *= slow_speed_mult
            boosting = wants_boost and boost_meter > 0.0 and not wants_slow
            if boosting:
                speed_mult *= boost_speed_mult
                boost_meter = max(0.0, boost_meter - boost_drain_per_s * dt)
            else:
                boost_meter = min(boost_meter_max, boost_meter + boost_regen_per_s * dt)

            if move_dir.length_squared() > 0:
                move_dir = move_dir.normalize()
                last_move_velocity = move_dir * player_speed * speed_mult
            else:
                last_move_velocity = pygame.Vector2(0, 0)

            move_x = int(last_move_velocity.x * dt)
            move_y = int(last_move_velocity.y * dt)

            # Shooting
            # Apply both temporary and permanent fire rate multipliers
            temp_mult = fire_rate_mult if fire_rate_buff_t > 0 else 1.0
            perm_mult = 1.0 / player_stat_multipliers["firerate"] if player_stat_multipliers["firerate"] > 1.0 else 1.0
            effective_cooldown = player_shoot_cooldown * temp_mult * perm_mult
            if pygame.mouse.get_pressed(3)[0] and player_time_since_shot >= effective_cooldown:
                spawn_player_bullet_and_log()
                player_time_since_shot = 0.0

            move_player_with_push(player, move_x, move_y, blocks)

            # Update timed buffs
            if fire_rate_buff_t > 0:
                fire_rate_buff_t = max(0.0, fire_rate_buff_t - dt)

            block_rects = [b["rect"] for b in blocks]
            for e in enemies:
                dir_vec = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                move_vec = dir_vec * e["speed"] * dt
                dx_e = int(move_vec.x)
                dy_e = int(move_vec.y)
                if dx_e or dy_e:
                    moved = False
                    if can_move_rect(e["rect"], dx_e, dy_e, block_rects):
                        e["rect"].x += dx_e
                        e["rect"].y += dy_e
                        moved = True
                    else:
                        if dx_e and can_move_rect(e["rect"], dx_e, 0, block_rects):
                            e["rect"].x += dx_e
                            moved = True
                        if dy_e and can_move_rect(e["rect"], 0, dy_e, block_rects):
                            e["rect"].y += dy_e
                            moved = True
                    if moved:
                        clamp_rect_to_screen(e["rect"])

            # Position sampling
            pos_timer += dt
            if pos_timer >= POS_SAMPLE_INTERVAL:
                pos_timer -= POS_SAMPLE_INTERVAL
                telemetry.log_player_position(PlayerPosEvent(t=run_time, x=player.x, y=player.y))
                
                # Log player velocity
                telemetry.log_player_velocity(
                    PlayerVelocityEvent(
                        t=run_time,
                        x=player.x,
                        y=player.y,
                        vel_x=float(last_move_velocity.x),
                        vel_y=float(last_move_velocity.y),
                        speed=float(last_move_velocity.length()),
                    )
                )
                
                # Log enemy positions
                for e in enemies:
                    dir_vec = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                    vel_vec = dir_vec * e["speed"]
                    telemetry.log_enemy_position(
                        EnemyPositionEvent(
                            t=run_time,
                            enemy_type=e["type"],
                            x=e["rect"].x,
                            y=e["rect"].y,
                            speed=float(e["speed"]),
                            vel_x=float(vel_vec.x),
                            vel_y=float(vel_vec.y),
                        )
                    )

            # Enemy shooting
            for e in enemies:
                e["time_since_shot"] += dt
                if e["time_since_shot"] >= e["shoot_cooldown"]:
                    spawn_enemy_projectile(e)
                    e["time_since_shot"] = 0.0

            # Pickup spawning
            pickup_spawn_timer += dt
            if pickup_spawn_timer >= PICKUP_SPAWN_INTERVAL:
                pickup_spawn_timer = 0.0
                # Randomize pickup type - player never knows what they'll get
                pickup_types = [
                    "boost",  # temporary boost meter refill
                    "firerate",  # temporary fire rate buff
                    "spawn_boost",  # enemy can grab, player can shoot
                    "max_health",  # permanent max HP increase
                    "speed",  # permanent speed increase
                    "firerate_permanent",  # permanent fire rate increase
                    "bullet_size",  # permanent bullet size increase
                    "bullet_speed",  # permanent bullet speed increase
                    "bullet_damage",  # permanent bullet damage increase
                    "bullet_knockback",  # permanent knockback increase
                    "bullet_penetration",  # permanent penetration increase
                    "bullet_explosion",  # permanent explosion radius increase
                    "giant_bullets",  # 10x bullet size
                    "triple_shot",  # shoot 3 beams
                    "bouncing_bullets",  # bullets bounce off walls
                ]
                spawn_pickup(random.choice(pickup_types))

            # Pickup interactions
            for p in pickups[:]:
                pr = p["rect"]
                ptype = p["type"]

                # Player collects beneficial pickups
                if ptype != "spawn_boost" and pr.colliderect(player):
                    if ptype == "boost":
                        boost_meter = min(boost_meter_max, boost_meter + 45.0)
                    elif ptype == "firerate":
                        fire_rate_buff_t = fire_rate_buff_duration
                    elif ptype == "max_health":
                        player_max_hp += 15
                        player_hp += 15  # also heal by the same amount
                    elif ptype == "speed":
                        player_stat_multipliers["speed"] += 0.15
                    elif ptype == "firerate_permanent":
                        player_stat_multipliers["firerate"] += 0.12
                    elif ptype == "bullet_size":
                        player_stat_multipliers["bullet_size"] += 0.20
                    elif ptype == "bullet_speed":
                        player_stat_multipliers["bullet_speed"] += 0.15
                    elif ptype == "bullet_damage":
                        player_stat_multipliers["bullet_damage"] += 0.20
                    elif ptype == "bullet_knockback":
                        player_stat_multipliers["bullet_knockback"] += 0.25
                    elif ptype == "bullet_penetration":
                        player_stat_multipliers["bullet_penetration"] += 1
                    elif ptype == "bullet_explosion":
                        player_stat_multipliers["bullet_explosion_radius"] += 25.0
                    elif ptype == "giant_bullets":
                        giant_bullets_active = True
                    elif ptype == "triple_shot":
                        triple_shot_active = True
                    elif ptype == "bouncing_bullets":
                        bouncing_bullets_active = True
                    pickups.remove(p)
                    continue

                # Enemies can collect spawn boost pickup
                if ptype == "spawn_boost":
                    grabbed = False
                    for e in enemies:
                        if pr.colliderect(e["rect"]):
                            enemy_spawn_boost_level = min(10, enemy_spawn_boost_level + 1)
                            # also make current wave a bit scarier by slightly reducing remaining respawn delay
                            wave_respawn_delay = max(0.8, wave_respawn_delay - 0.15)
                            grabbed = True
                            break
                    if grabbed:
                        pickups.remove(p)
                        continue

            # Player bullets update
            for b in player_bullets[:]:
                r = b["rect"]
                v = b["vel"]
                r.x += int(v.x * dt)
                r.y += int(v.y * dt)

                # Handle bouncing bullets
                bounces_left = b.get("bounces", 0)
                if bounces_left > 0:
                    bounced = False
                    if r.left < 0:
                        v.x = abs(v.x)
                        bounced = True
                    elif r.right > WIDTH:
                        v.x = -abs(v.x)
                        bounced = True
                    if r.top < 0:
                        v.y = abs(v.y)
                        bounced = True
                    elif r.bottom > HEIGHT:
                        v.y = -abs(v.y)
                        bounced = True
                    if bounced:
                        b["bounces"] = bounces_left - 1
                        b["vel"] = v
                        # Keep bullet on screen
                        r.x = max(0, min(r.x, WIDTH - r.w))
                        r.y = max(0, min(r.y, HEIGHT - r.h))

                if rect_offscreen(r) and bounces_left == 0:
                    player_bullets.remove(b)
                    continue

                # bullets can destroy spawn_boost pickups
                hit_pickup = None
                for p in pickups:
                    if p["type"] == "spawn_boost" and r.colliderect(p["rect"]):
                        hit_pickup = p
                        break
                if hit_pickup is not None:
                    try:
                        pickups.remove(hit_pickup)
                    except ValueError:
                        pass
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

                    # apply damage (use bullet's stored damage value)
                    bullet_damage = b.get("damage", player_bullet_damage)
                    e["hp"] -= bullet_damage
                    damage_dealt += bullet_damage

                    # Apply knockback if available
                    knockback = b.get("knockback", 0.0)
                    if knockback > 0.0:
                        knockback_vec = vec_toward(e["rect"].centerx, e["rect"].centery, player.centerx, player.centery)
                        e["rect"].x += int(knockback_vec.x * knockback * 5)
                        e["rect"].y += int(knockback_vec.y * knockback * 5)
                        clamp_rect_to_screen(e["rect"])

                    # Handle explosion if available
                    explosion_radius = b.get("explosion_radius", 0.0)
                    if explosion_radius > 0.0:
                        exp_center = pygame.Vector2(b["rect"].center)
                        for other_e in enemies:
                            if other_e is e:
                                continue
                            dist = pygame.Vector2(other_e["rect"].center).distance_to(exp_center)
                            if dist <= explosion_radius:
                                # Damage falls off with distance
                                exp_damage = int(bullet_damage * (1.0 - dist / explosion_radius) * 0.6)
                                if exp_damage > 0:
                                    other_e["hp"] -= exp_damage
                                    damage_dealt += exp_damage
                                    # Log explosion hit
                                    telemetry.log_enemy_hit(
                                        EnemyHitEvent(
                                            t=run_time,
                                            enemy_type=other_e["type"],
                                            enemy_x=other_e["rect"].x,
                                            enemy_y=other_e["rect"].y,
                                            damage=exp_damage,
                                            enemy_hp_after=max(0, other_e["hp"]),
                                            killed=other_e["hp"] <= 0,
                                        )
                                    )
                                    if other_e["hp"] <= 0:
                                        try:
                                            idx = enemies.index(other_e)
                                            enemies.pop(idx)
                                            enemies_killed += 1
                                        except ValueError:
                                            pass

                    killed = e["hp"] <= 0
                    hp_after = max(0, e["hp"])

                    telemetry.log_enemy_hit(
                        EnemyHitEvent(
                            t=run_time,
                            enemy_type=e["type"],
                            enemy_x=e["rect"].x,
                            enemy_y=e["rect"].y,
                            damage=bullet_damage,
                            enemy_hp_after=hp_after,
                            killed=killed,
                        )
                    )

                    # Handle penetration
                    penetration = b.get("penetration", 0)
                    if penetration > 0:
                        # Bullet can pierce through
                        b["penetration"] = penetration - 1
                        # Continue to next enemy if penetration remains
                        if b["penetration"] > 0:
                            continue
                    else:
                        # No penetration left, remove bullet
                        player_bullets.remove(b)

                    if killed:
                        enemies.pop(hit_enemy_index)
                        enemies_killed += 1

                    # If bullet was removed, continue to next bullet
                    if b not in player_bullets:
                        continue

                # bullets interact with indestructible blocks
                for blk in blocks:
                    if r.colliderect(blk["rect"]):
                        # Bouncing bullets can bounce off blocks too
                        if b.get("bounces", 0) > 0:
                            # Simple bounce: reverse velocity
                            b["vel"] = -b["vel"]
                            b["bounces"] = b.get("bounces", 0) - 1
                        else:
                            player_bullets.remove(b)
                        break
                
                # Player bullets can destroy destructible blocks
                for db in destructible_blocks[:]:
                    if r.colliderect(db["rect"]):
                        bullet_damage = b.get("damage", player_bullet_damage)
                        db["hp"] -= bullet_damage
                        if db["hp"] <= 0:
                            destructible_blocks.remove(db)
                        # Remove bullet unless it has penetration
                        if b.get("penetration", 0) == 0:
                            player_bullets.remove(b)
                        break
                if b not in player_bullets:
                    continue

            # Enemy projectiles update
            for p in enemy_projectiles[:]:
                r = p["rect"]
                v = p["vel"]
                r.x += int(v.x * dt)
                r.y += int(v.y * dt)

                # Handle bouncing enemy projectiles
                bounces_left = p.get("bounces", 0)
                if bounces_left > 0:
                    bounced = False
                    if r.left < 0:
                        v.x = abs(v.x)
                        bounced = True
                    elif r.right > WIDTH:
                        v.x = -abs(v.x)
                        bounced = True
                    if r.top < 0:
                        v.y = abs(v.y)
                        bounced = True
                    elif r.bottom > HEIGHT:
                        v.y = -abs(v.y)
                        bounced = True
                    if bounced:
                        p["bounces"] = bounces_left - 1
                        p["vel"] = v
                        # Keep projectile on screen
                        r.x = max(0, min(r.x, WIDTH - r.w))
                        r.y = max(0, min(r.y, HEIGHT - r.h))

                if rect_offscreen(r) and bounces_left == 0:
                    enemy_projectiles.remove(p)
                    continue

                # Enemy projectiles can damage destructible blocks
                for db in destructible_blocks[:]:
                    if r.colliderect(db["rect"]):
                        db["hp"] -= enemy_projectile_damage
                        if db["hp"] <= 0:
                            destructible_blocks.remove(db)
                        enemy_projectiles.remove(p)
                        break
                if p not in enemy_projectiles:
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
        
        # Draw destructible blocks with health bars
        for db in destructible_blocks:
            pygame.draw.rect(screen, db["color"], db["rect"])
            draw_health_bar(db["rect"].x, db["rect"].y - 10, db["rect"].w, 6, db["hp"], db["max_hp"])

        for pu in pickups:
            pygame.draw.rect(screen, pu["color"], pu["rect"])

        for e in enemies:
            pygame.draw.rect(screen, e["color"], e["rect"])
            draw_health_bar(e["rect"].x, e["rect"].y - 10, e["rect"].w, 6, e["hp"], e["max_hp"])

        pygame.draw.rect(screen, (200, 60, 60), player)

        if last_move_velocity.length_squared() > 0:
            path_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            future_times = [0.2, 0.4, 0.6, 0.8, 1.0]
            for idx, t_pred in enumerate(future_times):
                future_pos = pygame.Vector2(player.center) + last_move_velocity * t_pred
                alpha = max(40, 170 - idx * 25)
                pygame.draw.circle(
                    path_overlay,
                    (120, 255, 120, alpha),
                    (int(future_pos.x), int(future_pos.y)),
                    6,
                )
            screen.blit(path_overlay, (0, 0))

        for b in player_bullets:
            draw_projectile(b["rect"], b.get("color", player_bullets_color), b.get("shape", "square"))
            # Draw explosion radius indicator if bullet has explosion
            if b.get("explosion_radius", 0.0) > 0.0:
                exp_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                radius = int(b["explosion_radius"])
                pygame.draw.circle(exp_surf, (255, 200, 0, 30), b["rect"].center, radius, 2)
                screen.blit(exp_surf, (0, 0))
        for p in enemy_projectiles:
            draw_projectile(p["rect"], p.get("color", enemy_projectiles_color), p.get("shape", "circle"))

        # HUD
        draw_health_bar(10, 10, 220, 18, player_hp, player_max_hp)
        screen.blit(font.render(f"HP: {player_hp}/{player_max_hp}", True, (230, 230, 230)), (12, 34))
        screen.blit(font.render(f"Lives: {lives}", True, (230, 230, 230)), (10, 58))
        screen.blit(font.render(f"Wave: {wave_number}", True, (230, 230, 230)), (10, 80))
        if wave_active:
            wave_text = f"Enemies: {len(enemies)}"
        else:
            wave_text = f"Next wave in: {time_to_next_wave:.1f}s"
        screen.blit(font.render(wave_text, True, (230, 230, 230)), (10, 102))
        screen.blit(font.render(f"Damage dealt: {damage_dealt}", True, (230, 230, 230)), (10, 124))
        screen.blit(font.render(f"Damage taken: {damage_taken}", True, (230, 230, 230)), (10, 146))
        screen.blit(font.render(f"Boost: {int(boost_meter)}/{int(boost_meter_max)}", True, (230, 230, 230)), (10, 190))
        if fire_rate_buff_t > 0:
            screen.blit(font.render(f"Firerate buff: {fire_rate_buff_t:.1f}s", True, (255, 220, 120)), (10, 212))
        if enemy_spawn_boost_level > 0:
            screen.blit(font.render(f"Enemy spawn boost: +{enemy_spawn_boost_level}", True, (255, 140, 220)), (10, 234))
        
        # Display permanent stat upgrades
        y_offset = 256
        if player_stat_multipliers["speed"] > 1.0:
            screen.blit(font.render(f"Speed: +{int((player_stat_multipliers['speed']-1.0)*100)}%", True, (150, 255, 150)), (10, y_offset))
            y_offset += 22
        if player_stat_multipliers["firerate"] > 1.0:
            screen.blit(font.render(f"Fire Rate: +{int((player_stat_multipliers['firerate']-1.0)*100)}%", True, (150, 255, 150)), (10, y_offset))
            y_offset += 22
        if player_stat_multipliers["bullet_damage"] > 1.0:
            screen.blit(font.render(f"Damage: +{int((player_stat_multipliers['bullet_damage']-1.0)*100)}%", True, (150, 255, 150)), (10, y_offset))
            y_offset += 22
        if player_stat_multipliers["bullet_penetration"] > 0:
            screen.blit(font.render(f"Penetration: {int(player_stat_multipliers['bullet_penetration'])}", True, (150, 255, 150)), (10, y_offset))
            y_offset += 22
        if player_stat_multipliers["bullet_explosion_radius"] > 0:
            screen.blit(font.render(f"Explosion: {int(player_stat_multipliers['bullet_explosion_radius'])}px", True, (150, 255, 150)), (10, y_offset))
            y_offset += 22
        if giant_bullets_active:
            screen.blit(font.render("GIANT BULLETS (10x)", True, (255, 200, 0)), (10, y_offset))
            y_offset += 22
        if triple_shot_active:
            screen.blit(font.render("TRIPLE SHOT", True, (255, 200, 0)), (10, y_offset))
            y_offset += 22
        if bouncing_bullets_active:
            screen.blit(font.render("BOUNCING BULLETS", True, (255, 200, 0)), (10, y_offset))
            y_offset += 22
        
        screen.blit(
            font.render(
                f"Run: {run_time:.1f}s  Shots: {shots_fired}  Hits: {hits}  Kills: {enemies_killed}  Deaths: {deaths}",
                True,
                (230, 230, 230),
            ),
            (10, 168),
        )

        # Pause overlay
        if state == STATE_PAUSED:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            draw_centered_text("Paused", HEIGHT // 2 - 140, use_big=True)
            draw_centered_text("Press C for Controls", HEIGHT // 2 - 90, color=(190, 190, 190))

            for i, opt in enumerate(pause_options):
                prefix = "> " if i == pause_selected else "  "
                draw_centered_text(prefix + opt, HEIGHT // 2 - 40 + i * 40)

            draw_centered_text("Up/Down + Enter.  P or Esc to resume.", HEIGHT // 2 + 120, color=(190, 190, 190))

        # Controls overlay
        elif state == STATE_CONTROLS:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            draw_centered_text("Controls", HEIGHT // 2 - 200, use_big=True)
            draw_centered_text("Up/Down select  Enter rebind  Esc back", HEIGHT // 2 - 150, color=(190, 190, 190))

            for i, action in enumerate(controls_actions):
                key_name = pygame.key.name(controls.get(action, pygame.K_UNKNOWN))
                prefix = "> " if i == controls_selected else "  "
                label = f"{action}: {key_name}"
                draw_centered_text(prefix + label, HEIGHT // 2 - 60 + i * 32)

            if controls_rebinding:
                draw_centered_text("Press a key...", HEIGHT // 2 + 160, color=(255, 230, 120))

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
        max_wave=wave_number,
    )
    telemetry.close()
    pygame.quit()

    print(f"Saved run_id={run_id} to game_telemetry.db")
