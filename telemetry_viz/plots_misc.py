"""Miscellaneous plots: bullets, enemies, score, weapons, zones, actions."""
from __future__ import annotations

import sqlite3

import matplotlib.pyplot as plt
import numpy as np

from telemetry_viz.db_utils import no_data, read_df, safe_numeric, table_exists


def draw_bullet_shape_distribution(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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
    ax.barh(df["color_label"], df["count"], color=colors)
    ax.set_xlabel("Usage Count")
    ax.set_ylabel("Color (RGB)")
    return True


def draw_enemy_movement_paths(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "enemy_positions"):
        no_data(ax, "enemy_positions table missing")
        return False

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


def draw_score_progression(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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

    ax.plot(df["t"], df["hp_pct"], linewidth=2, label="Boss HP %")
    ax.fill_between(df["t"], df["hp_pct"], alpha=0.3)

    phase_changes = df[df["event_type"] == "phase_transition"]
    if not phase_changes.empty:
        ax.scatter(
            phase_changes["t"], phase_changes["hp_pct"], c="red", s=100,
            marker="X", zorder=5, label="Phase Change"
        )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("HP %")
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    ax.legend()
    return True


def draw_weapon_usage(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
    if not table_exists(conn, "weapon_switches"):
        no_data(ax, "weapon_switches table missing")
        return False

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
    ax.barh(df["pickup_type"], df["collected_count"], color=colors)
    ax.set_xlabel("Collected Count")
    ax.set_ylabel("Pickup Type")
    ax.grid(True, alpha=0.3, axis="x")

    for i, (idx, row) in enumerate(df.iterrows()):
        ax.text(row["collected_count"], i, f"  {row['collection_rate']:.0f}%",
                va="center", fontsize=9)
    return True


def draw_overshield_usage(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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
    ax.axhline(
        y=df["max_overshield"].iloc[0] if not df.empty else 0,
        color="red", linestyle="--", alpha=0.5, label="Max Overshield"
    )
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Overshield")
    ax.grid(True, alpha=0.3)
    ax.legend()
    return True


def draw_player_action_frequency(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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
    ax.barh(df["transition"], df["frequency"], color=colors)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Action Transition")
    ax.grid(True, alpha=0.3, axis="x")

    for i, (idx, row) in enumerate(df.iterrows()):
        ax.text(row["frequency"], i, f"  {row['avg_time']:.2f}s avg",
                va="center", fontsize=8)
    return True


def draw_running_statistics(ax: plt.Axes, conn: sqlite3.Connection, run_id: int) -> bool:
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
