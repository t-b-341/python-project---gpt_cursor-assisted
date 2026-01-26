# Globals and Module-Level State Audit

Audit of global variables, module-level state, and singleton-style Pygame usage across the repo. **No code was changed**; this is analysis only.

---

## 1. List of globals and where they are declared

All declarations below are in **game.py** unless noted.

### 1.1 Display / Pygame resources (assigned in `main()`, declared global there)

| Name | Declared | Assigned | Notes |
|------|----------|----------|--------|
| `WIDTH` | line 115 | line 141 (in main) | Placeholder 1920 at module level (104) |
| `HEIGHT` | line 115 | line 141 (in main) | Placeholder 1080 at module level (105) |
| `screen` | line 115 | line 142 | `pygame.display.set_mode(...)` |
| `clock` | line 115 | line 145 | `pygame.time.Clock()` |
| `font` | line 115 | line 146 | `pygame.font.SysFont(None, 28)` |
| `big_font` | line 115 | line 147 | `pygame.font.SysFont(None, 56)` |
| `small_font` | line 115 | line 148 | `pygame.font.SysFont(None, 20)` |

### 1.2 Telemetry and run

| Name | Declared | Module-level assignment | Notes |
|------|----------|-------------------------|--------|
| `telemetry` | line 116 | 1187: `None` | Set in main when user enables telemetry (611–613) |
| `telemetry_enabled` | line 116 | 1186: `False` | Toggle from menu |
| `run_started_at` | line 128 | 1188: `datetime.now(...)` | ISO string for run |

### 1.3 Flow state and menu (also mirrored on GameState in places)

| Name | Module-level assignment (game.py) |
|------|-----------------------------------|
| `state` | 1192: `STATE_MENU` |
| `previous_game_state` | 1193: `None` |
| `menu_section` | 1194 |
| `ui_show_metrics_selected` | 1195 |
| `ui_show_hud` | 1196 |
| `ui_options_selected` | 1197 |
| `endurance_mode_selected` | 1198 |
| `use_character_profile` | 1201 |
| `use_character_profile_selected` | 1202 |
| `character_profile_selected` | 1203 |
| `custom_profile_stat_selected` | 1205 |
| `custom_profile_stats` | 1206–1214 |
| `side_quests` | 1215–1223 |
| `wave_damage_taken` | 1224 |
| `testing_mode` | 1226 |
| `invulnerability_mode` | 1227 |
| `beam_selection_selected` | 1228 |
| `beam_selection_pattern` | 1229 |
| `current_level` | 1232 |
| `max_level` | 1233 |
| `wave_in_level` | 1234 |
| `difficulty` | 1238 |
| `difficulty_selected` | 1239 |
| `aiming_mode` | 1242 |
| `aiming_mode_selected` | 1243 |
| `player_class` | 1246 |
| `player_class_selected` | 1247 |
| `mod_enemy_spawn_multiplier` | 1250 |
| `mod_custom_waves_enabled` | 1251 |
| `custom_waves` | 1252 |
| `ui_show_health_bars` | 1255–1261 |
| `ui_telemetry_enabled_selected` | 1261 |
| `aiming_mechanic` | 1264 |
| `pause_selected` | 1267 |
| `continue_blink_t` | 1268 |
| `controls_selected` | 1271 |
| `controls_rebinding` | 1272 |

### 1.4 Controls

| Name | Module-level assignment |
|------|-------------------------|
| `controls` | 1180: `{}` (loaded in main() ~167 when empty) |

### 1.5 Player-related (many duplicated on GameState)

