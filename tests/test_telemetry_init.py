"""Tests for telemetry schema initialization (in-memory DB, no display)."""
import sqlite3
import unittest

from telemetry.schema import table_exists, get_columns, init_schema


class TestTelemetrySchema(unittest.TestCase):
    def test_init_schema_creates_runs_table(self):
        conn = sqlite3.connect(":memory:")
        init_schema(conn)
        assert table_exists(conn, "runs")
        conn.close()

    def test_init_schema_creates_enemy_spawns_and_shots(self):
        conn = sqlite3.connect(":memory:")
        init_schema(conn)
        assert table_exists(conn, "enemy_spawns")
        assert table_exists(conn, "shots")
        conn.close()

    def test_runs_table_has_expected_columns(self):
        conn = sqlite3.connect(":memory:")
        init_schema(conn)
        cols = get_columns(conn, "runs")
        assert "id" in cols
        assert "started_at" in cols
        assert "player_max_hp" in cols
        assert "seconds_survived" in cols
        conn.close()

    def test_init_schema_idempotent(self):
        conn = sqlite3.connect(":memory:")
        init_schema(conn)
        init_schema(conn)
        assert table_exists(conn, "runs")
        cols = get_columns(conn, "runs")
        assert "id" in cols
        conn.close()
