"""Tests that data-driven enemy and projectile definitions load and match expected defaults."""
from __future__ import annotations

import pytest

from config.enemy_defs import get_enemy_def, clear_enemy_def_cache
from config.projectile_defs import get_projectile_def, clear_projectile_def_cache


def test_get_enemy_def_ambient():
    clear_enemy_def_cache()
    d = get_enemy_def("ambient")
    assert d is not None
    assert d.get("type_id") == "ambient" or d.get("type") == "ambient"
    assert "ambient" in d.get("behavior_flags", set())


def test_get_enemy_def_final_boss():
    clear_enemy_def_cache()
    d = get_enemy_def("FINAL_BOSS")
    assert d is not None
    assert d.get("type") == "FINAL_BOSS" or d.get("type_id") == "FINAL_BOSS"
    assert "boss" in d.get("behavior_flags", set())


def test_get_enemy_def_unknown_returns_none():
    clear_enemy_def_cache()
    assert get_enemy_def("nonexistent_type_xyz") is None


def test_get_projectile_def_player_basic():
    clear_projectile_def_cache()
    d = get_projectile_def("player_basic")
    assert d is not None
    assert d["type_id"] == "player_basic"
    assert d["speed"] > 0
    assert d["damage"] > 0
    assert "num_projectiles" in d


def test_get_projectile_def_enemy_default():
    clear_projectile_def_cache()
    d = get_projectile_def("enemy_default")
    assert d is not None
    assert d["type_id"] == "enemy_default"
    assert d["damage"] > 0
    assert "size" in d and len(d["size"]) == 2
    assert "color" in d


def test_get_projectile_def_unknown_returns_none():
    clear_projectile_def_cache()
    assert get_projectile_def("nonexistent_proj_xyz") is None


def test_projectile_def_caching():
    clear_projectile_def_cache()
    a = get_projectile_def("player_basic")
    b = get_projectile_def("player_basic")
    assert a is b
