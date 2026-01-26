"""
Scene base and SceneStack for the gameplay screen flow.

Scenes manage a single screen (gameplay, pause, high scores, name input). The game loop
delegates handle_input, update, and render to the current scene. Transitions are expressed
via the return value of handle_input (e.g. pop, push, quit, restart).

Order of operations in the loop: handle_input -> apply transitions -> update -> render.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Scene(Protocol):
    """Protocol for a scene. handle_input returns a transition dict; update/render mutate nothing except via game_state/ctx."""

    def state_id(self) -> str:
        """Identifier used for game_state.current_screen when this scene is active (e.g. 'PLAYING', 'PAUSED')."""
        ...

    def handle_input(self, events: list, game_state: Any, ctx: dict) -> dict:
        """
        Process input events. Return a transition dict with any of:
          screen: str — set current_screen and stack will be synced (e.g. 'MENU' to exit to menu)
          pop: bool — pop this scene (resume / back)
          push: Scene — push another scene (e.g. push PauseScene)
          quit: bool, restart: bool, restart_to_wave1: bool, replay: bool — interpreted by the loop
        """
        ...

    def update(self, dt: float, game_state: Any, ctx: dict) -> None:
        """Update this scene for this frame (e.g. run gameplay systems, or no-op for static menus)."""
        ...

    def render(self, render_ctx: Any, game_state: Any, ctx: dict) -> None:
        """Draw this scene. render_ctx provides screen, fonts, dimensions."""
        ...

    def on_enter(self, game_state: Any, ctx: dict) -> None:
        """Called when this scene becomes current (after push or when replacing). Optional no-op by default."""
        ...

    def on_exit(self, game_state: Any, ctx: dict) -> None:
        """Called when this scene is replaced or popped. Optional no-op by default."""
        ...


class SceneStack:
    """
    Stack of scenes. The top scene is the current one; input/update/render go to current().
    Used for: gameplay -> pause (push) -> resume (pop); gameplay -> name input -> high scores (push/pop).
    """

    __slots__ = ("_stack",)

    def __init__(self) -> None:
        self._stack: list[Scene] = []

    def push(self, scene: Scene) -> None:
        self._stack.append(scene)

    def pop(self) -> Scene | None:
        if not self._stack:
            return None
        return self._stack.pop()

    def current(self) -> Scene | None:
        if not self._stack:
            return None
        return self._stack[-1]

    def clear(self) -> None:
        self._stack.clear()

    def __len__(self) -> int:
        return len(self._stack)