| Name | Module-level assignment |
|------|-------------------------|
| `player` | 1277: `None` (alias for `game_state.player_rect` in main) |
| `player_speed` | 1278 |
| `player_max_hp` | 1279 |
| `player_hp` | 1280 |
| `overshield` | 1283 |
| `overshield_recharge_timer` | 1285 |
| `shield_recharge_timer` | 1287 |
| `lives` | 1291 |
| `last_horizontal_key` | 1294 |
| `last_vertical_key` | 1295 |
| `last_move_velocity` | 1296 |
| `jump_cooldown_timer` | 1299 |
| `jump_velocity` | 1300 |
| `jump_timer` | 1301 |
| `is_jumping` | 1302 |
| `previous_boost_state` | 1305 |
| `previous_slow_state` | 1306 |
| `boost_meter` | 1309 |
| `fire_rate_buff_t` | 1312 |
| `fire_rate_buff_duration` | 1313 |
| `fire_rate_mult` | 1314 |
| `shield_active` | 1317 |
| `shield_duration_remaining` | 1318 |
| `shield_cooldown` | 1319 |
| `shield_cooldown_remaining` | 1320 |
| `shield_recharge_cooldown` | 1321 |
| `shield_recharge_timer` | 1322 |
| `player_stat_multipliers` | 1325–1337 |
| `random_damage_multiplier` | 1338 |
| `current_weapon_mode` | 1347 |
| `previous_weapon_mode` | 1348 |
| `laser_time_since_shot` | 1353 |
| `wave_beam_time_since_shot` | 1357 |
| `wave_beam_pattern_index` | 1358 |
| `grenade_time_since_used` | 1676 |
| `missile_time_since_used` | 1680 |
| `missile_explosion_radius` | 1681 |
| `missile_speed` | 1682 |
| `player_time_since_shot` | 1671 |
| `player_bullet_shape_index` | 1672 |
| `player_current_zones` | 1659 |
| `player_health_regen_rate` | 1662 |
| `pickup_spawn_timer` | ~1895 (in similar block) |

Values such as `boost_meter_max`, `shield_recharge_cooldown`, `overshield_recharge_cooldown`, `shield_duration`, etc. are imported from **constants.py** and referenced in main and in helpers (e.g. `apply_pickup_effect`).

### 1.6 Level geometry and obstacles (module-level data)

| Name | Approx. lines |
|------|----------------|
| `hazard_obstacles` | 1362–~1440 |
| `blocks` | 1442 |
| `destructible_blocks` | 1445–1461 |
| `moveable_destructible_blocks` | 1463–~1473 |
| `giant_blocks` | 1475–1481 |
| `super_giant_blocks` | 1482–1490 |
| `trapezoid_blocks` | 1491 |
| `triangle_blocks` | 1492 |
| `left_trap_height`, `left_gap`, … (trapezoid/triangle layout) | 1495–~1645 |
| `moving_health_zone` | 1648–1657 |
| `teleporter_pads` | (used in level_context; defined in same geometry block) |
| `health_zone_overlaps` | 1743 |
| `max_health_zone_attempts` | 1744 |
| `TELEPORTER_SIZE` | 1776 |
| `weapon_selection_options` | (from constants or set in main; referenced in menu) |
| `friendly_ai_templates` | 1836 (alias for FRIENDLY_AI_TEMPLATES) |
| `overshield_max`, `grenade_cooldown`, `missile_cooldown`, `ally_drop_cooldown` | imported / constants, used in level_context and apply_pickup_effect |

`clamp_rect_to_screen(r)` at 1919 uses module-level **WIDTH** and **HEIGHT** and takes only `r`.

---

## 2. Functions / modules that implicitly depend on these globals

### 2.1 In game.py (use globals without receiving them as parameters)

- **`clamp_rect_to_screen(r)`** (1919)  
  Uses `WIDTH`, `HEIGHT`. No width/height arguments.

- **`update_hazard_obstacles(dt)`** (2648)  
  Uses `global hazard_obstacles, current_level` and **WIDTH**, **HEIGHT** (2684–2692). No context/state args.

- **`apply_pickup_effect(pickup_type, state)`** (3209)  
  Uses: `boost_meter_max`, `fire_rate_buff_duration`, `telemetry_enabled`, `telemetry`, and `global ally_drop_cooldown` (3246). These are not passed in.

- **`spawn_pickup(pickup_type)`** (2731)  
  Uses module-level `state` (flow state, not GameState), `state.pickups`, `moving_health_zone`, and `pickups.append`. This is inconsistent with the rest of the game (flow `state` is not a GameState), and **spawn_pickup is never called** in the repo. It is effectively dead and would fail if ever used.

- **`spawn_weapon_in_center(weapon_type, state)`** (2769)  
  Uses **WIDTH**, **HEIGHT** (2775–2778). Does not take screen or dimensions.

- **`_make_level_context()`** (inside main, 178–231)  
  Captures in its closure: `WIDTH`, `HEIGHT`, `blocks`, `destructible_blocks`, `moveable_destructible_blocks`, `giant_blocks`, `super_giant_blocks`, `trapezoid_blocks`, `triangle_blocks`, `hazard_obstacles`, `moving_health_zone`, `telemetry`, `telemetry_enabled`, `difficulty`, `overshield_recharge_cooldown`, `ally_drop_cooldown`, and several callables that themselves use globals (`clamp_rect_to_screen`, `kill_enemy`, `reset_after_death`, `create_pickup_collection_effect`, `apply_pickup_effect`, etc.). So the whole level_context is backed by globals.

