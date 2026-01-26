# Enemy Reference

This document describes all enemy types, their spawn rules, colors, behavior, and projectile traits. Data is taken from `config_enemies.py`, `constants.py`, `enemies.py`, `systems/spawn_system.py`, `systems/ai_system.py`, `systems/movement_system.py`, and `game.py`.

---

## Runtime Appearance (Colors)

**All enemies use a single unified color at runtime**, regardless of template. Template `color` values are overridden when enemies are created.

| What            | Value        | Source / note                                               |
|-----------------|-------------|-------------------------------------------------------------|
| Enemy body      | `(200, 50, 50)` | `constants.ENEMY_COLOR` — applied in `make_enemy_from_template()` |
| Projectile body | Per template or `(200, 200, 200)` | `template["projectile_color"]` or `constants.ENEMY_PROJECTILES_COLOR` |

So in-game, every enemy is drawn with the same red body color; projectile color can differ by type.

---

## Global Projectile Defaults

Used when a projectile has no explicit `damage` or when spawning does not set it:

| Constant / usage              | Value  | Meaning                                      |
|------------------------------|--------|----------------------------------------------|
| `ENEMY_PROJECTILE_SIZE`      | (10, 10) | Pixel size of enemy projectiles              |
| `ENEMY_PROJECTILE_DAMAGE`    | 11     | Defined in constants; spawn uses 10 if unset |
| Default damage at spawn      | 10     | `enemy.get("flame_damage", enemy.get("damage", 10))` |
| Default damage in collision  | 10     | `proj.get("damage", 10)` when hitting player/friendlies |

Flamethrower is the only type that sets a different projectile damage via `flame_damage` (8).

---

## Spawn Rates and Wave Logic

### Spawn configuration (`config_enemies.py`)

| Constant / logic               | Value | Effect |
|--------------------------------|-------|--------|
| `BASE_ENEMIES_PER_WAVE`        | 12    | Base count before multipliers |
| `MAX_ENEMIES_PER_WAVE`         | 72    | Cap per wave |
| `ENEMY_SPAWN_MULTIPLIER`       | 3.5   | Applied to effective base count |
| Wave count formula             | `min(int((BASE + 2*(wave-1)) * diff_spawn * ENEMY_SPAWN_MULTIPLIER), MAX_ENEMIES_PER_WAVE)` | |

### Difficulty multipliers (`constants.difficulty_multipliers`)

| Difficulty | enemy_hp | enemy_speed | enemy_spawn |
|------------|----------|-------------|-------------|
| EASY       | 0.7      | 0.8         | 0.8         |
| NORMAL     | 1.0      | 1.0         | 1.0         |
| HARD       | 1.5      | 1.3         | 1.5         |

### Who spawns when

- **Waves 1 and 2 (regular):** Enemies are chosen at random from all non-ambient templates. Count is scaled by wave number, difficulty, level, and `ENEMY_SPAWN_MULTIPLIER`, then clamped to `MAX_ENEMIES_PER_WAVE`.
- **Wave 3 (boss wave):** One boss (`FINAL_BOSS`) is spawned at screen center; no regular wave pool.
- **Ambient:** On every wave start (including boss waves), **3–5** stationary “ambient” enemies are spawned at random non-overlapping positions.
- **Spawner minions:** Spawner-type enemies add minions over time (see “spawner” below).

### Size-class caps (per wave)

When picking the next enemy, the spawner enforces per–size-class limits:

| Size class   | Cap |
|-------------|-----|
| basic       | 20  |
| large       | 10  |
| super_large | 2   |

If a roll would exceed a cap, another template from a different size class is chosen instead. Queen is further limited to at most **3 per wave**.

### HP and speed scaling

For non-queen, non-ambient enemies, scaling uses:

- **HP scale:** `(1 + 0.15*(wave-1)) * diff_mult["enemy_hp"] * level_mult * wave_in_level_mult`  
  Then `hp = int(t["hp"] * hp_scale * ENEMY_HP_SCALE_MULTIPLIER * 10)` capped by `ENEMY_HP_CAP * 10`.
- **Speed scale:** `(1 + 0.05*(wave-1)) * diff_mult["enemy_speed"] * level_mult * wave_in_level_mult`  
  Then `speed = template_speed * speed_scale * ENEMY_SPEED_SCALE_MULTIPLIER`.

| Scaling constant              | Value | Note |
|------------------------------|-------|------|
| `ENEMY_HP_SCALE_MULTIPLIER`  | 1.1   | 110% |
| `ENEMY_SPEED_SCALE_MULTIPLIER` | 1.1 | 110% |
| `ENEMY_FIRE_RATE_MULTIPLIER` | 7.5   | Cooldown is divided by this (much faster fire) |
| `ENEMY_HP_CAP`               | 300   | Non-queen HP capped at `ENEMY_HP_CAP * 10` |
| `QUEEN_FIXED_HP`             | 5000  | Queen ignores HP scaling |

