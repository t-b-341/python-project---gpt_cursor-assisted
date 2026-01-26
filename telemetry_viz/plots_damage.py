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
    """Scatter plot of death positions for one run. Axes match in-game coordinates (px). Color by wave_number if present."""
    if not table_exists(conn, "player_deaths"):
        no_data(ax, "player_deaths table missing")
        return False

    # Prefer wave_number when present (schema migration adds it)
    try:
        df = read_df(
            conn,
            """
            SELECT player_x AS x, player_y AS y, COALESCE(wave_number, 0) AS wave
            FROM player_deaths
            WHERE run_id = ?
            ORDER BY t ASC;
            """,
            (run_id,),
        )
    except Exception:
        df = read_df(
            conn,
            "SELECT player_x AS x, player_y AS y FROM player_deaths WHERE run_id = ? ORDER BY t ASC;",
            (run_id,),
        )
        df["wave"] = 0

    if df.empty:
        no_data(ax, "No deaths logged for this run")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)
    df["wave"] = safe_numeric(df["wave"], fill=0).astype(int)

    if "wave" in df.columns and df["wave"].nunique() > 1:
        scatter = ax.scatter(df["x"], df["y"], c=df["wave"], cmap="viridis", s=28, alpha=0.8)
        plt.colorbar(scatter, ax=ax, label="Wave")
    else:
        ax.scatter(df["x"], df["y"], s=28, alpha=0.8, color="crimson")
    ax.set_xlabel("x (px, in-game)")
    ax.set_ylabel("y (px, in-game)")
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


def draw_difficulty_time_series(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    """For one run: enemies_alive, player_health, cumulative damage over time. Vertical lines at wave start."""
    if not table_exists(conn, "runs"):
        no_data(ax, "runs table missing")
        return False

    max_hp = 1000
    row = conn.execute("SELECT player_max_hp FROM runs WHERE id = ?", (run_id,)).fetchone()
    if row and row[0] is not None:
        max_hp = int(row[0])

    plotted = False
    has_samples = table_exists(conn, "run_state_samples")
    if has_samples:
        df = read_df(
            conn,
            "SELECT t, player_hp, enemies_alive FROM run_state_samples WHERE run_id = ? ORDER BY t",
            (run_id,),
        )
        if not df.empty:
            df["t"] = safe_numeric(df["t"], fill=0.0)
            df["hp_ratio"] = safe_numeric(df["player_hp"], fill=0).astype(float) / max(1, max_hp)
            df["enemies_alive"] = safe_numeric(df["enemies_alive"], fill=0)
            ax.plot(df["t"], df["hp_ratio"], label="HP (ratio)", color="green", alpha=0.9)
            ax_twin = ax.twinx()
            ax_twin.plot(df["t"], df["enemies_alive"], label="Enemies alive", color="orange", alpha=0.8)
            ax_twin.set_ylabel("Enemies alive", color="orange")
            ax_twin.tick_params(axis="y", labelcolor="orange")
            plotted = True

    if table_exists(conn, "player_damage"):
        dmg = read_df(
            conn,
            "SELECT t, amount FROM player_damage WHERE run_id = ? ORDER BY t",
            (run_id,),
        )
        if not dmg.empty:
            dmg["t"] = safe_numeric(dmg["t"], fill=0.0)
            dmg["amount"] = safe_numeric(dmg["amount"], fill=0.0)
            dmg["cum"] = dmg["amount"].cumsum()
            ax.plot(dmg["t"], dmg["cum"], label="Cum. damage", color="red", alpha=0.7)
            ax.set_xlabel("Time (s)")
            plotted = True

    if not plotted:
        no_data(ax, "No run_state_samples or player_damage for this run")
        return False

    if table_exists(conn, "waves"):
        wave_rows = conn.execute(
            "SELECT t FROM waves WHERE run_id = ? AND event_type = 'start' ORDER BY t",
            (run_id,),
        ).fetchall()
        for (t,) in wave_rows:
            ax.axvline(x=float(t), color="gray", linestyle="--", alpha=0.5)

    ax.set_ylabel("HP ratio / Cum. damage")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    return True
