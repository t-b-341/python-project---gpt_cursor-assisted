import sqlite3
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass
class EnemySpawnEvent:
    t: float
    enemy_type: str
    x: int
    y: int
    w: int
    h: int
    hp: int


@dataclass
class PlayerPosEvent:
    t: float
    x: int
    y: int


@dataclass
class ShotEvent:
    t: float
    origin_x: int
    origin_y: int
    target_x: int
    target_y: int
    dir_x: float
    dir_y: float


class Telemetry:
    """
    Buffered SQLite telemetry writer.

    - Keeps inserts buffered in memory
    - Flushes on a timer (e.g., every 0.5s) or when buffer grows large
    - Flushes and closes cleanly on shutdown
    """

    def __init__(self, db_path: str = "game_telemetry.db", flush_interval_s: float = 0.5, max_buffer: int = 500):
        self.db_path = db_path
        self.flush_interval_s = float(flush_interval_s)
        self.max_buffer = int(max_buffer)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._init_schema()

        self.run_id: Optional[int] = None
        self._time_since_flush = 0.0

        self._enemy_spawn_buf: list[tuple] = []
        self._pos_buf: list[tuple] = []
        self._shot_buf: list[tuple] = []

    def _init_schema(self) -> None:
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            seconds_survived REAL,
            player_max_hp INTEGER NOT NULL,
            player_hp_end INTEGER,
            shots_fired INTEGER NOT NULL DEFAULT 0,
            hits INTEGER NOT NULL DEFAULT 0,
            damage_taken INTEGER NOT NULL DEFAULT 0,
            enemies_spawned INTEGER NOT NULL DEFAULT 0,
            enemies_killed INTEGER NOT NULL DEFAULT 0
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS enemy_spawns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            enemy_type TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            w INTEGER NOT NULL,
            h INTEGER NOT NULL,
            hp INTEGER NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS player_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS shots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            origin_x INTEGER NOT NULL,
            origin_y INTEGER NOT NULL,            target_x INTEGER NOT NULL,
            target_y INTEGER NOT NULL,
            dir_x REAL NOT NULL,
            dir_y REAL NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        self.conn.commit()

    def start_run(self, started_at_iso: str, player_max_hp: int) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO runs (started_at, player_max_hp) VALUES (?, ?);",
            (started_at_iso, int(player_max_hp)),
        )
        self.conn.commit()
        self.run_id = cur.lastrowid
        return self.run_id

    def end_run(
        self,
        ended_at_iso: str,
        seconds_survived: float,
        player_hp_end: int,
        shots_fired: int,
        hits: int,
        damage_taken: int,
        enemies_spawned: int,
        enemies_killed: int,
    ) -> None:
        if self.run_id is None:
            return

        # Flush any buffered events first
        self.flush(force=True)

        self.conn.execute(
            """
            UPDATE runs
            SET ended_at = ?,
                seconds_survived = ?,
                player_hp_end = ?,
                shots_fired = ?,
                hits = ?,
                damage_taken = ?,
                enemies_spawned = ?,
                enemies_killed = ?
            WHERE id = ?;
            """,
            (
                ended_at_iso,
                float(seconds_survived),
                int(player_hp_end),
                int(shots_fired),
                int(hits),
                int(damage_taken),
                int(enemies_spawned),
                int(enemies_killed),
                int(self.run_id),
            ),
        )
        self.conn.commit()

    def log_enemy_spawn(self, event: EnemySpawnEvent) -> None:
        if self.run_id is None:
            return
        self._enemy_spawn_buf.append(
            (self.run_id, event.t, event.enemy_type, event.x, event.y, event.w, event.h, event.hp)
        )

    def log_player_position(self, event: PlayerPosEvent) -> None:
        if self.run_id is None:
            return
        self._pos_buf.append((self.run_id, event.t, event.x, event.y))

    def log_shot(self, event: ShotEvent) -> None:
        if self.run_id is None:
            return
        self._shot_buf.append(
            (self.run_id, event.t, event.origin_x, event.origin_y, event.target_x, event.target_y, event.dir_x, event.dir_y)
        )

    def tick(self, dt: float) -> None:
        """Call once per frame; flushes periodically."""
        self._time_since_flush += float(dt)
        if self._time_since_flush >= self.flush_interval_s:
            self.flush()

        # safety: if buffers get large, flush early
        if (len(self._enemy_spawn_buf) + len(self._pos_buf) + len(self._shot_buf)) >= self.max_buffer:
            self.flush()

    def flush(self, force: bool = False) -> None:
        if not force:
            # normal timed flush
            self._time_since_flush = 0.0

        cur = self.conn.cursor()
        wrote_any = False

        if self._enemy_spawn_buf:
            cur.executemany(
                """
                INSERT INTO enemy_spawns (run_id, t, enemy_type, x, y, w, h, hp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                self._enemy_spawn_buf,
            )
            self._enemy_spawn_buf.clear()
            wrote_any = True

        if self._pos_buf:
            cur.executemany(
                """
                INSERT INTO player_positions (run_id, t, x, y)
                VALUES (?, ?, ?, ?);
                """,
                self._pos_buf,
            )
            self._pos_buf.clear()
            wrote_any = True

        if self._shot_buf:
            cur.executemany(
                """
                INSERT INTO shots (run_id, t, origin_x, origin_y, target_x, target_y, dir_x, dir_y)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                self._shot_buf,
            )
            self._shot_buf.clear()
            wrote_any = True

        if wrote_any:
            self.conn.commit()

    def close(self) -> None:
        self.flush(force=True)
        self.conn.close()
