"""Player-focused plots: movement, velocity, shots."""
from __future__ import annotations

import sqlite3

import matplotlib.pyplot as plt

from telemetry_viz.db_utils import no_data, read_df, safe_numeric, table_exists


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

    scatter = ax.scatter(df["target_x"], df["target_y"], c=df["t"], cmap="coolwarm", s=10, alpha=0.5, edgecolors="none")
    ax.set_xlabel("Target X")
    ax.set_ylabel("Target Y")
    ax.set_aspect("equal", adjustable="datalim")
    plt.colorbar(scatter, ax=ax, label="Time (s)")
    return True


def draw_player_velocity_over_time(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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