Ambient enemies are created with `hp_scale=1.0`, `speed_scale=1.0` and keep template HP; speed stays 0 (stationary).

---

## Behavior Overview

- **Targeting:** Enemies use `find_nearest_threat()`: they prefer a **dropped ally** within 350 px, otherwise the **player**, otherwise the nearest friendly AI.
- **Movement:** Implemented in `movement_system._update_enemies()`:
  - **Ambient:** No movement.
  - **Patrol:** Moves along the screen border in a rectangular patrol (four sides).
  - **Non-boss, non-patrol:** When the player is inside the “main area,” they move toward the **nearest point on the outer perimeter** of the play area (patrol-style); when the player is outside, they chase the nearest threat. They also use grenade bait (approach/retreat), stuck escaping, random wander, and **dodge**: if player/friendly bullets are within 220 px and will reach in &lt; 0.5 s, they add a perpendicular sidestep to their direction.
- **Shooting:** Handled in `ai_system._update_enemy_ai()`. Non-reflector enemies use `shoot_cooldown`; when it elapses and there is a target, they fire either a normal shot or a **predictive** shot (`is_predictive`). Cooldown is divided by `ENEMY_FIRE_RATE_MULTIPLIER` (7.5) for most types.

---

## Enemy Templates (by type)

Below, “body color” is the template value; in-game all use `ENEMY_COLOR (200,50,50)`. Projectile color is what is actually used for their shots.

---

### ambient

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (150, 80, 200) |
| **Size**  | 26×26 |
| **HP**    | 40 (no scaling) |
| **Speed** | 0 (stationary) |
| **Size class** | — |
| **Spawn** | 3–5 per wave start, random positions; excluded from regular wave pool |

**Behavior:** Does not move. Fires a single **rocket** at the current threat every **6 s** (not affected by fire-rate multiplier). No other weapons.

**Projectile:**  
Speed 220, shape circle, color (200, 100, 80). Damage uses default (10).

---

### pawn

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (180, 180, 180) |
| **Size**  | 28×28 |
| **HP**    | 50 (scaled, cap applies) |
| **Speed** | 80 (scaled) |
| **Size class** | basic |
| **Shoot cooldown** | 1.0 s (then / 7.5) |
| **Projectile** | speed 300, circle, (200,200,200), damage 10 |

Standard basic unit. Chases threat, uses normal (non-predictive) aim.

---

### suicide

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (255, 50, 50) |
| **Size**  | 48×48 |
| **HP**    | 30 (scaled) |
| **Speed** | 90 (scaled) |
| **Size class** | — (no size_class) |
| **Shoot cooldown** | 999 (does not shoot) |

**Behavior:** Does not shoot. When within **50 px** of the player, detonates: **500** damage in **150** px radius (explosion_range). Ignores shield for damage application; overshield/HP apply as usual. Dies when detonating.

---

### grunt

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (220, 80, 80) |
| **Size**  | 28×28 |
| **HP**    | 60 (scaled) |
| **Speed** | 90 (scaled) |
| **Size class** | basic |
| **Shoot cooldown** | 0.9 s (then / 7.5) |
| **Projectile** | speed 320, **square**, (180,220,255), damage 10 |

Basic shooter with square bullets.

---

### heavy

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (220, 120, 80) |
| **Size**  | 32×32 |
| **HP**    | 80 (scaled) |
| **Speed** | 70 (scaled) |
| **Size class** | large |
| **Shoot cooldown** | 1.2 s (then / 7.5) |
| **Projectile** | speed 280, circle, (255,190,120), damage 10 |

Slower, tougher large unit.

---

### stinky

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (220, 80, 80) |
| **Size**  | 28×28 |
| **HP**    | 60 (scaled) |
| **Speed** | 110 (scaled) |
| **Size class** | basic |
| **Shoot cooldown** | 0.9 s (then / 7.5) |
| **Projectile** | speed 320, **diamond**, (180,220,255), damage 10 |

Faster basic with diamond shots.

---

### baka

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (100, 80, 80) |
| **Size**  | 28×28 |
| **HP**    | 300 (scaled, then capped) |
| **Speed** | 150 (scaled) |
| **Size class** | basic |
| **Shoot cooldown** | 0.1 s (then / 7.5) |
| **Projectile** | speed 500, square, (255,120,180), damage 10 |

**Behavior:** **Predictive** aim: shoots where the target will be. Very high fire rate.

---

### neko neko desu

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (100, 80, 0) |
| **Size**  | 28×28 |
| **HP**    | 20 (scaled) |
| **Speed** | 160 (scaled) |
| **Size class** | basic |
| **Shoot cooldown** | 0.01 s (then / 7.5) |
| **Projectile** | speed 500, circle, (200,255,140), damage 10 |

