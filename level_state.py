"""Level geometry container. Holds all block lists and zone data for a level.
Populated at level build; read by collision_system, movement_system, spawn_system."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class LevelState:
    """Holds all level geometry: blocks, hazards, and moving zone.
    
    Used by GameState.level so geometry is no longer in module-level globals.
    """
    static_blocks: list[Any]  # list of rect-like dicts; empty in current design
    trapezoid_blocks: list[Any]
    triangle_blocks: list[Any]
    destructible_blocks: list[Any]
    moveable_blocks: list[Any]  # moveable_destructible_blocks
    giant_blocks: list[Any]
    super_giant_blocks: list[Any]
    hazard_obstacles: list[Any]
    moving_health_zone: Optional[dict[str, Any]] = None