- **Main loop**  
  Reads/writes the globals declared at 115–128 and the flow/menu/options variables above. Pygame init and `screen`/`clock`/fonts setup happen only inside **main()** (130, 139, 142, 145–148); there is no Pygame init at import time.

### 2.2 In other modules

- **enemies.py**  
  - `clamp_rect_to_screen(r, width, height)` takes width/height; no globals.  
  - Telemetry is passed in as an argument to the spawn-logging path.  
  No implicit reliance on game.py globals.

- **state.py**  
  Defines `GameState` only. No use of screen/clock/fonts/telemetry/config.

- **rendering.py**  
  - All drawing uses `screen` and `ctx` (or state) passed in.  
  - Module-level caches: `_wall_texture_cache`, `_health_bar_cache`, `_hud_text_cache`, `_trapezoid_surface_cache`, `_triangle_surface_cache`.  
  No use of global screen/clock/fonts.

- **screens/** (pause, high_scores, name_input, gameplay)  
  All use `(screen, game_state, ctx)` or `(screen, state, ctx)`. Fonts and dimensions come from `ctx["WIDTH"]`, `ctx["font"]`, etc. No imports from game and no global screen/clock/fonts.

- **systems/** (movement_system, spawn_system, collision_system, ai_system, ui_system, telemetry_system)  
  Use `state` and `ctx` (or `state.level_context`). They get telemetry, dimensions, blocks, callbacks from `ctx` / `level_context`, not from globals. No direct reliance on game.py globals.

---

## 3. Modules that access screen / clock / fonts / telemetry / config through globals

- **game.py**  
  - **Screen/clock/fonts:** Used only inside `main()` and in helpers that are either (a) called from main, or (b) invoked via `level_context` callbacks. The main loop builds `screen_ctx` and `gameplay_ctx` from its local `screen`, `font`, `big_font`, `small_font`, `WIDTH`, `HEIGHT`, and passes them to screen handlers and `gameplay_render`. So de facto “global” access is only within game.py (main + its callees that use module-level names).
  - **Telemetry/config:** `telemetry`, `telemetry_enabled`, `difficulty`, and many menu/options variables are module-level. They are read/written in main and in `apply_pickup_effect`, and injected into `game_state.level_context` (e.g. `ctx["telemetry"]`, `ctx["difficulty"]`) so that **spawn_system**, **collision_system**, **ai_system**, and **enemies** (when called with that context) see them only via `ctx`, not by importing game.

- **No other module** imports `game` or reads screen/clock/fonts/telemetry/config from globals. They receive everything via `screen`, `game_state`, and `ctx` (or `state.level_context`).

So the only place that “accesses screen/clock/fonts/telemetry/config through globals” is **game.py** (main and the helpers listed in §2.1 that use module-level names). Other modules use them only when provided in `ctx` or as arguments.

---

## 4. Recommendation: AppContext vs GameState vs local

### 4.1 AppContext (per-run, non–game-play state; created after Pygame init)

Put here things that are shared by the process for the lifetime of the window and that are not “current game state”:

- **screen**, **clock**, **font**, **big_font**, **small_font**
- **WIDTH**, **HEIGHT**
- **controls** (key bindings; load once per run)
- **telemetry**, **telemetry_enabled** (optional; could stay “top-level optional” if you prefer)
- **run_started_at** (if needed for telemetry)

So: **AppContext** = { screen, clock, font, big_font, small_font, WIDTH, HEIGHT, controls, telemetry?, telemetry_enabled?, run_started_at? }.  
Main would build one `AppContext` after `pygame.display.set_mode` and pass it (or its fields) into the loop and into any code that currently relies on those globals.

### 4.2 GameState (already in state.py)

Use for all **mutable per-session and per-game state** that already lives on `GameState`, and move remaining gameplay/menu flow into it where it still lives as globals:

- **Flow / UI:** `current_screen`, `previous_screen`, `menu_section`, `pause_selected`, `continue_blink_t`, `controls_selected`, `controls_rebinding`, `title_confirm_quit`, `menu_confirm_quit`
- **Menu/options persistence:** difficulty, aiming_mode, use_character_profile, player_class, custom_profile_*, beam_selection_*, endurance_mode_selected, ui_show_*, ui_telemetry_enabled_selected, testing_mode, invulnerability_mode, etc. Either keep as “session options” on `GameState” or in a small “SessionOptions” attached to it.
- **Level/wave:** current_level, max_level, wave_in_level, wave_damage_taken, side_quests (already on state in some form)
- **Player and combat:** already largely on GameState; remove duplicates from module-level (player_speed, player_hp, boost_meter, shield_*, etc.) so **GameState is the single source of truth** for these.

So: **GameState** = existing state.py fields + anything that is “current run / current menu / current game” that is still global in game.py.

### 4.3 Level/geometry and “level context” data

- **Level geometry and static obstacles:**  
  `blocks`, `trapezoid_blocks`, `triangle_blocks`, `destructible_blocks`, `moveable_destructible_blocks`, `giant_blocks`, `super_giant_blocks`, `hazard_obstacles`, `moving_health_zone`, `teleporter_pads`  
  Recommendation: keep as **level data** (e.g. a `LevelGeometry` or similar) built once per run (or per level) and pass it in `level_context` or as part of a “level” object. They should not be global; they can be created in main (or a level-loader) and then only referenced via `game_state.level_context` or an explicit parameter.

- **level_context**  
  Should be built in main (or a helper) from **AppContext** (WIDTH, HEIGHT, etc.) and the chosen **LevelGeometry**, and from callbacks that take explicit arguments (e.g. `clamp_rect_to_screen(r, w, h)`). That way `update_hazard_obstacles`, `clamp_rect_to_screen`, and movement/collision helpers do not touch globals.

### 4.4 Stay local to main (or small scopes)

- **Loop-only temporaries:** e.g. `state`, `previous_game_state`, `menu_section`, etc. can be local in main and read/written to `game_state` at the start/end of each iteration, until they are fully migrated to GameState.
- **FPS, theme, and other loop constants** can stay as local or const in main.

### 4.5 Concrete refactor targets (for later, not done in this audit)

- **`clamp_rect_to_screen(r)`**  
  Either take `(r, width, height)` and pass WIDTH/HEIGHT from context, or take `(r, ctx)` and use `ctx["width"]`, `ctx["height"]`. Prefer the explicit (r, w, h) signature to match enemies.py and avoid global WIDTH/HEIGHT.

- **`update_hazard_obstacles(dt)`**  
  Take `(dt, hazard_obstacles, current_level, width, height)` or `(dt, level_geometry, ctx)` so it no longer uses `global hazard_obstacles, current_level` or WIDTH/HEIGHT.

- **`apply_pickup_effect(pickup_type, state)`**  
  Take all needed values explicitly or via a small context (e.g. `boost_meter_max`, `fire_rate_buff_duration`, `telemetry`, `telemetry_enabled`, `ally_drop_cooldown` or a setter for cooldown) so it does not read globals.

- **`spawn_weapon_in_center(weapon_type, state)`**  
  Take `(weapon_type, state, width, height)` or get dimensions from `state.level_context` / AppContext.

- **`spawn_pickup`**  
  Either remove as dead code or rewrite to take `(pickup_type, state)` and use `state.pickups` and level data from context only.

- **Level context construction**  
  Build `level_context` from an **AppContext** + **LevelGeometry** + **GameState** (or session options), and pass telemetry/difficulty/cooldowns explicitly or via a narrow “runtime config” object, so that nothing in level_context or in systems depends on game.py module-level globals.

---

**Summary**

- **Globals:** All substantive globals are in **game.py** (display, telemetry, flow/menu/options, player-related, level geometry, and several helpers that use them).
- **Implicit dependencies:** In game.py, `clamp_rect_to_screen`, `update_hazard_obstacles`, `apply_pickup_effect`, `spawn_weapon_in_center`, and the unused `spawn_pickup` depend on globals`; level_context is fed by closure over many of these globals.
- **Other modules:** Only use screen/clock/fonts/telemetry/config via arguments and `ctx` / `level_context`; they do not import or read from game globals.
- **AppContext:** screen, clock, fonts, WIDTH, HEIGHT, controls, and optionally telemetry/run_started_at.
- **GameState:** All mutable per-run and per-game state; migrate remaining flow/menu/player/level globals here (or into a small SessionOptions/LevelGeometry) so that game.py no longer relies on module-level mutable state for behavior.
