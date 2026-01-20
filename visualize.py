# visualize.py
# - Saves plots as PNGs into telemetry_plots/
# - Shows a SINGLE popup window that pages through plots (n/p or arrows)
# - Press 'q' (or Esc) to close the window and end the program

import os
import sys
import sqlite3
from dataclasses import dataclass
from typing import Callable, Optional, List, Tuple

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


DB_PATH = "game_telemetry.db"
OUT_DIR = "telemetry_plots"
SHOW_POPUP = True  # keep saving PNGs either way


# ----------------------------
# Helpers
# ----------------------------
def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;",
        (name,),
    ).fetchone()
    return row is not None


def get_table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    if not table_exists(conn, table):
        return set()
    rows = conn.execute(f"PRAGMA table_info({table});").fetchall()
    # PRAGMA table_info: (cid, name, type, notnull, dflt_value, pk)
    return {r[1] for r in rows}


def get_latest_run_id(conn: sqlite3.Connection) -> Optional[int]:
    if table_exists(conn, "runs"):
        row = conn.execute("SELECT MAX(id) FROM runs;").fetchone()
        if row and row[0] is not None:
            return int(row[0])

    for t in ("player_positions", "shots", "enemy_spawns", "enemy_hits", "player_damage", "player_deaths"):
        if table_exists(conn, t):
            row = conn.execute(f"SELECT MAX(run_id) FROM {t};").fetchone()
            if row and row[0] is not None:
                return int(row[0])

    return None


def read_df(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn, params=params)


def safe_numeric(series: pd.Series, fill=0.0) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(fill)


def no_data(ax: plt.Axes, msg: str = "No data") -> None:
    ax.text(0.5, 0.5, msg, ha="center", va="center", transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])


# ----------------------------
# Plot pages
# ----------------------------
@dataclass
class Page:
    title: str
    filename: str
    draw: Callable[[plt.Axes, sqlite3.Connection, int], bool]
    # draw() returns True if it drew a plot, False if no data / not available


