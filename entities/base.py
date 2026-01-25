"""
Base class for all game entities. Provides a common interface for position, health,
and unified update/draw hooks. Subclasses override update() and draw() as needed.
"""
from typing import Any, Optional

import pygame


class Entity:
    """
    Minimal base for entity-like objects (enemies, allies, projectiles).
    Holds position (rect), hp, and an alive/active flag.
    update(dt, state) and draw(screen) are no-ops by default; subclasses override.
    """

    __slots__ = ("_rect", "_hp", "_alive")

    def __init__(
        self,
        rect: Optional[pygame.Rect] = None,
        hp: int = 1,
        alive: bool = True,
    ):
        self._rect = rect
        self._hp = int(hp)
        self._alive = bool(alive)

    @property
    def rect(self) -> Optional[pygame.Rect]:
        return self._rect

    @rect.setter
    def rect(self, value: Optional[pygame.Rect]) -> None:
        self._rect = value

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = int(value)

    @property
    def alive(self) -> bool:
        return self._alive

    @alive.setter
    def alive(self, value: bool) -> None:
        self._alive = bool(value)

    def update(self, dt: float, state: Any) -> None:
        """Override in subclasses. Default no-op."""
        pass

    def draw(self, screen: pygame.Surface, state: Any = None) -> None:
        """Override in subclasses. Default no-op."""
        pass
