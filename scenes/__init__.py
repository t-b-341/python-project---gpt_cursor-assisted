"""Scenes: gameplay, pause, high scores, name input. Driven by SceneStack in the game loop."""
from .base import Scene, SceneStack
from .gameplay import GameplayScene
from .pause import PauseScene
from .high_scores import HighScoreScene
from .name_input import NameInputScene

__all__ = [
    "Scene",
    "SceneStack",
    "GameplayScene",
    "PauseScene",
    "HighScoreScene",
    "NameInputScene",
]
