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

    ax.plot(df["x"], df["y"])
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", adjustable="datalim")
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
        WHERE run_id = ?;
        """,
        (run_id,),
    )
    if df.empty:
        no_data(ax, "No player_positions for this run")
        return False

    df["x"] = safe_numeric(df["x"], fill=0.0)
    df["y"] = safe_numeric(df["y"], fill=0.0)

    # Note: colorbar is tricky in a single shared axes window.
    # For popup, we omit colorbar; PNGs still look fine.
    ax.hist2d(df["x"], df["y"], bins=50)
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
        SELECT target_x, target_y
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

    ax.scatter(df["target_x"], df["target_y"], s=8)
    ax.set_xlabel("target_x")
    ax.set_ylabel("target_y")
    ax.set_aspect("equal", adjustable="datalim")
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

    ax.plot(df["t"], df["cum_damage"])
    ax.set_xlabel("t (s)")
    ax.set_ylabel("cumulative damage")
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

    ax.bar(df["enemy_type"], df["total_damage"])
    ax.set_xlabel("enemy_type")
    ax.set_ylabel("total damage")
    ax.tick_params(axis="x", rotation=30)
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
        Page("Shots scatter", "shots_scatter.png", draw_shots_scatter),
        Page("Damage taken timeline", "damage_taken_timeline.png", draw_damage_taken_timeline),
        Page("Damage taken by enemy type", "damage_taken_by_enemy.png", draw_damage_taken_by_enemy),
        Page("Damage dealt by enemy type", "damage_dealt_by_enemy.png", draw_damage_dealt_by_enemy),
        Page("Death locations", "death_locations.png", draw_death_locations),
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
