"""Scenes: gameplay, pause, high scores, name input, shader test, title, options. Driven by SceneStack in the game loop."""
from .base import Scene, SceneStack
from .gameplay import GameplayScene
from .high_scores import HighScoreScene
from .name_input import NameInputScene
from .options import OptionsScene
from .pause import PauseScene
from .shader_test import ShaderTestScene
from .title import TitleScene

__all__ = [
    "Scene",
    "SceneStack",
    "GameplayScene",
    "PauseScene",
    "HighScoreScene",
    "NameInputScene",
    "OptionsScene",
    "ShaderTestScene",
    "TitleScene",
]