Extremely fast fire, low HP, high speed.

---

### BIG NEKU

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (100, 200, 0) |
| **Size**  | 28×28 |
| **HP**    | 300 (scaled, capped) |
| **Speed** | 60 (scaled) |
| **Size class** | basic |
| **Shoot cooldown** | 1.0 s (then / 7.5) |
| **Projectile** | speed 700, diamond, (160,200,255), damage 10 |

Tanky basic, fast projectiles.

---

### bouncer

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (255, 100, 100) |
| **Size**  | 30×30 |
| **HP**    | 70 (scaled) |
| **Speed** | 85 (scaled) |
| **Size class** | large |
| **Shoot cooldown** | 1.5 s (then / 7.5) |
| **Projectile** | speed 350, square, (255,150,150), damage 10, **bounces: 10** |

**Projectile trait:** Bullets bounce off walls up to 10 times.

---

### shield enemy

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (100, 150, 200) |
| **Size**  | 32×32 |
| **HP**    | 100 (scaled) |
| **Speed** | 60 (scaled) |
| **Size class** | large |
| **Shoot cooldown** | 1.0 s (then / 7.5) |
| **Projectile** | speed 300, circle, (150,200,255), damage 10 |

**Behavior:** **has_shield**: front shield blocks/reflects player bullets. Reflected shots use **reflect_damage_mult 1.5**. Shield rotates toward current threat. If hit from the flank (side/behind), behaves like a normal enemy.

---

### reflector

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (200, 150, 100) |
| **Size**  | 36×36 |
| **HP**    | 150 (scaled) |
| **Speed** | 40 (scaled) |
| **Size class** | large |
| **Shoot cooldown** | 999 (does not shoot) |

**Behavior:** **has_reflective_shield**: no gun; shield turns toward threat (**turn_speed** 0.5). Absorbs and reflects shots (shield_hp and fire-back logic in collision). Does not use normal or predictive shooting.

---

### spawner

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (150, 50, 150) |
| **Size**  | 40×40 |
| **HP**    | 120 (scaled) |
| **Speed** | 30 (scaled) |
| **Size class** | large |
| **Shoot cooldown** | 999 (does not shoot) |

**Behavior:** **is_spawner**. Every **5 s** (**spawn_cooldown**), spawns one minion (up to **max_spawns = 3** total). Minion pool = all templates except spawner, FINAL_BOSS, and ambient; same size-class caps (20 basic, 10 large, 2 super_large) apply. Minions are created with `hp_scale=1.0`, `speed_scale=1.0` and linked to this spawner; when the spawner dies, all its minions are removed.

---

### queen

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (100, 0, 0) |
| **Size**  | 32×32 |
| **HP**    | **5000** (fixed, no scaling) |
| **Speed** | 240 (template 80 × 3; uses ENEMY_SPEED_SCALE_MULTIPLIER only) |
| **Size class** | — |
| **Shoot cooldown** | 0.5 s (then / 7.5) |
| **Projectile** | speed 350, circle, (150,0,0), damage 10 |

**Behavior:** Player-clone style. **Predictive** aim. Shield toggles on/off in phases (duration 10–20 s off, 5–10 s on). Can use **grenades** (cooldown 5 s) and **missiles** (cooldown 10 s, damage from `ctx["missile_damage"]`). **Rage:** after taking 300–500 damage (random per instance), enters rage for 5 s. Capped at **3 per wave**.

---

### patrol

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (150, 100, 200) |
| **Size**  | 32×32 |
| **HP**    | 150 (scaled) |
| **Speed** | 100 (scaled) |
| **Size class** | large |
| **Shoot cooldown** | 0.5 s (then / 7.5) |
| **Projectile** | speed 400, circle, (200,150,255), damage 10 |

**Behavior:** **is_patrol**. Moves along the screen border in a four-sided loop (margin 50 px), independent of player position. Shoots at nearest threat when in range.

---

### flamethrower

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (220, 100, 40) |
| **Size**  | 30×30 |
| **HP**    | 55 (scaled) |
| **Speed** | 70 (scaled) |
| **Size class** | basic |
| **Shoot cooldown** | 0.15 s (then / 7.5) |
| **Projectile** | speed 380, circle, (255,120,40), **damage 8** (flame_damage) |

**Behavior:** **is_flamethrower**. Same shooting logic as normal enemies; projectile damage is **flame_damage** (8), not the default 10.

---

### super_large

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (80, 60, 100) |
| **Size**  | 128×128 |
| **HP**    | 800 × 1.5 × hp_scale (no normal cap) |
| **Speed** | 20 (scaled) |
| **Size class** | super_large |

