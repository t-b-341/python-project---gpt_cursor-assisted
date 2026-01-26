"""
Lightweight ECS-style components for entities.

Components are simple dataclasses. Systems can query entities by component type
via GameState.get_entities_with(PositionComponent, VelocityComponent), etc.
This layer coexists with existing list-based storage (enemies, player_bullets, etc.)
during gradual migration.

Type-branch inventory (for data-driven migration):
- Enemies: enemy.get("type") (queen, pawn, suicide, grunt, …), flags like is_boss,
  is_patrol, is_ambient, has_shield, has_reflective_shield, fires_laser, fires_rockets,
  can_use_grenades, is_suicide, is_flamethrower. See enemies.make_enemy_from_template,
  systems.ai_system, systems.collision_system, systems.movement_system.
- Projectiles: enemy_type, shape, color on dicts in player_bullets / enemy_projectiles.
- Pickups: pickup_type in (armor, dash_recharge, firerate, health, …) in game.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import pygame


@dataclass
class PositionComponent:
    """Position and size on screen. Uses pygame.Rect for compatibility."""
    rect: pygame.Rect


@dataclass
class VelocityComponent:
    """Movement per second (pixels). Can be updated by movement/input systems."""
    vx: float = 0.0
    vy: float = 0.0

    def as_vector(self) -> pygame.Vector2:
        return pygame.Vector2(self.vx, self.vy)


@dataclass
class HealthComponent:
    """Current and max HP. Used for damage, death, and UI."""
    hp: int
    max_hp: int

    @property
    def alive(self) -> bool:
        return self.hp > 0


@dataclass
class RenderComponent:
    """How to draw: color and optional size override. Replaces ad-hoc enemy['color'] etc."""
    color: tuple[int, int, int] = (200, 50, 50)
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class AIComponent:
    """Behavior identifier for AI system. Reduces 'if enemy_type == X' branching."""
    behavior: str = "chase"  # chase | patrol | ambient | boss | spawner | suicide
    flags: set[str] = field(default_factory=set)  # e.g. has_shield, fires_laser


@dataclass
class ColliderComponent:
    """Marks entity as solid for collision. Optionally carry size if different from position rect."""
    layer: str = "default"  # default | player_bullet | enemy_projectile | pickup
    radius: Optional[float] = None  # For circle vs rect; None => use rect
