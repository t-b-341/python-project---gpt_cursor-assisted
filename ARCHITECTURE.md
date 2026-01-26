# Architecture: systems, definitions, and scenes

## How systems are registered and updated

Simulation systems are listed in **`systems/registry.py`** as `SIMULATION_SYSTEMS`.  
The game’s fixed-step loop runs them in order each tick:

1. **Movement** — player, enemies, bullets.
2. **Collision** — hits, damage, pickups, teleporters.
3. **Spawn** — wave timers, spawner minions, next-wave.
4. **AI** — enemy and friendly targeting/shooting.

Order is important: movement updates positions before collision; collision runs before spawn and AI so spawn and AI see the latest state.  
The main loop uses `SIMULATION_SYSTEMS` from `systems.registry`; the gameplay screen uses `GAMEPLAY_SYSTEMS` from `systems` (same list plus telemetry).

## How enemy and projectile definitions are structured and extended

- **Enemies:** `config/enemy_defs.py` exposes `get_enemy_def(type_id)`. Defs are built from `config_enemies.ENEMY_TEMPLATES` and `BOSS_TEMPLATE`, with normalized fields (`type_id`, `base_health`, `move_speed`, `sprite_id`, `score_value`, `behavior_flags`). Use `clear_enemy_def_cache()` in tests or for hot-reload. Spawn and other logic use `get_enemy_def("ambient")`, `get_enemy_def("FINAL_BOSS")`, etc., instead of scanning templates by hand.

- **Projectiles:** `config/projectile_defs.py` exposes `get_projectile_def(type_id)`. Supported `type_id`s include `player_basic`, `player_triple`, `player_giant`, `enemy_default`. Defs hold speed, damage, size, color, and weapon-style fields. Use `clear_projectile_def_cache()` when needed. Spawn and bullet creation use these defs where it fits so base stats stay data-driven.

## How scenes and the scene stack manage screens and gameplay

- **Scenes** live under `scenes/`. Each scene implements: `state_id()`, `handle_input(events, game_state, ctx)`, `update(dt, game_state, ctx)`, `render(render_ctx, game_state, ctx)`, and optional `on_enter` / `on_exit`.  
  Implemented scenes: **GameplayScene**, **PauseScene**, **HighScoreScene**, **NameInputScene**.

- **SceneStack** (`scenes/base.py`) keeps a stack of scenes with `push(scene)`, `pop()`, `current()`, and `clear()`. The main loop uses it when `game_state.current_screen` is one of PLAYING, ENDURANCE, PAUSED, HIGH_SCORES, NAME_INPUT: it syncs the stack to that state, then forwards input and render to `scene_stack.current()`.  
  Transitions (e.g. pause/resume, death → name input → high scores) are expressed via `handle_input` return values (`screen`, `quit`, `restart`, etc.); the loop updates both `current_screen` and the stack (push/pop/clear) so the stack stays the source of truth for the active overlay.

- **Flows:** gameplay ⇄ pause (push Pause / pop); gameplay → death → name input → high scores (push/pop by sync and transitions); “play again” clears the stack and pushes a new GameplayScene.