**Behavior:** Does **not** use normal projectiles. **Fires rockets** every **5 s** (player-seeking, damage 400, radius 100). **Grenades** every **8 s**: damage **400**, radius **120**, **can_use_grenades_player_allies_only** (hits only player and allies, not enemies). No standard bullets.

---

### large_laser

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (120, 80, 180) |
| **Size**  | 48×48 |
| **HP**    | 120 × hp_scale × 10, cap ENEMY_HP_CAP×10 |
| **Speed** | 50 (scaled) |
| **Size class** | large |
| **Shoot cooldown** | 999 (no regular shots) |

**Behavior:** **fires_laser**. Single beam toward threat. **Laser:** interval 3 s, **deploy 2 s** (no damage during deploy), then **0.4 s** active. Damage **80×60** per second in collision (i.e. 80 per second in code, scaled by dt×60). Length 600, color (180,100,255), width 4.

---

### super_large_triple_laser

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (60, 40, 120) |
| **Size**  | 128×128 |
| **HP**    | 1000 × 1.5 × hp_scale (no normal cap) |
| **Speed** | 18 (scaled) |
| **Size class** | super_large |
| **Shoot cooldown** | 999 (no regular shots) |

**Behavior:** **fires_triple_laser**. Three beams with **±15°** spread. Interval 4 s, deploy 2 s, **0.5 s** active. Damage **120×60** per second per beam. Length 700, spread_deg 15, color (200,80,255), width 6.

---

### FINAL_BOSS (boss)

| Property   | Value |
|-----------|--------|
| **Body color (template)** | (255, 0, 0) → runtime ENEMY_COLOR |
| **Size**  | 100×100 |
| **HP**    | 300 × level scaling × difficulty × formula, cap 15000 |
| **Speed** | 50 × ENEMY_SPEED_SCALE_MULTIPLIER |
| **Shoot cooldown** | 0.5 s (then / 7.5) |
| **Projectile** | speed 400, circle, (255,50,50), damage 10 (default) |

**Spawn:** Wave 3 of each level only, one per wave, at screen center. **Behavior:** Uses normal enemy shooting (spawn_enemy_projectile), so projectiles use default damage 10. Boss-specific `spawn_boss_projectile()` exists but is not used in the current AI loop; if it were used, those projectiles would also default to 10 in collisions (no "damage" key set). **Phases:** phase 1 at start; phase 2 at 66% HP, phase 3 at 33% HP (phase_hp_thresholds [0.66, 0.33]).

---

## Projectile Traits Summary

| Trait | Enemies | Effect |
|-------|---------|--------|
| **Shape: circle** | pawn, heavy, ambient, neko neko desu, BIG NEKU, shield enemy, queen, patrol, flamethrower, boss | Drawn as circle |
| **Shape: square** | grunt, baka, bouncer | Drawn as square |
| **Shape: diamond** | stinky, reflector (template; doesn’t shoot), large_laser/super_large_triple (beams) | Drawn as diamond; stinky uses diamond bullets |
| **Bounces** | bouncer | Up to 10 bounces |
| **Predictive** | baka, queen | Aim at predicted player position |
| **Damage override** | flamethrower | 8 (flame_damage); others 10 unless set |
| **Lifetime** | Predictive and boss projectiles (when spawn_boss_projectile is used) | 5 s then removed |

---

## File Reference

- **Templates & scaling:** `config_enemies.py` (ENEMY_TEMPLATES, BOSS_TEMPLATE, BASE/MAX_ENEMIES_PER_WAVE, ENEMY_SPAWN_MULTIPLIER, HP/SPEED/FIRE_RATE multipliers, QUEEN_FIXED_HP).
- **Unified color & projectile defaults:** `constants.py` (ENEMY_COLOR, ENEMY_PROJECTILES_COLOR, ENEMY_PROJECTILE_SIZE, ENEMY_PROJECTILE_DAMAGE).
- **Creation from template:** `enemies.make_enemy_from_template()` (applies scaling and overrides color to ENEMY_COLOR).
- **Spawn rules:** `systems/spawn_system.py` (waves, boss, ambient, spawner minions, size-class caps).
- **Targeting:** `enemies.find_nearest_threat()` (dropped ally &lt; 350 px, else player, else friendlies).
- **Movement:** `systems/movement_system._update_enemies()` (chase, patrol, dodge, stuck, wander, grenade bait).
- **Shooting & specials:** `systems/ai_system._update_enemy_ai()` (normal/predictive shots, ambient rockets, queen shield/missiles/grenades, suicide detonate, reflector shield, super_large rockets/grenades, lasers).
- **Projectile spawning:** `game.spawn_enemy_projectile()`, `game.spawn_enemy_projectile_predictive()` (and optionally `spawn_boss_projectile()`).
- **Damage application:** `systems/collision_system` (player/friendly/block hits; beams; grenades; missiles).
