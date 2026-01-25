"""Wave progression and difficulty plots."""
from __future__ import annotations

import sqlite3

import matplotlib.pyplot as plt

from telemetry_viz.db_utils import no_data, read_df, safe_numeric, table_exists


def draw_wave_progression(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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

    if not starts.empty:
        ax.plot(starts["t"], starts["wave_number"], "b-", alpha=0.3, linewidth=2, label="Wave Progression")

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Wave Number")
    ax.legend()
    ax.grid(True, alpha=0.3)
    return True


def draw_wave_difficulty_scaling(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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


def draw_survival_time_per_wave(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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
