"""Tests that the systems registry runs systems in the expected order."""
from __future__ import annotations

import pytest

from systems.registry import SIMULATION_SYSTEMS
from systems.movement_system import update as movement_update
from systems.collision_system import update as collision_update
from systems.spawn_system import update as spawn_update
from systems.ai_system import update as ai_update


def test_simulation_systems_order():
    """Registry must run movement -> collision -> spawn -> ai (order documented in registry.py)."""
    expected = [movement_update, collision_update, spawn_update, ai_update]
    assert len(SIMULATION_SYSTEMS) == 4
    assert SIMULATION_SYSTEMS == expected
