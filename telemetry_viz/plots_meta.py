"""Cross-run and performance summary plots."""
from __future__ import annotations

import sqlite3

import matplotlib.pyplot as plt
import numpy as np

from telemetry_viz.db_utils import get_table_columns, no_data, read_df, safe_numeric, table_exists


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

    denom = df["shots_fired"].replace(0, float("nan"))
    acc = (df["hits"] / denom) * 100.0
    df["accuracy_pct"] = safe_numeric(acc, fill=0.0)

    ax.plot(df["run_id"], df["accuracy_pct"])
    ax.set_xlabel("run_id")
    ax.set_ylabel("accuracy (%)")
    ax.set_ylim(0, 100)
    return True


def draw_damage_totals_over_runs(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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


def draw_performance_summary_view(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "runs"):
        no_data(ax, "runs table missing")
        return False

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
    ax.barh(metrics, values, color=colors)
    ax.set_xlabel("Value")
    ax.set_title(
        f"Performance Summary (Level {df['max_level'].iloc[0] if not df.empty else '?'}, "
        f"{df['difficulty'].iloc[0] if not df.empty else '?'})"
    )
    ax.grid(True, alpha=0.3, axis="x")

    for i, (metric, val) in enumerate(zip(metrics, values)):
        ax.text(val, i, f"  {val:.2f}", va="center", fontsize=10, fontweight="bold")
    return True
