"""
Explicit scene transition type for a scene-driven main loop.

Scenes may eventually return SceneTransition from handle_input/update instead of
a transition dict. For now, transition-returning methods are stubs used only in tests.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# Kind names for SceneTransition.kind
KIND_NONE = "NONE"
KIND_PUSH = "PUSH"
KIND_POP = "POP"
KIND_REPLACE = "REPLACE"
KIND_QUIT_GAME = "QUIT_GAME"


@dataclass(frozen=True)
class SceneTransition:
    """Lightweight descriptor for a requested scene transition.

    kind: one of NONE, PUSH, POP, REPLACE, QUIT_GAME.
    scene_name: optional; used when kind is PUSH or REPLACE (e.g. "PAUSED", "MENU").
    """
    kind: str
    scene_name: Optional[str] = None

    @classmethod
    def none(cls) -> "SceneTransition":
        return cls(kind=KIND_NONE)

    @classmethod
    def push(cls, scene_name: str) -> "SceneTransition":
        return cls(kind=KIND_PUSH, scene_name=scene_name)

    @classmethod
    def pop(cls) -> "SceneTransition":
        return cls(kind=KIND_POP)

    @classmethod
    def replace(cls, scene_name: str) -> "SceneTransition":
        return cls(kind=KIND_REPLACE, scene_name=scene_name)

    @classmethod
    def quit_game(cls) -> "SceneTransition":
        return cls(kind=KIND_QUIT_GAME)
