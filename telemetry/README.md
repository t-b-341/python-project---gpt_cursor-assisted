# Telemetry

Structured logging of game events to SQLite for tuning and analysis.

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
