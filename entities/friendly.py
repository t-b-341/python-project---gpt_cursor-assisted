"""
Friendly AI entity: wraps the existing friendly dict for unified Entity interface
while keeping full dict-like access for compatibility.
"""
from typing import Any, Optional

import pygame

from .base import Entity


class Friendly(Entity):
    """
    Friendly AI unit that extends Entity and wraps the legacy dict representation.
    Supports both attribute access and dict access (["rect"], ["hp"], .get(...)).
    """

    def __init__(self, data: dict):
        rect = data.get("rect")
        hp = data.get("hp", 0)
        super().__init__(rect=rect, hp=hp, alive=hp > 0)
        self._data = data

    @property
    def rect(self) -> Optional[pygame.Rect]:
        return self._data.get("rect")

    @rect.setter
    def rect(self, value: Optional[pygame.Rect]) -> None:
        self._data["rect"] = value

    @property
    def hp(self) -> int:
        return self._data.get("hp", 0)

    @hp.setter
    def hp(self, value: int) -> None:
        self._data["hp"] = int(value)

    @property
    def alive(self) -> bool:
        return self._data.get("hp", 0) > 0

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def update(self, dt: float, state: Any) -> None:
        """Per-friendly logic remains in the game loop; hook for future use."""
        pass

    def draw(self, screen: pygame.Surface, state: Any = None) -> None:
        """Draw this friendly (rect only; health bars stay in the game loop)."""
        rect = self._data.get("rect")
        if rect is None:
            return
        color = self._data.get("color", (100, 200, 100))
        pygame.draw.rect(screen, color, rect)
