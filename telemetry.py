import sqlite3
from dataclasses import dataclass
from typing import Optional


# ----------------------------
# Events
# ----------------------------
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


@dataclass
class EnemyHitEvent:
    t: float
    enemy_type: str
    enemy_x: int
    enemy_y: int
    damage: int
    enemy_hp_after: int
    killed: bool


@dataclass
class PlayerDamageEvent:
    t: float
    amount: int
    source_type: str               # e.g. "enemy_projectile"
    source_enemy_type: Optional[str]
    player_x: int
    player_y: int
    player_hp_after: int


@dataclass
class PlayerDeathEvent:
    t: float
    player_x: int
    player_y: int
    lives_left: int


@dataclass
class WaveEvent:
    t: float
    wave_number: int
    event_type: str  # "start" or "end"
    enemies_spawned: int
    hp_scale: float
    speed_scale: float


@dataclass
class EnemyPositionEvent:
    t: float
    enemy_type: str
    x: int
    y: int
    speed: float
    vel_x: float
    vel_y: float


@dataclass
class PlayerVelocityEvent:
    t: float
    x: int
    y: int
    vel_x: float
    vel_y: float
    speed: float


@dataclass
class BulletMetadataEvent:
    t: float
    bullet_type: str  # "player" or "enemy"
    shape: str
    color_r: int
    color_g: int
    color_b: int
    source_enemy_type: Optional[str] = None


