# Telemetry

Structured logging of game events to SQLite for tuning and analysis.

## Database schema (tables)

| Table | Description |
|-------|-------------|
| **runs** | One row per game session: score, survival time, shots/hits, damage, deaths, difficulty, max wave/level. |
| **enemy_spawns** | Each enemy spawn (run, time, type, position, size, HP). |
| **player_positions** | Sampled player (x, y) over time per run. |
| **shots** | Player shot events (origin, target, direction, optional shape/color). |
| **enemy_hits** | Hits on enemies (time, type, position, damage, HP after, killed flag). |
| **player_damage** | Damage taken by the player (amount, source, position, HP after). |
| **player_deaths** | Death events (position, lives left, wave). |
| **run_state_samples** | Periodic snapshots (player HP, enemies alive) per run. |
| **waves** | Wave start/end and spawn counts (wave_number, event_type, hp_scale, speed_scale). |
| **enemy_positions** | Sampled enemy positions and velocities. |
| **player_velocities** | Sampled player velocity. |
| **bullet_metadata** | Bullet type, shape, color, source (player/enemy). |
| **score_events** | Score changes (score, score_change, source). |
| **level_events** | Level transitions (level, level_name). |
| **boss_events** | Boss-wave events (wave, phase, HP, event_type). |
| **weapon_switches** | When the player switched weapon (weapon_mode). |
| **pickup_events** | Pickups (type, position, collected). |
| **overshield_events** | Overshield changes. |
| **zones** | Named zones (bounds). |
| **player_actions** | Actions (type, position, duration, success). |
| **player_zone_visits** | Zone enter/exit. |
| **friendly_ai_spawns** | Ally spawns. |
| **friendly_ai_positions** | Ally positions over time. |
| **friendly_ai_shots** | Ally shot events. |
| **friendly_ai_deaths** | Ally deaths (killed_by). |
| **wave_enemy_types** | Per-wave breakdown of enemy types and counts. |

The view **player_performance_summary** summarizes each run (accuracy_pct, kills_per_second, dps, etc.) from **runs**.

## Example SQL queries

Helper SQL files live in `telemetry/sql/`. Run them against your DB with sqlite3:

```bash
# From project root; DB is often in current directory or a path you set
sqlite3 game_telemetry.db ".read telemetry/sql/top_sessions.sql"
sqlite3 game_telemetry.db ".read telemetry/sql/weapon_accuracy.sql"
```

Or start an interactive session and run the files there:

```bash
sqlite3 game_telemetry.db
sqlite> .read telemetry/sql/top_sessions.sql
sqlite> .read telemetry/sql/weapon_accuracy.sql
```

- **top_sessions.sql** – Top N sessions by score or survival time.
- **weapon_accuracy.sql** – Shots and (where available) accuracy by weapon.

## Enabling telemetry

1. Start the game and go to **Options**.
2. In the **Telemetry** step, choose **Enabled**.
3. Start a run. Events are written to `game_telemetry.db` in the working directory.

Runs, shots, player position, damage, deaths, waves, and run-state samples (HP, enemy count over time) are logged when telemetry is enabled.

## Running the visualizer

From the project root:

```bash
python -m telemetry_viz.viewer
```

Or use `visualize.py` if it wraps this. The viewer loads `game_telemetry.db`, picks the latest run (or a chosen one), and shows plot pages. Use the indicated keys to move between pages and quit.

## Interpreting key plots

- **Death locations** – Scatter of (x, y) where the player died; axes are in-game pixels. Color by wave when `wave_number` is recorded.
- **Difficulty over time** – For one run: HP ratio and cumulative damage vs time; optional “enemies alive” on a second axis. Gray vertical lines mark wave start. Use this to see when pressure spikes.
- **Damage taken timeline** – Cumulative damage over time.
- **Wave progression / survival per wave** – How far you get each wave and level.

## Performance debugging

Set `GAME_DEBUG_PERF=1` in the environment to record frame times in memory (see `telemetry.perf`). Off by default; no effect when unset.

## Future: pressure score

A combined “pressure” metric (e.g. from enemy count, bullets near the player, recent damage) can be added later. If implemented, it would be logged in run-state samples or a dedicated table and plotted alongside difficulty-over-time.
