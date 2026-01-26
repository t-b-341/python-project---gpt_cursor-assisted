# Developer guide

Setup, running the game, tests, profiling/telemetry, and a short architectural overview.

---

## Setup

### Prerequisites

- **Python 3.10+** (3.12 tested)
- **Pygame** — main runtime dependency

### Install dependencies

From the project root:

```bash
pip install -r requirements.txt
```

For development you need `pytest` (included in `requirements.txt`).

### Optional: C extension (faster collision/physics)

The game can use a C extension (`game_physics`) for better performance. Build it with:

```bash
python setup.py build_ext --inplace
```

See `comments/BUILD_INSTRUCTIONS.md` for compiler setup (e.g. Visual Studio Build Tools on Windows, `python3-dev` + `build-essential` on Linux).

### Optional: GPU physics (CUDA)

GPU-accelerated bullet physics is optional. If `gpu_physics` (CUDA) is available, enable it via **Options → use_gpu_physics** or the graphics preset in `config/game_config.py`. See `comments/CUDA_INSTALLATION_GUIDE.md` if you install CUDA.

---

## How to run the game

From the project root:

```bash
python game.py
```

This calls `main()` → `GameApp().run()`. The game window opens and the main loop runs until you quit.

---

## How to run tests

Tests live under `tests/` and use pytest. From the project root:

```bash
pytest
```

Or with more detail:

```bash
pytest -v
```

Configuration is in `pytest.ini` (test dir `tests/`, `test_*.py` files, verbose default). Pygame is initialized where needed via fixtures (e.g. in `tests/conftest.py`).

---

## Profiling and telemetry tools

### Profiling (cProfile)

Use the provided profiling script to profile the game for a short period (~10 seconds):

```bash
python profile_game.py
```

This runs the game under cProfile, then writes:

- `profiling_results.txt` — human-readable summary (top functions by cumulative time)
- `profiling_results.prof` — binary stats for tools like SnakeViz

View with SnakeViz (install separately):

```bash
pip install snakeviz
snakeviz profiling_results.prof
```

### Telemetry (SQLite)

The game can log structured events (runs, shots, damage, waves, etc.) to SQLite when telemetry is enabled in **Options**.

1. In-game: **Options → Telemetry → Enabled**, then play.
2. Events are written to `game_telemetry.db` in the working directory.

See `telemetry/README.md` for the schema and example queries. Helper SQL is in `telemetry/sql/` (e.g. `top_sessions.sql`, `weapon_accuracy.sql`):

```bash
sqlite3 game_telemetry.db ".read telemetry/sql/top_sessions.sql"
```

### Telemetry visualizer

To plot runs (e.g. death locations, difficulty over time):

```bash
python -m telemetry_viz.viewer
```

Or use the wrapper that can save PNGs and step through pages:

```bash
python visualize.py
```

Use the prompts and keys shown in the window (e.g. n/p or arrows to change pages, q or Esc to quit).

---

## Architectural overview

- **GameState** (`state.py`) — Mutable per-run state: player, enemies, bullets, score, wave, lives, level, pickups, timers, etc. Created when a run starts and passed through the loop and systems.
- **AppContext** (`context.py`) — App-level, long-lived resources and config: screen, fonts, clock, dimensions, `config` (`GameConfig`), telemetry client, controls. Built at startup and passed into the main loop and screens.
- **config/** — Central configuration: `game_config.py` (difficulty, options, feel, graphics presets), `enemy_defs.py`, `projectile_defs.py`, balance/tuning. `config_enemies.py` / `config_weapons.py` are shims over these. Systems read from `ctx.config` or level context.
- **systems/** — Per-frame simulation and UI: movement, collision, spawn, AI, input, audio, telemetry, UI (HUD/overlays). Registered in `systems/registry.py` and as `GAMEPLAY_SYSTEMS`; the gameplay screen runs them in a fixed order. `ui_system` draws HUD and overlays (health bars, score, damage numbers, wave banner, etc.).
- **scenes/** — Full-screen “scenes” (gameplay, pause, high scores, name input, title, options, shader test). Each has `state_id()`, `handle_input`, `update`, `render`; the scene stack in `scenes/base.py` drives transitions (e.g. pause push/pop, game over → name input → high scores).
- **screens/** — Lower-level draw logic used by the loop or scenes (e.g. `screens/gameplay` does the five-phase render: background, entities, projectiles, HUD, overlays).
- **rendering/** — Drawing utilities and context: `context.py` (RenderContext), `world.py` (background, terrain, entities, projectiles, effects, beams), `hud.py` (health bars, centered text, HUD text), `overlays.py` (e.g. debug overlay). Build `RenderContext` with `RenderContext.from_app_ctx(app_ctx)` and pass it into render calls.
- **shader_effects/** — CPU-side post-process effects (vignette, color grading, distortion, etc.). `base.py` has the base class, registry, and profile/stack helpers; `color_effects.py` and `distort_effects.py` hold the effect classes. Used by menus, pause, and gameplay when the corresponding config flags and profiles are set.
- **telemetry/** — Event types, SQLite writer/reader, schema. Used when `config.enable_telemetry` is true. `telemetry_viz` consumes the DB for plots.

Data flow in short: **AppContext** + **GameState** are passed through the main loop → scenes/screens and **systems** read/write **GameState** and draw via **rendering** and **shader_effects**; **config** and **telemetry** are used where needed.