class Telemetry:
    """
    Buffered SQLite telemetry writer.

    - Buffers inserts in memory
    - Flushes on a timer or when buffers get large
    - Flushes and closes cleanly on shutdown
    """

    def __init__(self, db_path: str = "game_telemetry.db", flush_interval_s: float = 0.5, max_buffer: int = 500):
        self.db_path = db_path
        self.flush_interval_s = float(flush_interval_s)
        self.max_buffer = int(max_buffer)

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._init_schema_and_migrate()

        self.run_id: Optional[int] = None
        self._time_since_flush = 0.0

        # Buffers
        self._enemy_spawn_buf: list[tuple] = []
        self._pos_buf: list[tuple] = []
        self._shot_buf: list[tuple] = []

        self._enemy_hit_buf: list[tuple] = []
        self._player_damage_buf: list[tuple] = []
        self._player_death_buf: list[tuple] = []
        
        # New buffers
        self._wave_buf: list[tuple] = []
        self._enemy_pos_buf: list[tuple] = []
        self._player_velocity_buf: list[tuple] = []
        self._bullet_metadata_buf: list[tuple] = []

    # ----------------------------
    # Schema helpers
    # ----------------------------
    def _table_exists(self, name: str) -> bool:
        row = self.conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;",
            (name,),
        ).fetchone()
        return row is not None

    def _columns(self, table: str) -> set[str]:
        if not self._table_exists(table):
            return set()
        rows = self.conn.execute(f"PRAGMA table_info({table});").fetchall()
        return {r[1] for r in rows}

    def _add_column_if_missing(self, table: str, col: str, ddl: str) -> None:
        cols = self._columns(table)
        if col in cols:
            return
        self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {ddl};")
        self.conn.commit()

    def _init_schema_and_migrate(self) -> None:
        cur = self.conn.cursor()

        # Create runs table if missing (base version; we'll migrate after)
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

        # Ensure new columns exist (migration)
        # Note: SQLite doesn't support ADD COLUMN IF NOT EXISTS, so we check via PRAGMA table_info.
        self.conn.commit()
        self._add_column_if_missing("runs", "damage_dealt", "damage_dealt INTEGER NOT NULL DEFAULT 0")
        self._add_column_if_missing("runs", "deaths", "deaths INTEGER NOT NULL DEFAULT 0")
        self._add_column_if_missing("runs", "max_wave", "max_wave INTEGER")
        
        # Add bullet metadata columns to shots table
        self._add_column_if_missing("shots", "shape", "shape TEXT")
        self._add_column_if_missing("shots", "color_r", "color_r INTEGER")
        self._add_column_if_missing("shots", "color_g", "color_g INTEGER")
        self._add_column_if_missing("shots", "color_b", "color_b INTEGER")

        # Existing tables (safe to CREATE IF NOT EXISTS)
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
            origin_y INTEGER NOT NULL,
            target_x INTEGER NOT NULL,
            target_y INTEGER NOT NULL,
            dir_x REAL NOT NULL,
            dir_y REAL NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        # New tables
        cur.execute("""
        CREATE TABLE IF NOT EXISTS enemy_hits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            enemy_type TEXT NOT NULL,
            enemy_x INTEGER NOT NULL,
            enemy_y INTEGER NOT NULL,
            damage INTEGER NOT NULL,
            enemy_hp_after INTEGER NOT NULL,
            killed INTEGER NOT NULL,  -- 0/1
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS player_damage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            amount INTEGER NOT NULL,
            source_type TEXT NOT NULL,
            source_enemy_type TEXT,
            player_x INTEGER NOT NULL,
            player_y INTEGER NOT NULL,
            player_hp_after INTEGER NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS player_deaths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            player_x INTEGER NOT NULL,
            player_y INTEGER NOT NULL,
            lives_left INTEGER NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        # New tables for enhanced telemetry
        cur.execute("""
        CREATE TABLE IF NOT EXISTS waves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            wave_number INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            enemies_spawned INTEGER NOT NULL,
            hp_scale REAL NOT NULL,
            speed_scale REAL NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS enemy_positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            enemy_type TEXT NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            speed REAL NOT NULL,
            vel_x REAL NOT NULL,
            vel_y REAL NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS player_velocities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            x INTEGER NOT NULL,
            y INTEGER NOT NULL,
            vel_x REAL NOT NULL,
            vel_y REAL NOT NULL,
            speed REAL NOT NULL,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS bullet_metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            t REAL NOT NULL,
            bullet_type TEXT NOT NULL,
            shape TEXT NOT NULL,
            color_r INTEGER NOT NULL,
            color_g INTEGER NOT NULL,
            color_b INTEGER NOT NULL,
            source_enemy_type TEXT,
            FOREIGN KEY(run_id) REFERENCES runs(id) ON DELETE CASCADE
        );
        """)

        self.conn.commit()

    # ----------------------------
    # Run lifecycle
    # ----------------------------
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
        damage_dealt: int,
        enemies_spawned: int,
        enemies_killed: int,
        deaths: int,
        max_wave: Optional[int] = None,
    ) -> None:
        if self.run_id is None:
            return

        self.flush(force=True)

        # Build update query dynamically based on whether max_wave column exists
        cols = self._columns("runs")
        has_max_wave = "max_wave" in cols
        
        if has_max_wave and max_wave is not None:
            self.conn.execute(
                """
                UPDATE runs
                SET ended_at = ?,
                    seconds_survived = ?,
                    player_hp_end = ?,
                    shots_fired = ?,
                    hits = ?,
                    damage_taken = ?,
                    damage_dealt = ?,
                    enemies_spawned = ?,
                    enemies_killed = ?,
                    deaths = ?,
                    max_wave = ?
                WHERE id = ?;
                """,
                (
                    ended_at_iso,
                    float(seconds_survived),
                    int(player_hp_end),
                    int(shots_fired),
                    int(hits),
                    int(damage_taken),
                    int(damage_dealt),
                    int(enemies_spawned),
                    int(enemies_killed),
                    int(deaths),
                    int(max_wave),
                    int(self.run_id),
                ),
            )
        else:
            self.conn.execute(
                """
                UPDATE runs
                SET ended_at = ?,
                    seconds_survived = ?,
                    player_hp_end = ?,
                    shots_fired = ?,
                    hits = ?,
                    damage_taken = ?,
                    damage_dealt = ?,
                    enemies_spawned = ?,
                    enemies_killed = ?,
                    deaths = ?
                WHERE id = ?;
                """,
                (
                    ended_at_iso,
                    float(seconds_survived),
                    int(player_hp_end),
                    int(shots_fired),
                    int(hits),
                    int(damage_taken),
                    int(damage_dealt),
                    int(enemies_spawned),
                    int(enemies_killed),
                    int(deaths),
                    int(self.run_id),
                ),
            )
        self.conn.commit()

    # ----------------------------
    # Log methods (buffered)
    # ----------------------------
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

    def log_shot(self, event: ShotEvent, shape: Optional[str] = None, color: Optional[tuple[int, int, int]] = None) -> None:
        if self.run_id is None:
            return
        # Store shape and color if provided (for backward compatibility)
        if shape and color:
            # Update shots table with metadata if columns exist
            pass  # Will be handled separately via bullet_metadata table
        self._shot_buf.append(
            (self.run_id, event.t, event.origin_x, event.origin_y, event.target_x, event.target_y, event.dir_x, event.dir_y)
        )

    def log_enemy_hit(self, event: EnemyHitEvent) -> None:
        if self.run_id is None:
            return
        self._enemy_hit_buf.append(
            (
                self.run_id,
                float(event.t),
                event.enemy_type,
                int(event.enemy_x),
                int(event.enemy_y),
                int(event.damage),
                int(event.enemy_hp_after),
                1 if event.killed else 0,
            )
        )

    def log_player_damage(self, event: PlayerDamageEvent) -> None:
        if self.run_id is None:
            return
        self._player_damage_buf.append(
            (
                self.run_id,
                float(event.t),
                int(event.amount),
                event.source_type,
                event.source_enemy_type,
                int(event.player_x),
                int(event.player_y),
                int(event.player_hp_after),
            )
        )

    def log_player_death(self, event: PlayerDeathEvent) -> None:
        if self.run_id is None:
            return
        self._player_death_buf.append(
            (self.run_id, float(event.t), int(event.player_x), int(event.player_y), int(event.lives_left))
        )

    def log_wave(self, event: WaveEvent) -> None:
        if self.run_id is None:
            return
        self._wave_buf.append(
            (
                self.run_id,
                float(event.t),
                int(event.wave_number),
                event.event_type,
                int(event.enemies_spawned),
                float(event.hp_scale),
                float(event.speed_scale),
            )
        )

    def log_enemy_position(self, event: EnemyPositionEvent) -> None:
        if self.run_id is None:
            return
        self._enemy_pos_buf.append(
            (
                self.run_id,
                float(event.t),
                event.enemy_type,
                int(event.x),
                int(event.y),
                float(event.speed),
                float(event.vel_x),
                float(event.vel_y),
            )
        )

    def log_player_velocity(self, event: PlayerVelocityEvent) -> None:
        if self.run_id is None:
            return
        self._player_velocity_buf.append(
            (
                self.run_id,
                float(event.t),
                int(event.x),
                int(event.y),
                float(event.vel_x),
                float(event.vel_y),
                float(event.speed),
            )
        )

    def log_bullet_metadata(self, event: BulletMetadataEvent) -> None:
        if self.run_id is None:
            return
        self._bullet_metadata_buf.append(
            (
                self.run_id,
                float(event.t),
                event.bullet_type,
                event.shape,
                int(event.color_r),
                int(event.color_g),
                int(event.color_b),
                event.source_enemy_type,
            )
        )

    # ----------------------------
    # Flush / tick / close
    # ----------------------------
    def tick(self, dt: float) -> None:
        self._time_since_flush += float(dt)
        if self._time_since_flush >= self.flush_interval_s:
            self.flush()

        if (
            len(self._enemy_spawn_buf)
            + len(self._pos_buf)
            + len(self._shot_buf)
            + len(self._enemy_hit_buf)
            + len(self._player_damage_buf)
            + len(self._player_death_buf)
            + len(self._wave_buf)
            + len(self._enemy_pos_buf)
            + len(self._player_velocity_buf)
            + len(self._bullet_metadata_buf)
        ) >= self.max_buffer:
            self.flush()

    def flush(self, force: bool = False) -> None:
        if not force:
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

        if self._enemy_hit_buf:
            cur.executemany(
                """
                INSERT INTO enemy_hits (run_id, t, enemy_type, enemy_x, enemy_y, damage, enemy_hp_after, killed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                self._enemy_hit_buf,
            )
            self._enemy_hit_buf.clear()
            wrote_any = True

        if self._player_damage_buf:
            cur.executemany(
                """
                INSERT INTO player_damage (run_id, t, amount, source_type, source_enemy_type, player_x, player_y, player_hp_after)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                self._player_damage_buf,
            )
            self._player_damage_buf.clear()
            wrote_any = True

        if self._player_death_buf:
            cur.executemany(
                """
                INSERT INTO player_deaths (run_id, t, player_x, player_y, lives_left)
                VALUES (?, ?, ?, ?, ?);
                """,
                self._player_death_buf,
            )
            self._player_death_buf.clear()
            wrote_any = True

        if self._wave_buf:
            cur.executemany(
                """
                INSERT INTO waves (run_id, t, wave_number, event_type, enemies_spawned, hp_scale, speed_scale)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                self._wave_buf,
            )
            self._wave_buf.clear()
            wrote_any = True

        if self._enemy_pos_buf:
            cur.executemany(
                """
                INSERT INTO enemy_positions (run_id, t, enemy_type, x, y, speed, vel_x, vel_y)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                self._enemy_pos_buf,
            )
            self._enemy_pos_buf.clear()
            wrote_any = True

        if self._player_velocity_buf:
            cur.executemany(
                """
                INSERT INTO player_velocities (run_id, t, x, y, vel_x, vel_y, speed)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                self._player_velocity_buf,
            )
            self._player_velocity_buf.clear()
            wrote_any = True

        if self._bullet_metadata_buf:
            cur.executemany(
                """
                INSERT INTO bullet_metadata (run_id, t, bullet_type, shape, color_r, color_g, color_b, source_enemy_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                self._bullet_metadata_buf,
            )
            self._bullet_metadata_buf.clear()
            wrote_any = True

        if wrote_any:
            self.conn.commit()

    def close(self) -> None:
        self.flush(force=True)
        self.conn.close()
