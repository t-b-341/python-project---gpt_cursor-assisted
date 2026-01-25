"""Damage and death plots."""
from __future__ import annotations

import sqlite3

import matplotlib.pyplot as plt
import numpy as np

from telemetry_viz.db_utils import no_data, read_df, safe_numeric, table_exists


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

    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(df)))
    ax.barh(df["enemy_type"], df["total_damage"], color=colors)
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


def draw_damage_heatmap_by_wave(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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
