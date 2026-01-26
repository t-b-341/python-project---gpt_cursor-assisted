"""SQLite and DataFrame helpers for telemetry visualization."""
from __future__ import annotations

import sqlite3
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

# GPU acceleration support (optional). Single capability flag from gpu_physics.
try:
    from gpu_physics import CUDA_AVAILABLE
    USE_GPU = CUDA_AVAILABLE
except Exception:
    USE_GPU = False


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