def draw_movement_path(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "player_positions"):
        no_data(ax, "player_positions table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT t, x, y
        FROM player_positions
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No player_positions for this run")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)
    df["t"] = safe_numeric(df["t"], fill=0.0)

    # Enhanced: color by time progression
    scatter = ax.scatter(df["x"], df["y"], c=df["t"], cmap="plasma", s=5, alpha=0.6, edgecolors="none")
    ax.plot(df["x"], df["y"], "k-", alpha=0.2, linewidth=0.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="datalim")
    plt.colorbar(scatter, ax=ax, label="Time (s)")
    return True


def draw_movement_heatmap(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "player_positions"):
        no_data(ax, "player_positions table missing")
        return False

    # Sample for large datasets to improve performance
    df = read_df(
        conn,
        """
        SELECT x, y
        FROM player_positions
        WHERE run_id = ? AND (id % 5 = 0 OR 1=1)
        LIMIT 50000;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No player_positions for this run")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)

    # Use adaptive binning based on data range
    bins = min(50, max(20, int((df["x"].max() - df["x"].min()) / 10)))
    ax.hist2d(df["x"], df["y"], bins=bins, cmap="hot")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="datalim")
    return True


def draw_shots_scatter(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "shots"):
        no_data(ax, "shots table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT target_x, target_y, t
        FROM shots
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No shots for this run")
        return False

    df["target_x"] = safe_numeric(df["target_x"], fill=0.0)
    df["target_y"] = safe_numeric(df["target_y"], fill=0.0)
    df["t"] = safe_numeric(df["t"], fill=0.0)

    # Enhanced: color by time, use hexbin for density
    scatter = ax.scatter(df["target_x"], df["target_y"], c=df["t"], cmap="coolwarm", s=10, alpha=0.5, edgecolors="none")
    ax.set_xlabel("Target X")
    ax.set_ylabel("Target Y")
    ax.set_aspect("equal", adjustable="datalim")
    plt.colorbar(scatter, ax=ax, label="Time (s)")
    return True


def draw_damage_taken_timeline(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "player_damage"):
        no_data(ax, "player_damage table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT t, amount
        FROM player_damage
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No player_damage for this run")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["amount"] = safe_numeric(df["amount"], fill=0.0)
    df["cum_damage"] = df["amount"].cumsum()

    # Enhanced: area chart instead of line
    ax.fill_between(df["t"], df["cum_damage"], alpha=0.6, color="red")
    ax.plot(df["t"], df["cum_damage"], linewidth=2, color="darkred")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Cumulative Damage")
    ax.grid(True, alpha=0.3)
    return True


def draw_damage_taken_by_enemy(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "player_damage"):
        no_data(ax, "player_damage table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT COALESCE(source_enemy_type, 'unknown') AS enemy_type,
               SUM(amount) AS total_damage
        FROM player_damage
        WHERE run_id = ?
        GROUP BY COALESCE(source_enemy_type, 'unknown')
        ORDER BY total_damage DESC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No player_damage for this run")
        return False

    df["total_damage"] = safe_numeric(df["total_damage"], fill=0.0)

    # Enhanced: horizontal bar chart with gradient colors
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(df)))
    bars = ax.barh(df["enemy_type"], df["total_damage"], color=colors)
    ax.set_xlabel("Total Damage")
    ax.set_ylabel("Enemy Type")
    ax.grid(True, alpha=0.3, axis="x")
    return True


def draw_damage_dealt_by_enemy(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "enemy_hits"):
        no_data(ax, "enemy_hits table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT enemy_type,
               SUM(damage) AS total_damage
        FROM enemy_hits
        WHERE run_id = ?
        GROUP BY enemy_type
        ORDER BY total_damage DESC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No enemy_hits for this run")
        return False

    df["total_damage"] = safe_numeric(df["total_damage"], fill=0.0)

    ax.bar(df["enemy_type"], df["total_damage"])
    ax.set_xlabel("enemy_type")
    ax.set_ylabel("total damage")
    ax.tick_params(axis="x", rotation=30)
    return True


def draw_death_locations(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "player_deaths"):
        no_data(ax, "player_deaths table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT player_x AS x, player_y AS y
        FROM player_deaths
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No deaths logged for this run")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)

    ax.scatter(df["x"], df["y"], s=18)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="datalim")
    return True


def draw_accuracy_over_runs(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "runs"):
        no_data(ax, "runs table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT id AS run_id, shots_fired, hits
        FROM runs
        ORDER BY id ASC;
        """,
    )
    if df.empty:
        no_data(ax, "No runs")
        return False

    df["run_id"] = safe_numeric(df["run_id"], fill=0).astype(int)
    df["shots_fired"] = safe_numeric(df["shots_fired"], fill=0).astype(int)
    df["hits"] = safe_numeric(df["hits"], fill=0).astype(int)

    # Avoid pd.NAType: use NaN float then fill with 0.0
    denom = df["shots_fired"].replace(0, float("nan"))
    acc = (df["hits"] / denom) * 100.0
    df["accuracy_pct"] = safe_numeric(acc, fill=0.0)

    ax.plot(df["run_id"], df["accuracy_pct"])
    ax.set_xlabel("run_id")
    ax.set_ylabel("accuracy (%)")
    ax.set_ylim(0, 100)
    return True


def draw_wave_progression(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Wave progression timeline with start/end markers."""
    if not table_exists(conn, "waves"):
        no_data(ax, "waves table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT t, wave_number, event_type, enemies_spawned, hp_scale, speed_scale
        FROM waves
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No wave data for this run")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["wave_number"] = safe_numeric(df["wave_number"], fill=0).astype(int)

    starts = df[df["event_type"] == "start"]
    ends = df[df["event_type"] == "end"]

    if not starts.empty:
        ax.scatter(starts["t"], starts["wave_number"], c="green", marker="^", s=100, label="Wave Start", zorder=3)
    if not ends.empty:
        ax.scatter(ends["t"], ends["wave_number"], c="red", marker="v", s=100, label="Wave End", zorder=3)
    
    # Draw lines connecting wave numbers
    if not starts.empty:
        ax.plot(starts["t"], starts["wave_number"], "b-", alpha=0.3, linewidth=2, label="Wave Progression")
    
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Wave Number")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return True


def draw_wave_difficulty_scaling(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """HP and speed scaling over waves."""
    if not table_exists(conn, "waves"):
        no_data(ax, "waves table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT wave_number, hp_scale, speed_scale
        FROM waves
        WHERE run_id = ? AND event_type = 'start'
        ORDER BY wave_number ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No wave start data")
        return False

    df["wave_number"] = safe_numeric(df["wave_number"], fill=0).astype(int)
    df["hp_scale"] = safe_numeric(df["hp_scale"], fill=1.0)
    df["speed_scale"] = safe_numeric(df["speed_scale"], fill=1.0)

    ax.plot(df["wave_number"], df["hp_scale"], "o-", label="HP Scale", linewidth=2, markersize=8)
    ax.plot(df["wave_number"], df["speed_scale"], "s-", label="Speed Scale", linewidth=2, markersize=8)
    ax.set_xlabel("Wave Number")
    ax.set_ylabel("Scale Factor")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return True


def draw_player_velocity_over_time(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Player speed over time."""
    if not table_exists(conn, "player_velocities"):
        no_data(ax, "player_velocities table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT t, speed
        FROM player_velocities
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No velocity data")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["speed"] = safe_numeric(df["speed"], fill=0.0)

    ax.plot(df["t"], df["speed"], linewidth=1.5, alpha=0.7)
    ax.fill_between(df["t"], df["speed"], alpha=0.3)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Speed (px/s)")
    ax.grid(True, alpha=0.3)
    return True


def draw_movement_path_with_velocity(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Movement path colored by velocity."""
    if not table_exists(conn, "player_velocities"):
        no_data(ax, "player_velocities table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT x, y, speed
        FROM player_velocities
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No velocity data")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)
    df["speed"] = safe_numeric(df["speed"], fill=0.0)

    scatter = ax.scatter(df["x"], df["y"], c=df["speed"], cmap="viridis", s=10, alpha=0.6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="datalim")
    plt.colorbar(scatter, ax=ax, label="Speed (px/s)")
    return True


def draw_bullet_shape_distribution(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Pie chart of bullet shapes used."""
    if not table_exists(conn, "bullet_metadata"):
        no_data(ax, "bullet_metadata table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT shape, COUNT(*) AS count
        FROM bullet_metadata
        WHERE run_id = ?
        GROUP BY shape
        ORDER BY count DESC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No bullet metadata")
        return False

    df["count"] = safe_numeric(df["count"], fill=0).astype(int)

    ax.pie(df["count"], labels=df["shape"], autopct="%1.1f%%", startangle=90)
    ax.set_title("Bullet Shape Distribution")
    return True


def draw_bullet_color_usage(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Bar chart showing bullet color frequency."""
    if not table_exists(conn, "bullet_metadata"):
        no_data(ax, "bullet_metadata table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT color_r, color_g, color_b, COUNT(*) AS count
        FROM bullet_metadata
        WHERE run_id = ?
        GROUP BY color_r, color_g, color_b
        ORDER BY count DESC
        LIMIT 10;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No bullet metadata")
        return False

    df["count"] = safe_numeric(df["count"], fill=0).astype(int)
    df["color_label"] = df.apply(lambda row: f"RGB({row['color_r']},{row['color_g']},{row['color_b']})", axis=1)

    colors = [tuple(row[["color_r", "color_g", "color_b"]].astype(int) / 255.0) for _, row in df.iterrows()]
    bars = ax.barh(df["color_label"], df["count"], color=colors)
    ax.set_xlabel("Usage Count")
    ax.set_ylabel("Color (RGB)")
    return True


def draw_enemy_movement_paths(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Enemy movement paths colored by type."""
    if not table_exists(conn, "enemy_positions"):
        no_data(ax, "enemy_positions table missing")
        return False

    # Sample data for performance (every 5th point) to improve rendering speed
    df = read_df(
        conn,
        """
        SELECT enemy_type, x, y, t
        FROM (
            SELECT enemy_type, x, y, t,
                   ROW_NUMBER() OVER (PARTITION BY enemy_type ORDER BY t) AS rn
            FROM enemy_positions
            WHERE run_id = ?
        ) sampled
        WHERE rn % 5 = 0 OR rn = 1
        ORDER BY enemy_type, t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No enemy position data")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)

    # Limit to top 10 enemy types by frequency for readability
    top_types = df["enemy_type"].value_counts().head(10).index
    df_filtered = df[df["enemy_type"].isin(top_types)]

    for enemy_type in top_types:
        type_df = df_filtered[df_filtered["enemy_type"] == enemy_type]
        if not type_df.empty:
            ax.plot(type_df["x"], type_df["y"], alpha=0.4, linewidth=1, label=enemy_type)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    return True


def draw_enemy_density_heatmap(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Heatmap of where enemies spend time."""
    if not table_exists(conn, "enemy_positions"):
        no_data(ax, "enemy_positions table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT x, y
        FROM enemy_positions
        WHERE run_id = ?;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No enemy position data")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)

    hb = ax.hexbin(df["x"], df["y"], gridsize=30, cmap="Reds")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="datalim")
    plt.colorbar(hb, ax=ax, label="Density")
    return True


def draw_damage_heatmap_by_wave(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Heatmap of damage locations, colored by wave."""
    if not table_exists(conn, "player_damage") or not table_exists(conn, "waves"):
        no_data(ax, "Required tables missing")
        return False

    df = read_df(
        conn,
        """
        SELECT pd.player_x AS x, pd.player_y AS y, pd.t,
               (SELECT MAX(wave_number) FROM waves w 
                WHERE w.run_id = pd.run_id AND w.t <= pd.t AND w.event_type = 'start') AS wave
        FROM player_damage pd
        WHERE pd.run_id = ?;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No damage data")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)
    df["wave"] = safe_numeric(df["wave"], fill=1).astype(int)

    scatter = ax.scatter(df["x"], df["y"], c=df["wave"], cmap="hot", s=20, alpha=0.6)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="datalim")
    plt.colorbar(scatter, ax=ax, label="Wave Number")
    return True


def draw_survival_time_per_wave(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Bar chart showing survival time per wave."""
    if not table_exists(conn, "waves"):
        no_data(ax, "waves table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT wave_number, 
               MIN(CASE WHEN event_type = 'start' THEN t END) AS start_t,
               MIN(CASE WHEN event_type = 'end' THEN t END) AS end_t
        FROM waves
        WHERE run_id = ?
        GROUP BY wave_number
        ORDER BY wave_number ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No wave data")
        return False

    df["wave_number"] = safe_numeric(df["wave_number"], fill=0).astype(int)
    df["start_t"] = safe_numeric(df["start_t"], fill=0.0)
    df["end_t"] = safe_numeric(df["end_t"], fill=0.0)
    df["duration"] = df["end_t"] - df["start_t"]
    df["duration"] = df["duration"].fillna(0.0)

    ax.bar(df["wave_number"], df["duration"], alpha=0.7)
    ax.set_xlabel("Wave Number")
    ax.set_ylabel("Survival Time (s)")
    ax.grid(True, alpha=0.3, axis="y")
    return True


def draw_score_progression(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Score progression over time."""
    if not table_exists(conn, "score_events"):
        no_data(ax, "score_events table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT t, score, score_change, source
        FROM score_events
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No score data")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["score"] = safe_numeric(df["score"], fill=0).astype(int)

    ax.plot(df["t"], df["score"], linewidth=2, label="Total Score")
    ax.fill_between(df["t"], df["score"], alpha=0.3)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Score")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return True


def draw_score_by_source(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Breakdown of score by source."""
    if not table_exists(conn, "score_events"):
        no_data(ax, "score_events table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT source, SUM(score_change) AS total_score
        FROM score_events
        WHERE run_id = ? AND score_change > 0
        GROUP BY source
        ORDER BY total_score DESC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No score data")
        return False

    df["total_score"] = safe_numeric(df["total_score"], fill=0).astype(int)
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(df)))
    ax.barh(df["source"], df["total_score"], color=colors)
    ax.set_xlabel("Total Score")
    ax.set_ylabel("Source")
    ax.grid(True, alpha=0.3, axis="x")
    return True


def draw_level_progression(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Level progression over time."""
    if not table_exists(conn, "level_events"):
        no_data(ax, "level_events table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT t, level, level_name
        FROM level_events
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No level data")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["level"] = safe_numeric(df["level"], fill=1).astype(int)

    ax.step(df["t"], df["level"], where="post", linewidth=2, marker="o", markersize=6)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Level")
    ax.grid(True, alpha=0.3)
    return True


def draw_boss_encounters(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Boss HP over time during encounters."""
    if not table_exists(conn, "boss_events"):
        no_data(ax, "boss_events table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT t, wave_number, phase, hp, max_hp, event_type
        FROM boss_events
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No boss data")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["hp"] = safe_numeric(df["hp"], fill=0).astype(int)
    df["max_hp"] = safe_numeric(df["max_hp"], fill=1).astype(int)
    df["hp_pct"] = (df["hp"] / df["max_hp"]) * 100.0

    # Plot HP percentage over time
    ax.plot(df["t"], df["hp_pct"], linewidth=2, label="Boss HP %")
    ax.fill_between(df["t"], df["hp_pct"], alpha=0.3)
    
    # Mark phase transitions
    phase_changes = df[df["event_type"] == "phase_transition"]
    if not phase_changes.empty:
        ax.scatter(phase_changes["t"], phase_changes["hp_pct"], c="red", s=100, 
                   marker="X", zorder=5, label="Phase Change")
    
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("HP %")
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.legend()
    return True


def draw_weapon_usage(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Time spent using each weapon."""
    if not table_exists(conn, "weapon_switches"):
        no_data(ax, "weapon_switches table missing")
        return False

    # Get run end time for last weapon duration calculation
    run_end = read_df(
        conn,
        """
        SELECT seconds_survived FROM runs WHERE id = ?;
        """,
        (run_id,),
    )
    run_end_time = run_end["seconds_survived"].iloc[0] if not run_end.empty and not run_end["seconds_survived"].isna().all() else None

    df = read_df(
        conn,
        """
        SELECT t, weapon_mode,
               LEAD(t) OVER (ORDER BY t) - t AS duration
        FROM weapon_switches
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No weapon switch data")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["duration"] = safe_numeric(df["duration"], fill=0.0)
    
    # For last weapon, estimate duration to run end
    if run_end_time is not None:
        last_t = df["t"].iloc[-1] if not df.empty else 0.0
        df.loc[df.index[-1], "duration"] = max(0.0, run_end_time - last_t)
    else:
        df["duration"] = df["duration"].fillna(0.0)

    weapon_times = df.groupby("weapon_mode")["duration"].sum().sort_values(ascending=False)
    
    if weapon_times.empty or weapon_times.sum() == 0:
        no_data(ax, "No weapon usage data")
        return False
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(weapon_times)))
    ax.pie(weapon_times.values, labels=weapon_times.index, autopct="%1.1f%%", 
           colors=colors, startangle=90)
    ax.set_title("Weapon Usage Time")
    return True


def draw_pickup_collection(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Pickup collection statistics."""
    if not table_exists(conn, "pickup_events"):
        no_data(ax, "pickup_events table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT pickup_type, 
               SUM(CASE WHEN collected = 1 THEN 1 ELSE 0 END) AS collected_count,
               COUNT(*) AS total_count
        FROM pickup_events
        WHERE run_id = ?
        GROUP BY pickup_type
        ORDER BY collected_count DESC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No pickup data")
        return False

    df["collected_count"] = safe_numeric(df["collected_count"], fill=0).astype(int)
    df["total_count"] = safe_numeric(df["total_count"], fill=0).astype(int)
    df["collection_rate"] = (df["collected_count"] / df["total_count"]) * 100.0

    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.7, len(df)))
    bars = ax.barh(df["pickup_type"], df["collected_count"], color=colors)
    ax.set_xlabel("Collected Count")
    ax.set_ylabel("Pickup Type")
    ax.grid(True, alpha=0.3, axis="x")
    
    # Add collection rate as text
    for i, (idx, row) in enumerate(df.iterrows()):
        ax.text(row["collected_count"], i, f" {row['collection_rate']:.0f}%", 
                va="center", fontsize=9)
    return True


def draw_overshield_usage(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Overshield changes over time."""
    if not table_exists(conn, "overshield_events"):
        no_data(ax, "overshield_events table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT t, overshield, max_overshield, change
        FROM overshield_events
        WHERE run_id = ?
        ORDER BY t ASC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No overshield data")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["overshield"] = safe_numeric(df["overshield"], fill=0).astype(int)
    df["max_overshield"] = safe_numeric(df["max_overshield"], fill=1).astype(int)

    ax.plot(df["t"], df["overshield"], linewidth=2, label="Overshield", color="cyan")
    ax.fill_between(df["t"], df["overshield"], alpha=0.3, color="cyan")
    ax.axhline(y=df["max_overshield"].iloc[0] if not df.empty else 0, 
               color="red", linestyle="--", alpha=0.5, label="Max Overshield")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Overshield")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return True


def draw_player_action_frequency(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Frequency of player actions using GROUP BY."""
    if not table_exists(conn, "player_actions"):
        no_data(ax, "player_actions table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT action_type, COUNT(*) AS count
        FROM player_actions
        WHERE run_id = ?
        GROUP BY action_type
        ORDER BY count DESC;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No action data")
        return False

    df["count"] = safe_numeric(df["count"], fill=0).astype(int)
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(df)))
    ax.bar(df["action_type"], df["count"], color=colors)
    ax.set_xlabel("Action Type")
    ax.set_ylabel("Frequency")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3, axis="y")
    return True


def draw_weapon_effectiveness_comparison(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Compare weapons using JOINs across multiple tables."""
    if not table_exists(conn, "weapon_switches") or not table_exists(conn, "enemy_hits"):
        no_data(ax, "Required tables missing")
        return False

    df = read_df(
        conn,
        """
        WITH weapon_periods AS (
            SELECT 
                w.weapon_mode,
                w.t AS start_time,
                COALESCE(
                    (SELECT MIN(t) FROM weapon_switches w2 
                     WHERE w2.run_id = w.run_id AND w2.t > w.t),
                    (SELECT seconds_survived FROM runs WHERE id = w.run_id)
                ) AS end_time
            FROM weapon_switches w
            WHERE w.run_id = ?
        )
        SELECT 
            wp.weapon_mode,
            COUNT(DISTINCT s.id) AS shots_fired,
            COUNT(DISTINCT eh.id) AS hits,
            COALESCE(SUM(eh.damage), 0) AS total_damage,
            COUNT(DISTINCT CASE WHEN eh.killed = 1 THEN eh.id END) AS kills
        FROM weapon_periods wp
        LEFT JOIN shots s ON s.run_id = ? 
            AND s.t BETWEEN wp.start_time AND wp.end_time
        LEFT JOIN enemy_hits eh ON eh.run_id = ?
            AND eh.t BETWEEN wp.start_time AND wp.end_time
        GROUP BY wp.weapon_mode
        ORDER BY total_damage DESC;
        """,
        (run_id, run_id, run_id),
    )
    if df.empty:
        no_data(ax, "No weapon data")
        return False

    df["shots_fired"] = safe_numeric(df["shots_fired"], fill=0).astype(int)
    df["hits"] = safe_numeric(df["hits"], fill=0).astype(int)
    df["total_damage"] = safe_numeric(df["total_damage"], fill=0).astype(int)
    df["kills"] = safe_numeric(df["kills"], fill=0).astype(int)
    df["accuracy"] = (df["hits"] / df["shots_fired"].replace(0, float("nan"))) * 100.0
    df["accuracy"] = df["accuracy"].fillna(0.0)

    x = np.arange(len(df))
    width = 0.35
    ax.bar(x - width/2, df["total_damage"], width, label="Damage", alpha=0.8)
    ax.bar(x + width/2, df["kills"] * 50, width, label="Kills (×50)", alpha=0.8)
    ax.set_xlabel("Weapon")
    ax.set_ylabel("Value")
    ax.set_xticks(x)
    ax.set_xticklabels(df["weapon_mode"], rotation=45, ha="right")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    return True


def draw_action_patterns_with_cte(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Use CTEs to analyze action sequences."""
    if not table_exists(conn, "player_actions"):
        no_data(ax, "player_actions table missing")
        return False

    df = read_df(
        conn,
        """
        WITH action_sequences AS (
            SELECT 
                action_type,
                t,
                LAG(action_type) OVER (ORDER BY t) AS prev_action,
                LEAD(action_type) OVER (ORDER BY t) AS next_action,
                t - LAG(t) OVER (ORDER BY t) AS time_since_prev
            FROM player_actions
            WHERE run_id = ?
        ),
        action_transitions AS (
            SELECT 
                prev_action || ' -> ' || action_type AS transition,
                COUNT(*) AS frequency,
                AVG(time_since_prev) AS avg_time
            FROM action_sequences
            WHERE prev_action IS NOT NULL
            GROUP BY transition
        )
        SELECT * FROM action_transitions
        ORDER BY frequency DESC
        LIMIT 10;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No action pattern data")
        return False

    df["frequency"] = safe_numeric(df["frequency"], fill=0).astype(int)
    df["avg_time"] = safe_numeric(df["avg_time"], fill=0.0)

    colors = plt.cm.plasma(np.linspace(0.2, 0.8, len(df)))
    bars = ax.barh(df["transition"], df["frequency"], color=colors)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Action Transition")
    ax.grid(True, alpha=0.3, axis="x")
    
    # Add average time annotations
    for i, (idx, row) in enumerate(df.iterrows()):
        ax.text(row["frequency"], i, f"  {row['avg_time']:.2f}s avg", 
                va="center", fontsize=8)
    return True


def draw_running_statistics(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Show running totals using window functions."""
    if not table_exists(conn, "score_events"):
        no_data(ax, "score_events table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT 
            t,
            score,
            score_change,
            SUM(score_change) OVER (ORDER BY t) AS running_score,
            AVG(score_change) OVER (
                ORDER BY t 
                ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
            ) AS moving_avg_10,
            COUNT(*) OVER (ORDER BY t) AS event_count
        FROM score_events
        WHERE run_id = ?
        ORDER BY t;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No score data")
        return False

    df["t"] = safe_numeric(df["t"], fill=0.0)
    df["running_score"] = safe_numeric(df["running_score"], fill=0).astype(int)
    df["moving_avg_10"] = safe_numeric(df["moving_avg_10"], fill=0.0)

    ax.plot(df["t"], df["running_score"], linewidth=2, label="Running Score", color="blue")
    ax.plot(df["t"], df["moving_avg_10"] * 10, linewidth=1.5, label="Moving Avg (×10)", 
            color="orange", alpha=0.7)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Score")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return True


def draw_zone_effectiveness(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Compare zones using correlated subqueries."""
    if not table_exists(conn, "player_zone_visits"):
        no_data(ax, "player_zone_visits table missing")
        return False

    df = read_df(
        conn,
        """
        SELECT 
            zone_name,
            zone_type,
            COUNT(CASE WHEN event_type = 'enter' THEN 1 END) AS visit_count,
            (SELECT COUNT(*) 
             FROM player_actions pa 
             WHERE pa.run_id = ? 
             AND pa.action_type = 'boost'
             AND EXISTS (
                 SELECT 1 FROM player_zone_visits pzv2
                 WHERE pzv2.run_id = ?
                 AND pzv2.zone_name = pzv.zone_name
                 AND pzv2.event_type = 'enter'
                 AND ABS(pa.t - pzv2.t) < 1.0
             )
            ) AS boost_actions_in_zone
        FROM player_zone_visits pzv
        WHERE pzv.run_id = ?
        GROUP BY zone_name, zone_type
        ORDER BY visit_count DESC;
        """,
        (run_id, run_id, run_id),
    )
    if df.empty:
        no_data(ax, "No zone data")
        return False

    df["visit_count"] = safe_numeric(df["visit_count"], fill=0).astype(int)
    df["boost_actions_in_zone"] = safe_numeric(df["boost_actions_in_zone"], fill=0).astype(int)

    x = np.arange(len(df))
    width = 0.35
    ax.bar(x - width/2, df["visit_count"], width, label="Visits", alpha=0.8)
    ax.bar(x + width/2, df["boost_actions_in_zone"], width, label="Boost Actions", alpha=0.8)
    ax.set_xlabel("Zone")
    ax.set_ylabel("Count")
    ax.set_xticks(x)
    ax.set_xticklabels(df["zone_name"], rotation=45, ha="right")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    return True


def draw_performance_summary_view(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """Use the player_performance_summary view."""
    if not table_exists(conn, "runs"):
        no_data(ax, "runs table missing")
        return False

    # Check if view exists
    view_exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='view' AND name='player_performance_summary'"
    ).fetchone()
    
    if not view_exists:
        no_data(ax, "View not available")
        return False

    df = read_df(
        conn,
        """
        SELECT 
            accuracy_pct,
            kills_per_second,
            dps,
            difficulty,
            max_level
        FROM player_performance_summary
        WHERE run_id = ?;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No performance data")
        return False

    metrics = ["Accuracy %", "Kills/sec", "DPS"]
    values = [
        df["accuracy_pct"].iloc[0] if not df.empty else 0.0,
        df["kills_per_second"].iloc[0] if not df.empty else 0.0,
        df["dps"].iloc[0] if not df.empty else 0.0,
    ]

    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.7, len(metrics)))
    bars = ax.barh(metrics, values, color=colors)
    ax.set_xlabel("Value")
    ax.set_title(f"Performance Summary (Level {df['max_level'].iloc[0] if not df.empty else '?'}, {df['difficulty'].iloc[0] if not df.empty else '?'})")
    ax.grid(True, alpha=0.3, axis="x")
    
    # Add value labels
    for i, (metric, val) in enumerate(zip(metrics, values)):
        ax.text(val, i, f"  {val:.2f}", va="center", fontsize=10, fontweight="bold")
    return True


def draw_damage_totals_over_runs(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """
    If runs.damage_dealt exists -> use it.
    Else -> compute damage_dealt from enemy_hits (if exists).
    """
    if not table_exists(conn, "runs"):
        no_data(ax, "runs table missing")
        return False

    runs_cols = get_table_columns(conn, "runs")
    has_damage_dealt = "damage_dealt" in runs_cols

    if has_damage_dealt:
        df = read_df(
            conn,
            """
            SELECT id AS run_id, damage_taken, damage_dealt
            FROM runs
            ORDER BY id ASC;
            """,
        )
        if df.empty:
            no_data(ax, "No runs")
            return False

        df["run_id"] = safe_numeric(df["run_id"], fill=0).astype(int)
        df["damage_taken"] = safe_numeric(df["damage_taken"], fill=0.0)
        df["damage_dealt"] = safe_numeric(df["damage_dealt"], fill=0.0)

        ax.plot(df["run_id"], df["damage_dealt"], label="damage_dealt")
        ax.plot(df["run_id"], df["damage_taken"], label="damage_taken")
        ax.set_xlabel("run_id")
        ax.set_ylabel("damage")
        ax.legend()
        return True

    # Fallback: compute damage_dealt per run from enemy_hits
    if not table_exists(conn, "enemy_hits"):
        no_data(ax, "runs.damage_dealt missing AND enemy_hits missing")
        return False

    df = read_df(
        conn,
        """
        SELECT r.id AS run_id,
               r.damage_taken AS damage_taken,
               COALESCE(h.damage_dealt, 0) AS damage_dealt
        FROM runs r
        LEFT JOIN (
            SELECT run_id, SUM(damage) AS damage_dealt
            FROM enemy_hits
            GROUP BY run_id
        ) h ON h.run_id = r.id
        ORDER BY r.id ASC;
        """,
    )
    if df.empty:
        no_data(ax, "No runs")
        return False

    df["run_id"] = safe_numeric(df["run_id"], fill=0).astype(int)
    df["damage_taken"] = safe_numeric(df["damage_taken"], fill=0.0)
    df["damage_dealt"] = safe_numeric(df["damage_dealt"], fill=0.0)

    ax.plot(df["run_id"], df["damage_dealt"], label="damage_dealt (computed)")
    ax.plot(df["run_id"], df["damage_taken"], label="damage_taken")
    ax.set_xlabel("run_id")
    ax.set_ylabel("damage")
    ax.legend()
    return True


# ----------------------------
# Single popup viewer (one window)
# ----------------------------
def run_single_popup(conn: sqlite3.Connection, run_id: int, pages: List[Page]) -> None:
    # Only keep pages that can draw something (quick probe)
    available: List[Page] = []
    for p in pages:
        fig_probe, ax_probe = plt.subplots()
        ok = False
        try:
            ax_probe.clear()
            ok = p.draw(ax_probe, conn, run_id)
        except Exception:
            ok = False
        plt.close(fig_probe)
        if ok:
            available.append(p)

    if not available:
        print("No plots available to show in popup.")
        return

    idx = 0
    quit_program = {"flag": False}

    fig, ax = plt.subplots()
    try:
        fig.canvas.manager.set_window_title("Telemetry Viewer (single window)")
    except Exception:
        pass

    def render():
        ax.clear()
        page = available[idx]
        ok = False
        try:
            ok = page.draw(ax, conn, run_id)
        except Exception as e:
            no_data(ax, f"Error: {e!r}")
            ok = False

        # Title shows index / count
        ax.set_title(f"[{idx+1}/{len(available)}] {available[idx].title} (run_id={run_id})")

        # Small footer hint
        fig.text(
            0.5, 0.01,
            "n/→ next   p/← prev   q/Esc quit",
            ha="center", va="bottom", fontsize=9
        )

        fig.tight_layout()
        fig.canvas.draw_idle()

    def on_key(event):
        if event.key in ("n", "right"):
            nonlocal_idx = (idx + 1) % len(available)
            # assign via outer scope trick:
            set_index(nonlocal_idx)
        elif event.key in ("p", "left"):
            nonlocal_idx = (idx - 1) % len(available)
            set_index(nonlocal_idx)
        elif event.key in ("q", "escape"):
            quit_program["flag"] = True
            plt.close(fig)

    def set_index(new_idx: int):
        nonlocal idx
        idx = new_idx
        # remove old footer text before redrawing it
        fig.texts.clear()
        render()

    fig.canvas.mpl_connect("key_press_event", on_key)
    render()

    plt.show()  # blocks until window closes

    if quit_program["flag"]:
        # End the program immediately as requested
        sys.exit(0)


# ----------------------------
# PNG generation
# ----------------------------
def save_pngs(conn: sqlite3.Connection, run_id: int, pages: List[Page]) -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    for p in pages:
        fig, ax = plt.subplots()
        try:
            ax.clear()
            ok = p.draw(ax, conn, run_id)
        except Exception as e:
            print(f"Error building plot {p.filename}: {e!r}")
            ok = False

        if not ok:
            plt.close(fig)
            print(f"Skipping (no data): {p.filename}")
            continue

        ax.set_title(f"{p.title} (run_id={run_id})")
        fig.tight_layout()
        out_path = os.path.join(OUT_DIR, f"run_{run_id}__{p.filename}")
        fig.savefig(out_path, dpi=160)
        plt.close(fig)
        print(f"Wrote: {out_path}")


# ----------------------------
# Main
# ----------------------------
def main():
    pages: List[Page] = [
        Page("Movement path", "movement_path.png", draw_movement_path),
        Page("Movement heatmap", "movement_heatmap.png", draw_movement_heatmap),
        Page("Movement path with velocity", "movement_path_velocity.png", draw_movement_path_with_velocity),
        Page("Player velocity over time", "player_velocity.png", draw_player_velocity_over_time),
        Page("Shots scatter", "shots_scatter.png", draw_shots_scatter),
        Page("Damage taken timeline", "damage_taken_timeline.png", draw_damage_taken_timeline),
        Page("Damage taken by enemy type", "damage_taken_by_enemy.png", draw_damage_taken_by_enemy),
        Page("Damage dealt by enemy type", "damage_dealt_by_enemy.png", draw_damage_dealt_by_enemy),
        Page("Damage heatmap by wave", "damage_heatmap_wave.png", draw_damage_heatmap_by_wave),
        Page("Death locations", "death_locations.png", draw_death_locations),
        Page("Wave progression", "wave_progression.png", draw_wave_progression),
        Page("Wave difficulty scaling", "wave_difficulty.png", draw_wave_difficulty_scaling),
        Page("Survival time per wave", "survival_per_wave.png", draw_survival_time_per_wave),
        Page("Enemy movement paths", "enemy_movement.png", draw_enemy_movement_paths),
        Page("Enemy density heatmap", "enemy_density.png", draw_enemy_density_heatmap),
        Page("Bullet shape distribution", "bullet_shapes.png", draw_bullet_shape_distribution),
        Page("Bullet color usage", "bullet_colors.png", draw_bullet_color_usage),
        Page("Score progression", "score_progression.png", draw_score_progression),
        Page("Score by source", "score_by_source.png", draw_score_by_source),
        Page("Level progression", "level_progression.png", draw_level_progression),
        Page("Boss encounters", "boss_encounters.png", draw_boss_encounters),
        Page("Weapon usage", "weapon_usage.png", draw_weapon_usage),
        Page("Pickup collection", "pickup_collection.png", draw_pickup_collection),
        Page("Overshield usage", "overshield_usage.png", draw_overshield_usage),
        Page("Player action frequency", "player_actions.png", draw_player_action_frequency),
        Page("Weapon effectiveness comparison", "weapon_effectiveness.png", draw_weapon_effectiveness_comparison),
        Page("Action patterns (CTE)", "action_patterns.png", draw_action_patterns_with_cte),
        Page("Running statistics", "running_stats.png", draw_running_statistics),
        Page("Zone effectiveness", "zone_effectiveness.png", draw_zone_effectiveness),
        Page("Performance summary (View)", "performance_summary.png", draw_performance_summary_view),
        Page("Accuracy over runs", "accuracy_over_runs.png", draw_accuracy_over_runs),
        Page("Damage totals over runs", "damage_totals_over_runs.png", draw_damage_totals_over_runs),
    ]

    with sqlite3.connect(DB_PATH) as conn:
        run_id = get_latest_run_id(conn)
        if run_id is None:
            print("No runs found in the database.")
            return

        print(f"Using run_id={run_id}")

        # Always save PNGs
        save_pngs(conn, run_id, pages)

        # Then show single popup (optional)
        if SHOW_POPUP:
            print("\nSingle popup controls: n/right=next, p/left=prev, q/esc=quit")
            run_single_popup(conn, run_id, pages)


if __name__ == "__main__":
    main()
